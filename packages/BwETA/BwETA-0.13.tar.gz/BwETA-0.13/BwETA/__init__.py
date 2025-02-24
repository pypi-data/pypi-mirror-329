import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from tensorflow.keras.models import model_from_json
from huggingface_hub import hf_hub_download
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model import *

def load_local(path):
    with open(f'{path}/model_config.json', 'r') as f:
        config = json.load(f)
        config = config["config"]
    try:
        name = config["name"]
    except:
        name = "transformer_model"
    model = TransformerModel(name,config["num_heads"],config["attention_dim"],config["vocab_size"],config["num_blocks"],config["ff_dim"],config["dropout_rate"])
    model.build_custom()
    model.load_weights(f'{path}/tf_model.h5')
    return model

def load_hf(path):
    model_repo = path
    filenames = ["model_config.json","tf_model.h5"]
    for i in filenames:
        print(hf_hub_download(repo_id=model_repo, filename=i,local_dir="Loaded_model"))
    return load_local("Loaded_model")
