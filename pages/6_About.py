import streamlit as st
from utils.page_setup import inject_sidebar

st.set_page_config(
    page_title="About - Plant Disease Detection",
    page_icon="ℹ️",
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

.about-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.about-card h3 {
    color: #f1f5f9;
    font-weight: 700;
    margin-top: 0;
    font-size: 1.30rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">ℹ️ About the Project</div>
    <div class="header-desc">Technical background, pipeline implementation details, and contributor information.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="about-card">
        <h3 style="border-left: 3px solid #10b981; padding-left: 0.6rem;">🔬 Project Overview</h3>
        <p style="color:#cbd5e1; line-height:1.7; font-size:0.95rem;">
            Early and precise detection of crop leaf diseases is vital to global food security, yield maximization, and eco-friendly farming. This system implements a multi-stage machine learning pipeline that goes beyond traditional end-to-end classifiers. By partitioning tasks into leaf localization, background segmentation, lesion isolation, and focus-augmented classification, we significantly boost diagnosis robustness in real-world environments.
        </p>
    </div>
    
    <div class="about-card">
        <h3 style="border-left: 3px solid #3b82f6; padding-left: 0.6rem;">🛠️ Pipeline Stages Detail</h3>
        <ul style="color:#cbd5e1; line-height:1.8; font-size:0.9rem; padding-left: 1.2rem;">
            <li style="margin-bottom:0.6rem;"><b>Leaf Localization (YOLOv8):</b> Filters out heavy backgrounds and locates the primary leaf structure within the input image, generating a bounding box region of interest (ROI).</li>
            <li style="margin-bottom:0.6rem;"><b>Salient Background Removal (U²-Net):</b> Isolates the leaf from complex agricultural soil, shadows, or neighboring vegetation by computing pixel-wise saliency maps.</li>
            <li style="margin-bottom:0.6rem;"><b>Lesion Segmentation (YOLOv8):</b> Focuses specifically on lesion patterns, brown spots, and necrotic tissue to mask out healthy green segments of the leaf.</li>
            <li style="margin-bottom:0.6rem;"><b>Attention Classification (CNN + Self-Attention):</b> Evaluates the processed leaf crop using convolutional feature maps augmented with a custom tanh-based self-attention block to prioritize disease-bearing features.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="about-card">
        <h3 style="border-left: 3px solid #fbbf24; padding-left: 0.6rem;">👥 Contributors</h3>
        <p style="font-weight:700; color:#fff; margin-bottom:0.2rem; font-size: 0.95rem;">Lead Researcher & Developer</p>
        <p style="font-size:0.9rem; color:#94a3b8; margin-bottom:1rem;">Tarun </p>
    </div>
    
    <div class="about-card">
        <h3 style="border-left: 3px solid #ec4899; padding-left: 0.6rem;">🔗 Reference Links</h3>
        <ul style="padding-left:1.2rem; font-size:0.9rem; color:#10b981; list-style-type: square;">
            <li style="margin-bottom:0.5rem;"><a href="https://github.com/Tarun995/Lightweight-CNN-Attention-for-Plant-Disease-Detection" target="_blank" style="color:#10b981; text-decoration:none; font-weight:600;">💻 GitHub Repository</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
