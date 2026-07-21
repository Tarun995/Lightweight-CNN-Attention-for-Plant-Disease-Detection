import streamlit as st
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
import os
from utils.page_setup import inject_sidebar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Grad-CAM Interpretability - Plant Disease Detection",
    page_icon="👁️",
    layout="wide"
)

inject_sidebar()

# Custom css styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stApp {
    background: radial-gradient(circle at 50% 0%, #111e2e 0%, #0a111a 60%, #06090e 100%);
}

.header-container {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.header-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.header-desc {
    color: #94a3b8;
    font-size: 1.1rem;
}

.gradcam-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* ── Content Card ── */
.custom-content-card {
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.diagnosis-header-label {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    border-left: 4px solid #10b981;
    padding-left: 0.8rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">👁️ Grad-CAM Visual Interpretability</div>
    <div class="header-desc">Visualize what parts of the leaf the neural network is focusing on to make its disease predictions (using Gradient-weighted Class Activation Mapping).</div>
</div>
""", unsafe_allow_html=True)

# Imports from utils
from utils.model_loader import load_disease_models
from utils.disease_info import LABELS

# ─── Grad-CAM Algorithm Helpers ───────────────────────────────────────────────
def get_last_conv_layer_name(model):
    """
    Search the model layers backwards to find the last Conv2D layer name.
    """
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    # Fallback to name heuristics
    for layer in reversed(model.layers):
        if "conv" in layer.name.lower():
            return layer.name
    return None

@st.cache_resource
def get_grad_model(_model, last_conv_layer_name):
    last_conv_layer = _model.get_layer(last_conv_layer_name)
    return tf.keras.models.Model(
        _model.inputs, [last_conv_layer.output, _model.output]
    )

def compute_gradcam(img_array, model, last_conv_layer_name, pred_index=None):
    """
    Computes Grad-CAM activation map.
    """
    grad_model = get_grad_model(model, last_conv_layer_name)

    with tf.GradientTape() as tape:
        outputs = grad_model(img_array, training=False)
        last_conv_layer_output, preds = outputs[0], outputs[1]

        # Defensive unwrap: depending on how the .keras model's input/output
        # structure was saved, grad_model(...) can sometimes return each
        # output wrapped in a single-element list instead of a bare tensor.
        # Indexing a list with [:, i] throws "list indices must be integers
        # or slices, not tuple" -- so we normalize to tensors here before
        # doing any tensor-style slicing below.
        if isinstance(last_conv_layer_output, (list, tuple)):
            last_conv_layer_output = last_conv_layer_output[0]
        if isinstance(preds, (list, tuple)):
            preds = preds[0]

        last_conv_layer_output = tf.convert_to_tensor(last_conv_layer_output)
        preds = tf.convert_to_tensor(preds)

        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # Gradient of top class w.r.t last conv layer outputs
    grads = tape.gradient(class_channel, last_conv_layer_output)
    if grads is None:
        raise ValueError("Gradients could not be computed. Ensure the convolutional layer connects to the output.")

    # Pool gradients across channels
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Multiply each channel by its pooled gradient weight
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # ReLU and normalize
    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.math.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val
    else:
        heatmap = tf.zeros_like(heatmap)

    return heatmap.numpy()

def overlay_heatmap(heatmap, original_img, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap on original image using alpha blending.
    """
    # Rescale heatmap to 0-255 range
    heatmap_255 = np.uint8(255 * heatmap)

    # Apply colormap
    heatmap_color = cv2.applyColorMap(heatmap_255, colormap)

    # Resize heatmap to match original image
    heatmap_color_resized = cv2.resize(heatmap_color, (original_img.shape[1], original_img.shape[0]))

    # Convert colormap BGR to RGB
    heatmap_color_rgb = cv2.cvtColor(heatmap_color_resized, cv2.COLOR_BGR2RGB)

    # Blend images
    overlayed = cv2.addWeighted(original_img, 1 - alpha, heatmap_color_rgb, alpha, 0)
    return overlayed

# ─── Sidebar Controls ─────────────────────────────────────────────────────────
col_ctrl, col_display = st.columns([1, 2.2])

with col_ctrl:
    st.markdown('<div class="gradcam-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #f1f5f9; margin-top: 0;'>⚙️ Settings</h4>", unsafe_allow_html=True)
    crop = st.selectbox(
        "Select Crop Model",
        options=["potato", "tomato", "corn"],
        format_func=lambda x: x.capitalize()
    )

    uploaded_file = st.file_uploader(
        "Upload Leaf Image for Grad-CAM",
        type=["jpg", "png", "jpeg"]
    )

    alpha = st.slider("Heatmap Intensity (Alpha)", min_value=0.1, max_value=0.9, value=0.5, step=0.05)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="gradcam-card">
        <h5 style="color: #fbbf24; margin-top: 0; font-weight: 700;">💡 How to read Grad-CAM?</h5>
        <p style="font-size:0.85rem; color:#94a3b8; line-height:1.5; margin:0;">
            Red/orange regions signify the areas where the model placed the highest mathematical focus to predict the disease class. Green/blue areas represent low focus or background noise.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_display:
    if uploaded_file is not None:
        try:
            with st.spinner("Loading models..."):
                models = load_disease_models()
                model = models[crop]
        except Exception as ex:
            st.error(f"Error loading model: {ex}")
            st.stop()

        # Load image
        img = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(img)

        # Preprocess for model input size
        H, W = model.input_shape[1:3]
        img_resized = cv2.resize(img_np, (W, H))
        img_input = img_resized.astype("float32") / 255.0
        img_input = np.expand_dims(img_input, axis=0)

        # Predict class
        preds = model.predict(img_input, verbose=0)[0]
        pred_idx = np.argmax(preds)
        pred_class = LABELS[crop][pred_idx]
        confidence = float(preds[pred_idx]) * 100

        st.markdown(f'<div class="diagnosis-header-label">Predicted Label: <span style="color:#10b981;">{pred_class}</span> ({confidence:.2f}% Confidence)</div>', unsafe_allow_html=True)

        # Find last conv layer
        last_conv = get_last_conv_layer_name(model)

        if last_conv is None:
            st.warning("Could not identify convolutional layers in this model for Grad-CAM computation.")
        else:
            with st.spinner(f"Computing Grad-CAM using layer: {last_conv}..."):
                try:
                    heatmap = compute_gradcam(img_input, model, last_conv, pred_index=pred_idx)
                    overlay = overlay_heatmap(heatmap, img_resized, alpha=alpha)

                    # Layout images side by side
                    st.markdown('<div class="custom-content-card">', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.image(img_resized, caption="Resized Input Image", use_container_width=True)
                    c2.image(overlay, caption=f"Grad-CAM Heatmap overlay ({last_conv})", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Failed to generate Grad-CAM: {e}")
                    st.info("💡 Some custom model definitions do not expose their sub-layer tape structures. Showing prediction only.")
    else:
        st.info("👆 Upload an image in the left panel to trigger Grad-CAM activation visualization.")

        # Show sample Grad-CAM image if it exists
        sample_path = os.path.join(BASE_DIR, "results", "gradcam", "gradcam_potato.png")

        if os.path.exists(sample_path):
            st.markdown("<h3 style='font-size: 1.3rem; color: #f1f5f9; margin-top:2rem;'>Sample Grad-CAM Output</h3>", unsafe_allow_html=True)
            st.markdown('<div class="custom-content-card" style="display:inline-block;">', unsafe_allow_html=True)
            st.image(Image.open(sample_path), caption="Grad-CAM analysis highlighting Early Blight lesions on a potato leaf.", width=500)
            st.markdown('</div>', unsafe_allow_html=True)