import streamlit as st

st.set_page_config(
    page_title="About - Plant Disease Detection",
    page_icon="ℹ️",
    layout="wide"
)

# Custom css styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1b2a 40%, #1b2838 100%);
}
.header-container {
    margin-bottom: 2.5rem;
}
.header-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 50%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.header-desc {
    color: #94a3b8;
    font-size: 1rem;
}
.about-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
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
        <h3>🔬 Project Overview</h3>
        <p style="color:#e2e8f0; line-height:1.6;">
            Early and precise detection of crop leaf diseases is vital to global food security, yield maximization, and eco-friendly farming. This system implements a multi-stage machine learning pipeline that goes beyond traditional end-to-end classifiers. By partitioning tasks into leaf localization, background segmentation, lesion isolation, and focus-augmented classification, we significantly boost diagnosis robustness in real-world environments.
        </p>
    </div>
    
    <div class="about-card">
        <h3>🛠️ Pipeline Stages Detail</h3>
        <ul style="color:#e2e8f0; line-height:1.7;">
            <li><b>Leaf Localization (YOLOv8):</b> Filters out heavy backgrounds and locates the primary leaf structure within the input image, generating a bounding box region of interest (ROI).</li>
            <li><b>Salient Background Removal (U²-Net):</b> Isolates the leaf from complex agricultural soil, shadows, or neighboring vegetation by computing pixel-wise saliency maps.</li>
            <li><b>Lesion Segmentation (YOLOv8):</b> Focuses specifically on lesion patterns, brown spots, and necrotic tissue to mask out healthy green segments of the leaf.</li>
            <li><b>Attention Classification (CNN + Self-Attention):</b> Evaluates the processed leaf crop using convolutional feature maps augmented with a custom tanh-based self-attention block to prioritize disease-bearing features.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="about-card">
        <h3>👥 Contributors</h3>
        <p style="font-weight:600; color:#fff; margin-bottom:0.2rem;">Lead Researcher & Developer</p>
        <p style="font-size:0.88rem; color:#94a3b8; margin-bottom:1rem;">Tarun </p>
        
        
    </div>
    
    <div class="about-card">
        <h3>🔗 Reference Links</h3>
        <ul style="padding-left:1.2rem; font-size:0.9rem; color:#22c55e;">
            <li style="margin-bottom:0.5rem;"><a href="https://github.com" target="_blank" style="color:#22c55e; text-decoration:none;">💻 GitHub Repository</a></li>
            <li style="margin-bottom:0.5rem;"><a href="https://arxiv.org" target="_blank" style="color:#22c55e; text-decoration:none;">📄 Research Paper (Pre-print)</a></li>
            <li style="margin-bottom:0.5rem;"><a href="https://pytorch.org" target="_blank" style="color:#22c55e; text-decoration:none;">🔥 PyTorch Backend</a></li>
            <li style="margin-bottom:0.5rem;"><a href="https://tensorflow.org" target="_blank" style="color:#22c55e; text-decoration:none;">🧠 TensorFlow Core</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
