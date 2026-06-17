import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Set page config
st.set_page_config(
    page_title="Disease Detection - Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1b2a 40%, #1b2838 100%);
}
.section-header {
    margin-bottom: 2rem;
}
.section-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 50%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.section-desc {
    color: #94a3b8;
    font-size: 1rem;
}
.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <div class="section-title">🌿 Crop Disease Diagnosis</div>
    <div class="section-desc">Upload a crop leaf image to identify diseases using our multi-stage deep learning pipeline.</div>
</div>
""", unsafe_allow_html=True)

# Imports from utils
from utils.model_loader import load_yolo_leaf, load_yolo_lesion, load_u2net, load_disease_models
from utils.disease_info import LABELS, DISEASE_GUIDE, FERTILIZER_LINKS, PESTICIDE_LINKS
from utils.pipeline import detect_leaf, remove_background, detect_lesions, predict_disease

# Guidance presentation block helper
def show_disease_guidance(crop, label):
    info = DISEASE_GUIDE.get(crop, {}).get(label, None)
    fert = FERTILIZER_LINKS.get(crop, "#")
    pest = PESTICIDE_LINKS.get(crop, "#")
    
    if info is None or label == "Healthy":
        st.success("🎉 Plant appears to be healthy! Maintain regular watering and soil management.")
        st.markdown(f"🛍️ **Resources:** [Fertilizer Recommendations]({fert})")
        return
        
    st.markdown(f"### 📋 Actionable Guidance for **{label}**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ⚡ Immediate Actions")
        for step in info["Immediate"]:
            st.markdown(f"- {step}")
        st.markdown("#### 🔜 Long-term Prevention")
        for step in info["Further"]:
            st.markdown(f"- {step}")
    with col2:
        st.markdown("#### 🧩 Primary Causes")
        for cause in info["Causes"]:
            st.markdown(f"- {cause}")
        st.markdown("#### 🛒 Treatment & Products")
        st.markdown(f"💊 [Shop Specific Fertilizer]({fert})")
        st.markdown(f"🧪 [Search Safe Fungicides/Pesticides]({pest})")

# Columns for controls and uploading
col_ctrl, col_display = st.columns([1, 2])

with col_ctrl:
    st.markdown("### ⚙️ Diagnosis Settings", unsafe_allow_html=True)
    
    # 1. Crop Selection
    crop = st.selectbox(
        "Select Crop Type",
        options=["potato", "tomato", "corn"],
        format_func=lambda x: x.capitalize()
    )
    
    # 2. File Uploader
    uploaded_file = st.file_uploader(
        f"Upload a {crop.capitalize()} Leaf Image",
        type=["jpg", "png", "jpeg"]
    )
    
    # 3. Pipeline controls
    st.markdown("#### Pipeline Toggles")
    default_bg = (crop != "corn")
    bg_remove = st.checkbox("Enable Background Removal (U²-Net)", value=default_bg)
    use_lesion = st.checkbox(
        "Enable Lesion Segmentation (YOLO)",
        value=False,
        disabled=not bg_remove,
        help="Runs lesion localization on the background-removed leaf ROI to mask out healthy parts."
    )
    
    confidence = st.slider("Detector Confidence Threshold", min_value=0.05, max_value=0.9, value=0.15, step=0.05)

with col_display:
    if uploaded_file is not None:
        st.markdown("### 🔍 Analysis Progress")
        
        # Load models
        try:
            with st.spinner("Initializing Models..."):
                yolo_leaf = load_yolo_leaf()
                if bg_remove:
                    u2net = load_u2net()
                if use_lesion:
                    yolo_lesion = load_yolo_lesion()
                disease_models = load_disease_models()
        except Exception as ex:
            st.error(f"Failed to load models: {ex}")
            st.stop()
            
        # Convert uploaded file to numpy RGB
        img_rgb = np.array(Image.open(uploaded_file).convert("RGB"))
        
        # Run Pipeline
        try:
            # Step 1: Leaf Detection
            with st.spinner("Stage 1/4: Running Leaf Detection (YOLOv8)..."):
                box, leaf_overlay = detect_leaf(yolo_leaf, img_rgb, conf=confidence)
            
            # Show original and Leaf Detection result
            c1, c2 = st.columns(2)
            c1.image(img_rgb, caption="Original Image", use_container_width=True)
            c2.image(leaf_overlay, caption="Leaf Detection ROI", use_container_width=True)
            
            # Step 2: Background Removal
            classifier_input = img_rgb
            if bg_remove:
                with st.spinner("Stage 2/4: Segementing Leaf Background (U²-Net)..."):
                    clean_rgb = remove_background(u2net, img_rgb, box)
                
                # Step 3: Lesion Detection
                if use_lesion:
                    with st.spinner("Stage 3/4: Isolating Lesions (YOLOv8)..."):
                        found, lesion_overlay, lesion_masked, fallback = detect_lesions(yolo_lesion, clean_rgb, conf=confidence)
                    
                    c3, c4 = st.columns(2)
                    c3.image(lesion_overlay, caption="Lesion Hotspots Detected", use_container_width=True)
                    if found:
                        c4.image(lesion_masked, caption="Lesion Focused (Model Input)", use_container_width=True)
                        classifier_input = lesion_masked
                    else:
                        c4.image(fallback, caption="No Lesions Found (Clean Input)", use_container_width=True)
                        classifier_input = fallback
                else:
                    st.image(clean_rgb, caption="Segmented Leaf", width=400)
                    classifier_input = clean_rgb
            
            # Step 4: Disease Prediction
            with st.spinner("Stage 4/4: Predicting Disease Class..."):
                model = disease_models[crop]
                idx, logits = predict_disease(model, classifier_input)
                disease_label = LABELS[crop][idx]
                confidence_score = float(logits[idx]) * 100
                
            # Final diagnosis header
            st.markdown("---")
            if disease_label == "Healthy":
                st.balloons()
                st.success(f"🌱 Diagnosis: **Healthy** (Confidence: {confidence_score:.2f}%)")
            else:
                st.error(f"🍂 Diagnosis: **{disease_label}** (Confidence: {confidence_score:.2f}%)")
                
            # Recommendations and Actionable items
            st.markdown('<div class="card">', unsafe_allow_html=True)
            show_disease_guidance(crop, disease_label)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            st.info("💡 Tip: Make sure the uploaded image clearly contains a potato, tomato, or corn leaf.")
            
    else:
        # Pre-upload view
        st.info("👆 Please upload a crop leaf image in the left panel to begin diagnosis.")
        
        # Show sample crop placeholders
        st.markdown("### Expected Leaf Types")
        c1, c2, c3 = st.columns(3)
        c1.markdown("#### 🥔 Potato Leaves")
        c1.caption("Early Blight, Late Blight, or Healthy leaf specimens.")
        c2.markdown("#### 🍅 Tomato Leaves")
        c2.caption("9 distinct bacterial/fungal/viral disease classes.")
        c3.markdown("#### 🌽 Corn Leaves")
        c3.caption("Gray Spot, Rust, Blight, or Healthy leaves.")
