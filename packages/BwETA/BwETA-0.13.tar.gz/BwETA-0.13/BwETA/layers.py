#@title Model everything
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from tensorflow.keras.layers import Dense
import math

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, embedding_dim):
        super(PositionalEncoding, self).__init__()
        self.embedding_dim = embedding_dim

    def call(self, inputs):
        current_dtype = inputs.dtype  # Get current dtype of inputs (bfloat16)
        sequence_length = tf.shape(inputs)[1]
        embedding_dim = self.embedding_dim

        # Cast position to the same dtype as inputs (bfloat16)
        position = tf.range(sequence_length, dtype=current_dtype)[:, tf.newaxis]  # (seq_len, 1)
        
        # Calculate the number of terms needed to cover all dimensions when interleaved
        num_terms = (embedding_dim + 1) // 2
        
        # Compute div_term in float32 first and then cast to current dtype
        div_term = tf.exp(
            tf.range(0, num_terms, dtype=tf.float32) * 
            -(tf.math.log(10000.0) / embedding_dim)
        )  # (num_terms,)

        div_term = tf.cast(div_term, current_dtype)  # Cast div_term to match inputs dtype
        
        # Compute sin and cos values
        sin_values = tf.sin(position * div_term)  # (seq_len, num_terms)
        cos_values = tf.cos(position * div_term)  # (seq_len, num_terms)
        
        # Interleave sin and cos values to form the positional encoding matrix
        pos_enc = tf.stack([sin_values, cos_values], axis=-1)  # (seq_len, num_terms, 2)
        pos_enc = tf.reshape(pos_enc, [sequence_length, 2 * num_terms])  # (seq_len, 2*num_terms)
        
        # Slice to the original embedding dimension in case it's odd
        pos_enc = pos_enc[:, :embedding_dim]
        
        # Expand dimensions to match batch size and add to inputs
        pos_enc = tf.expand_dims(pos_enc, 0)  # (1, seq_len, embedding_dim)
        pos_enc = tf.tile(pos_enc, [tf.shape(inputs)[0], 1, 1])  # (batch_size, seq_len, embedding_dim)
        
        return inputs + pos_enc


class TransformerBlock(layers.Layer):
    def __init__(self, num_heads, attention_dim, ff_dim=512, dropout_rate=0.1,**kwargs):
        super(TransformerBlock, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.attention_dim = attention_dim
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.is_frozen = False
        self.is_active = True

        # Multi-Head Attention Layer
        self.attention = MultiHeadSelfAttention(num_heads=num_heads, d_model=attention_dim)

        # Feed-forward network (two dense layers with ReLU activation)
        self.ffn1 = layers.Dense(ff_dim, activation=tf.keras.activations.gelu)
        self.ffn2 = layers.Dense(attention_dim)

        # Layer Normalization
        self.norm1 = layers.LayerNormalization()
        self.norm2 = layers.LayerNormalization()

        # Dropout layers
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)


    def call(self, inputs, mask=None):
        attn_output = self.attention(inputs, mask=mask)
        attn_output = self.dropout1(attn_output)
        out1 = self.norm1(inputs + attn_output)  # Add & Norm

        # Apply Feed-Forward Network
        ffn_output = self.ffn1(out1)
        ffn_output = self.ffn2(ffn_output)
        ffn_output = self.dropout2(ffn_output)
        out2 = self.norm2(out1 + ffn_output)  # Add & Norm

        return out2


    def activate(self):
        self.unfreeze()
        self.is_active = True
    
    def deactivate(self):
        self.freeze()
        self.is_active = False

    def freeze(self):
        for i in [self.attention,self.ffn1,self.ffn2]:
            i.trainable = False
        self.is_frozen = True

    def unfreeze(self):
        for i in [self.attention,self.ffn1,self.ffn2]:
            i.trainable = True
        self.is_frozen = False

class MultiHeadSelfAttention(tf.keras.layers.Layer):
    def __init__(self, num_heads, d_model):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        self.num_heads = num_heads
        self.d_model = d_model
        self.depth = d_model // num_heads

        # Compute Q, K, V together: output shape will be (batch, seq_len, 3*d_model)
        self.qkv_dense = Dense(d_model * 3)
        # Final projection to bring concatenated heads back to d_model
        self.out_dense = Dense(d_model)

    def call(self, x, mask=None):
        # x shape: (batch, seq_len, d_model)
        batch_size = tf.shape(x)[0]
        seq_len = tf.shape(x)[1]
        current_dtype = x.dtype
        
        if mask is not None:
            mask = tf.cast(mask,current_dtype)

        # Compute Q, K, V in one go and reshape:
        qkv = self.qkv_dense(x)  # (batch, seq_len, 3*d_model)
        qkv = tf.reshape(qkv, (batch_size, seq_len, 3, self.num_heads, self.depth))
        qkv = tf.transpose(qkv, perm=[2, 0, 3, 1, 4])  # (3, batch, num_heads, seq_len, depth)
        Q, K, V = qkv[0], qkv[1], qkv[2]  # each: (batch, num_heads, seq_len, depth)

        # Scaled dot-product attention:
        logits = tf.matmul(Q, K, transpose_b=True)  # (batch, num_heads, seq_len, seq_len)
        logits /= tf.math.sqrt(tf.cast(self.depth, current_dtype))

        if mask is not None:
            # Ensure mask broadcasts correctly: (batch, 1, seq_len, seq_len) is typical.
            logits += (mask * tf.cast(-1e9,current_dtype))

        attn_weights = tf.nn.softmax(logits, axis=-1)  # (batch, num_heads, seq_len, seq_len)
        attn_output = tf.matmul(attn_weights, V)  # (batch, num_heads, seq_len, depth)

        # Concatenate heads:
        attn_output = tf.transpose(attn_output, perm=[0, 2, 1, 3])  # (batch, seq_len, num_heads, depth)
        concat_output = tf.reshape(attn_output, (batch_size, seq_len, self.d_model))  # (batch, seq_len, d_model)

        # Final linear projection:
        output = self.out_dense(concat_output)
        return output