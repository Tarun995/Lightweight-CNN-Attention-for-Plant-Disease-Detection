# pyrefly: ignore [missing-import]
import streamlit as st
from utils.page_setup import inject_sidebar

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_sidebar()

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stApp {
    background: radial-gradient(circle at 50% 0%, #111e2e 0%, #0a111a 60%, #06090e 100%);
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* ── Hero Section ── */
.hero-container {
    text-align: center;
    padding: 4rem 2rem 3rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.08));
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 50px;
    padding: 0.4rem 1.2rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #34d399;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.hero-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    max-width: 700px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
    font-weight: 400;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin: 0 auto 3rem;
}
.metric-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.8rem 1.4rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card:nth-child(1)::before { background: linear-gradient(90deg, #10b981, #059669); }
.metric-card:nth-child(2)::before { background: linear-gradient(90deg, #3b82f6, #6366f1); }
.metric-card:nth-child(3)::before { background: linear-gradient(90deg, #f59e0b, #d97706); }
.metric-card:nth-child(4)::before { background: linear-gradient(90deg, #8b5cf6, #ec4899); }

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.35);
}
.metric-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}

/* ── Section Headers ── */
.section-header {
    text-align: center;
    margin-bottom: 2.5rem;
}
.section-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #10b981;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.6rem;
}
.section-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}
.section-desc {
    font-size: 1rem;
    color: #64748b;
    max-width: 550px;
    margin: 0 auto;
}

/* ── Pipeline Steps ── */
.pipeline-container {
    display: flex;
    align-items: stretch;
    gap: 0;
    margin: 0 auto 3.5rem;
    position: relative;
    justify-content: center;
}
.pipeline-step {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    flex: 1;
    max-width: 180px;
    transition: all 0.3s ease;
    position: relative;
}
.pipeline-step:hover {
    transform: translateY(-3px);
    border-color: rgba(16, 185, 129, 0.3);
    box-shadow: 0 12px 30px rgba(16, 185, 129, 0.08);
}
.pipeline-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: #fff;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.pipeline-icon {
    font-size: 1.8rem;
    margin-bottom: 0.6rem;
}
.pipeline-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.4;
}
.pipeline-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #10b981;
    font-size: 1.5rem;
    padding: 0 0.4rem;
    opacity: 0.5;
}

/* ── Crop Cards ── */
.crop-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
    margin: 0 auto 3rem;
}
.crop-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}
.crop-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}
.crop-card:nth-child(1):hover { border-color: rgba(245, 158, 11, 0.35); }
.crop-card:nth-child(2):hover { border-color: rgba(239, 68, 68, 0.35); }
.crop-card:nth-child(3):hover { border-color: rgba(16, 185, 129, 0.35); }

.crop-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
.crop-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
}
.crop-diseases {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 500;
}

/* ── Tech Stack Section ── */
.tech-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 0 auto 3.5rem;
}
.tech-item {
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
}
.tech-item:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
}
.tech-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.2rem;
}
.tech-desc {
    font-size: 0.72rem;
    color: #64748b;
}

/* ── Footer ── */
.custom-footer {
    text-align: center;
    padding: 2rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    margin-top: 2rem;
}
.footer-text {
    font-size: 0.85rem;
    color: #475569;
    font-weight: 500;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .hero-title { font-size: 2.2rem; }
    .metric-grid { grid-template-columns: repeat(2, 1fr); }
    .pipeline-container { flex-direction: column; align-items: center; }
    .pipeline-arrow { transform: rotate(90deg); }
    .crop-grid { grid-template-columns: 1fr; }
    .tech-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🔬 Deep Learning for Agriculture</div>
    <div class="hero-title">Smart Plant Disease<br>Detection System</div>
    <div class="hero-subtitle">
        A multi-stage deep learning pipeline combining YOLOv8 detection,
        U²-Net segmentation, and CNN with Attention mechanisms for
        accurate crop disease classification.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Metric Cards ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-value">97.8%</div>
        <div class="metric-label">Best Accuracy</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🌾</div>
        <div class="metric-value">3</div>
        <div class="metric-label">Supported Crops</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🧬</div>
        <div class="metric-value">4</div>
        <div class="metric-label">ML Models</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">&lt;2s</div>
        <div class="metric-label">Inference Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Detection Pipeline ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-tag">How It Works</div>
    <div class="section-title">Detection Pipeline</div>
    <div class="section-desc">From raw input image to accurate disease prediction in five processing stages</div>
</div>

<div class="pipeline-container">
    <div class="pipeline-step">
        <div class="pipeline-num">1</div>
        <div class="pipeline-icon">📸</div>
        <div class="pipeline-title">Input Image</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">2</div>
        <div class="pipeline-icon">🔍</div>
        <div class="pipeline-title">YOLOv8 Leaf Detection</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">3</div>
        <div class="pipeline-icon">✂️</div>
        <div class="pipeline-title">U²-Net Background Removal</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">4</div>
        <div class="pipeline-icon">🔬</div>
        <div class="pipeline-title">Lesion Detection</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">5</div>
        <div class="pipeline-icon">🧠</div>
        <div class="pipeline-title">CNN + Attention Classification</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Supported Crops ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-tag">Supported Crops</div>
    <div class="section-title">What We Can Detect</div>
    <div class="section-desc">Specialized models trained on high-quality datasets for each crop type</div>
</div>

<div class="crop-grid">
    <div class="crop-card">
        <div class="crop-icon">🥔</div>
        <div class="crop-name">Potato</div>
        <div class="crop-diseases">Early Blight · Late Blight · Healthy</div>
    </div>
    <div class="crop-card">
        <div class="crop-icon">🍅</div>
        <div class="crop-name">Tomato</div>
        <div class="crop-diseases">Bacterial Spot · Late Blight · Leaf Mold · +7 more</div>
    </div>
    <div class="crop-card">
        <div class="crop-icon">🌽</div>
        <div class="crop-name">Corn</div>
        <div class="crop-diseases">Gray Leaf Spot · Common Rust · Blight · Healthy</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tech Stack ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-tag">Technology Stack</div>
    <div class="section-title">Built With</div>
</div>

<div class="tech-grid">
    <div class="tech-item">
        <div class="tech-name">YOLOv8</div>
        <div class="tech-desc">Object Detection</div>
    </div>
    <div class="tech-item">
        <div class="tech-name">U²-Net</div>
        <div class="tech-desc">Salient Object Segmentation</div>
    </div>
    <div class="tech-item">
        <div class="tech-name">TensorFlow / Keras</div>
        <div class="tech-desc">CNN + Attention Model</div>
    </div>
    <div class="tech-item">
        <div class="tech-name">Streamlit</div>
        <div class="tech-desc">Interactive Web UI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="custom-footer">
    <div class="footer-text">
        🌿 Smart Plant Disease Detection System · Powered by Deep Learning
    </div>
</div>
""", unsafe_allow_html=True)
