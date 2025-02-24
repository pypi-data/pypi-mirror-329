#@title Model everything
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
class PositionalEncoding(layers.Layer):
    def __init__(self, embedding_dim):
        super(PositionalEncoding, self).__init__()
        self.embedding_dim = embedding_dim

    def call(self, inputs):
        # Get the sequence length dynamically from the input shape
        sequence_length = tf.shape(inputs)[1]  # shape = (batch_size, sequence_length, embedding_dim)

        # Generate positional encoding for the dynamic sequence length
        position = tf.range(sequence_length, dtype=tf.float32)[:, tf.newaxis]
        div_term = tf.exp(tf.range(0, self.embedding_dim, 2, dtype=tf.float32) * -(tf.math.log(10000.0) / self.embedding_dim))

        # Calculate sine and cosine for each dimension
        sin_values = tf.sin(position * div_term)
        cos_values = tf.cos(position * div_term)

        # Concatenate sine and cosine values
        pos_enc = tf.concat([sin_values, cos_values], axis=-1)

        # Ensure the positional encoding has the same batch size as the input
        pos_enc = tf.expand_dims(pos_enc, 0)  # Expand batch dimension (1, sequence_length, embedding_dim)
        return inputs + pos_enc  # Add positional encoding to input

    def get_positional_encoding(attention_dim):
        # Your implementation of the positional encoding
        return PositionalEncoding(attention_dim)

class TransformerBlock(layers.Layer):
    def __init__(self, num_heads, attention_dim, ff_dim=512, dropout_rate=0.1,**kwargs):
        super(TransformerBlock, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.attention_dim = attention_dim
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate

        # Multi-Head Attention Layer
        self.attention = layers.MultiHeadSelfAttention(num_heads=num_heads, key_dim=attention_dim)

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
        attn_output = self.attention(inputs, inputs, inputs, attention_mask=mask)
        attn_output = self.dropout1(attn_output)
        out1 = self.norm1(inputs + attn_output)  # Add & Norm

        # Apply Feed-Forward Network
        ffn_output = self.ffn1(out1)
        ffn_output = self.ffn2(ffn_output)
        ffn_output = self.dropout2(ffn_output)
        out2 = self.norm2(out1 + ffn_output)  # Add & Norm

        return out2

class TransformerModel(tf.keras.Model):
    def __init__(self, num_heads=8, attention_dim=512, vocab_size=5027,num_blocks=24, ff_dim=4096, dropout_rate=0.2,**kwargs):
        kwargs.pop('name', None)
        kwargs.pop('trainable', None)
        kwargs.pop('dtype', None)
        super(TransformerModel, self).__init__(**kwargs)
        self.num_heads = num_heads
        self.attention_dim = attention_dim
        self.vocab_size = vocab_size
        self.num_blocks = num_blocks
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=attention_dim)
        self.positional_encoding = PositionalEncoding(attention_dim)
        self.blocks = [TransformerBlock(num_heads, attention_dim, ff_dim, dropout_rate) for _ in range(num_blocks)]
        self.final_layer = layers.Dense(vocab_size)  # Output layer for classification (adjust output size accordingly)

    def call(self, inputs,attention_mask = None,labels = None):
        class CustomModelOutput():
            def __init__(self,loss,logits):
                self.loss = loss
                self.logits = logits

        # All the input data checking is being done here---
        try:
            mask = inputs["attention_mask"]  # If needed for masking
            input = inputs["input_ids"]
        except Exception:
            input = inputs
            if attention_mask == None:
                if len(input.shape) == 2:
                    input_len = input.shape[1]
                    batch_size = input.shape[0]
                elif len(input.shape) == 1:
                    input_len = input.shape[0]
                    batch_size = 1
                mask = tf.ones((batch_size,input_len))
            else:
                mask = attention_mask

        #Here everything is getting casted---
        mask = tf.cast(mask, tf.int32)
        input = tf.cast(input, tf.int32)

        #Here we calculate the mask for the inputted Mask
        mask_sq = self.process_mask(mask)

        # This is the place for the layer and blocks to run--
        x = self.embedding(input)
        x = x + self.positional_encoding(x)
        # Only pass the mask to blocks if it's not None
        for block in self.blocks:
            x = block(x, mask=mask_sq)  # Pass through each transformer block
        logits =  self.final_layer(x)

        if labels == None:
            return CustomModelOutput(None,logits)
        else:
            labels = labels[:, 1:]
            return CustomModelOutput(self.loss_fn(labels,logits[:, :-1, :]),logits)

    def process_mask(self,mask):
        batch_size = mask.shape[0]
        seq_len = mask.shape[1]
        mask_sq = tf.linalg.band_part(tf.ones((batch_size,seq_len,seq_len), dtype=tf.int32), -1, 0)
        mask = tf.reshape(mask, (batch_size,1,seq_len))
        mask_sq = mask_sq * mask
        mask_sq = tf.transpose(mask_sq, perm=[0, 2, 1])
        mask_sq = mask_sq * mask
        mask_sq = tf.transpose(mask_sq, perm=[0, 2, 1])
        return mask_sq

    def generate(self, input, max_len, mask=None):
        try:
            input = input["input_ids"]
            input = tf.constant(input, dtype=tf.int32)
        except:
            input = tf.constant(input, dtype=tf.int32)
        for _ in range(max_len):
            output = self(input, mask)
            probs = tf.nn.softmax(output.logits, axis=-1)
            predicted_id = tf.argmax(probs[:, -1, :], axis=-1).numpy().flatten()

            # Reshape predicted_id to match the batch size for concatenation
            predicted_id = tf.expand_dims(predicted_id, axis=1)  # Shape: (batch_size, 1)
            predicted_id = tf.cast(predicted_id,dtype=tf.int32)
            # Concatenate along the sequence length axis (axis=1)
            input = tf.concat([input, predicted_id], axis=1)

        return input.numpy().flatten()

    def save_pretrained(self,path):
            self.save(f'{path}/tf_model.h5')
            with open(f'{path}/model_config.json', 'w') as f:
                f.write(self.to_json())

    def build_custom(self):
        input_ids = tf.random.uniform([1, 2], maxval=50257, dtype=tf.int32)
        attention_mask = tf.ones([1, 2], dtype=tf.int32)
        input_data = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
        self(input_data,labels=input_data['input_ids'])

    def get_config(self):
        config = super(TransformerModel, self).get_config()
        config.update({
            "num_heads": self.num_heads,
            "attention_dim": self.attention_dim,
            "vocab_size": self.vocab_size,
            "num_blocks": self.num_blocks,
            "ff_dim": self.ff_dim,
            "dropout_rate": self.dropout_rate
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)

from tensorflow.keras.models import model_from_json
from huggingface_hub import hf_hub_download
import json

def load_local(path):
    with open(f'{path}/model_config.json', 'r') as f:
        config = json.load(f)
        config = config["config"]
    model = TransformerModel(config["num_heads"],config["attention_dim"],config["vocab_size"],config["num_blocks"],config["ff_dim"],config["dropout_rate"])
    model.build_custom()
    model.load_weights(f'{path}/tf_model.h5')
    return model

def load_hf(path):
    model_repo = path
    filenames = ["model_config.json","tf_model.h5"]
    for i in filenames:
        print(hf_hub_download(repo_id=model_repo, filename=i,local_dir="Loaded_model"))