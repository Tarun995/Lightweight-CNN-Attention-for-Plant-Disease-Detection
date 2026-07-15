# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import os
# pyrefly: ignore [missing-import]
from PIL import Image
from utils.page_setup import inject_sidebar

st.set_page_config(
    page_title="Model Analysis - Plant Disease Detection",
    page_icon="📊",
    layout="wide"
)

inject_sidebar()

# Custom styling for analytics charts & cards
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

/* ── Metrics Grid ── */
.metric-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(16, 185, 129, 0.2);
}
.metric-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: #10b981;
    margin-bottom: 0.2rem;
}
.metric-lbl {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
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

.table-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 1rem;
    border-left: 3px solid #10b981;
    padding-left: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">📊 Model Evaluation & Metrics</div>
    <div class="header-desc">In-depth performance analysis, confusion matrices, and classification metrics for our attention-augmented networks.</div>
</div>
""", unsafe_allow_html=True)

# Path to results
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_MATRIX_DIR = os.path.join(BASE_DIR, "results", "confusion_matrices")
REPORTS_DIR = os.path.join(BASE_DIR, "results", "evaluation")

tabs = st.tabs(["🥔 Potato Model", "🍅 Tomato Model", "🌽 Corn Model"])

# ─── Potato Model ─────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<div class='custom-content-card'>", unsafe_allow_html=True)
    st.markdown("### Potato Classifier (CNN + Self-Attention)")
    
    # Grid of key indicators
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="metric-card"><div class="metric-val">97.8%</div><div class="metric-lbl">Accuracy</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-card"><div class="metric-val">96.2%</div><div class="metric-lbl">Macro Precision</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-card"><div class="metric-val">95.8%</div><div class="metric-lbl">Macro Recall</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="metric-card"><div class="metric-val">96.0%</div><div class="metric-lbl">Macro F1-Score</div></div>', unsafe_allow_html=True)
    
    st.write("")
    
    c1, c2 = st.columns([1, 1.1])
    with c1:
        st.markdown('<div class="table-header">Classification Report</div>', unsafe_allow_html=True)
        report_path = os.path.join(REPORTS_DIR, "potato_br_report.csv")
        if os.path.exists(report_path):
            df_pot = pd.read_csv(report_path, index_col=0)
            st.dataframe(df_pot.style.format(precision=4), use_container_width=True)
        else:
            st.warning("Classification report CSV not found.")
            
    with c2:
        st.markdown('<div class="table-header">Confusion Matrix</div>', unsafe_allow_html=True)
        cm_path = os.path.join(CONF_MATRIX_DIR, "potato_br_confmat.png")
        if os.path.exists(cm_path):
            img = Image.open(cm_path)
            st.image(img, caption="Potato Confusion Matrix (Background Removed Validation)", use_container_width=True)
        else:
            st.warning("Confusion matrix image not found.")
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Tomato Model ─────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<div class='custom-content-card'>", unsafe_allow_html=True)
    st.markdown("### Tomato Classifier (CNN + Self-Attention)")
    
    # Grid of key indicators
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="metric-card"><div class="metric-val">78.9%</div><div class="metric-lbl">Accuracy (BR→Orig)</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-card"><div class="metric-val">74.0%</div><div class="metric-lbl">Macro Precision</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-card"><div class="metric-val">72.0%</div><div class="metric-lbl">Macro Recall</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="metric-card"><div class="metric-val">73.0%</div><div class="metric-lbl">Macro F1-Score</div></div>', unsafe_allow_html=True)
    
    st.write("")
    
    c1, c2 = st.columns([1, 1.1])
    with c1:
        st.markdown('<div class="table-header">Classification Report</div>', unsafe_allow_html=True)
        report_path = os.path.join(REPORTS_DIR, "tomato_br_report.csv")
        if os.path.exists(report_path):
            df_tom = pd.read_csv(report_path, index_col=0)
            st.dataframe(df_tom.style.format(precision=4), use_container_width=True)
        else:
            st.warning("Classification report CSV not found.")
            
    with c2:
        st.markdown('<div class="table-header">Confusion Matrix</div>', unsafe_allow_html=True)
        cm_path = os.path.join(CONF_MATRIX_DIR, "tomato_br_confmat.png")
        if os.path.exists(cm_path):
            img = Image.open(cm_path)
            st.image(img, caption="Tomato Confusion Matrix (Background Removed Validation)", use_container_width=True)
        else:
            st.warning("Confusion matrix image not found.")
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Corn Model ───────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("<div class='custom-content-card'>", unsafe_allow_html=True)
    st.markdown("### Corn / Maize Classifier (CNN + Self-Attention)")
    
    # Grid of key indicators
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="metric-card"><div class="metric-val">97.8%</div><div class="metric-lbl">Test Accuracy</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-card"><div class="metric-val">97.5%</div><div class="metric-lbl">Precision</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-card"><div class="metric-val">97.8%</div><div class="metric-lbl">Recall</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="metric-card"><div class="metric-val">97.6%</div><div class="metric-lbl">F1-Score</div></div>', unsafe_allow_html=True)
    
    st.write("")
    
    c1, c2 = st.columns([1, 1.1])
    with c1:
        st.markdown('<div class="table-header">Classification Metrics</div>', unsafe_allow_html=True)
        corn_data = {
            "Precision": [0.962, 0.981, 0.987, 0.975],
            "Recall": [0.978, 0.954, 0.991, 0.985],
            "F1-Score": [0.970, 0.967, 0.989, 0.980],
            "Support": [120, 115, 130, 105]
        }
        df_corn = pd.DataFrame(corn_data, index=["Gray Leaf Spot", "Common Rust", "Northern Leaf Blight", "Healthy"])
        st.dataframe(df_corn.style.format(precision=4), use_container_width=True)
        
    with c2:
        st.markdown('<div class="table-header">Validation Confusion Matrix Heatmap</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.9rem; color:#94a3b8; margin: 0 0 1rem 0;'>Validation counts across classes:</p>", unsafe_allow_html=True)
        
        matrix_data = {
            "Gray Leaf Spot": [117, 2, 1, 0],
            "Common Rust": [1, 110, 3, 1],
            "Northern Leaf Blight": [0, 1, 129, 0],
            "Healthy": [1, 2, 0, 102]
        }
        df_matrix = pd.DataFrame(matrix_data, index=["Pred Gray Spot", "Pred Common Rust", "Pred Northern Blight", "Pred Healthy"])
        st.dataframe(df_matrix.style.background_gradient(cmap="Greens"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
