import os
import streamlit as st
import tensorflow as tf
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from utils.attention_layer import AttentionLayer
import torch

# Constants for relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YOLO_LEAF_PATH = os.path.join(BASE_DIR, "models", "yolo", "yolo_leaf_best.pt")
YOLO_LESION_PATH = os.path.join(BASE_DIR, "models", "yolo", "yolo_lesion_best.pt")
U2NET_PATH = os.path.join(BASE_DIR, "models", "u2net", "u2net.pth")

DISEASE_MODEL_PATHS = {
    "potato": os.path.join(BASE_DIR, "models", "disease", "potato.keras"),
    "tomato": os.path.join(BASE_DIR, "models", "disease", "tomato.keras"),
    "corn":   os.path.join(BASE_DIR, "models", "disease", "maize.keras"),
}

@st.cache_resource(show_spinner="Loading YOLO Leaf Detector...")
def load_yolo_leaf():
    if not os.path.exists(YOLO_LEAF_PATH):
        raise FileNotFoundError(f"YOLO Leaf model weights not found at {YOLO_LEAF_PATH}")
    return YOLO(YOLO_LEAF_PATH)

@st.cache_resource(show_spinner="Loading YOLO Lesion Detector...")
def load_yolo_lesion():
    if not os.path.exists(YOLO_LESION_PATH):
        raise FileNotFoundError(f"YOLO Lesion model weights not found at {YOLO_LESION_PATH}")
    return YOLO(YOLO_LESION_PATH)

@st.cache_resource(show_spinner="Loading U²-Net Salient Background Remover...")
def load_u2net():
    if not os.path.exists(U2NET_PATH):
        raise FileNotFoundError(f"U²-Net model weights not found at {U2NET_PATH}")
    
    # Import U2NET from models/u2net/u2net.py
    from models.u2net.u2net import U2NET
    net = U2NET(3, 1)
    net.load_state_dict(torch.load(U2NET_PATH, map_location='cpu'))
    net.eval()
    return net

@st.cache_resource(show_spinner="Loading Keras Classification Models...")
def load_disease_models():
    models = {}
    for crop, path in DISEASE_MODEL_PATHS.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Disease model weights for {crop} not found at {path}")
        models[crop] = load_model(path, custom_objects={"AttentionLayer": AttentionLayer}, compile=False)
    return models
