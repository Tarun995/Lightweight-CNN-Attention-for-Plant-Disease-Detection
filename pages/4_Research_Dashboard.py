import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.page_setup import inject_sidebar

st.set_page_config(
    page_title="Research Dashboard - Plant Disease Detection",
    page_icon="🔬",
    layout="wide"
)

inject_sidebar()

# Custom dark design system styling
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

.research-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.research-card h4 {
    color: #f1f5f9;
    font-weight: 700;
    margin-top: 0;
    font-size: 1.2rem;
}
.research-card hr {
    border: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin: 1rem 0;
}
.research-card ul {
    padding-left: 1.2rem;
    margin: 0;
}
.research-card li {
    margin-bottom: 0.5rem;
    color: #cbd5e1;
    font-size: 0.9rem;
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">🔬 Research Dashboard</div>
    <div class="header-desc">Comparative analysis of baseline CNN vs. Attention-Augmented architectures, parameter distributions, and dataset statistics.</div>
</div>
""", unsafe_allow_html=True)

# ─── SECTION 1: Architecture Comparison ───────────────────────────────────────
st.markdown("<h3 style='color: #f1f5f9; font-weight: 700;'>🧬 Architecture Overview</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="research-card">
        <h4 style="border-left: 3px solid #4f46e5; padding-left: 0.6rem;">1. Baseline CNN Architecture</h4>
        <p style="font-size:0.9rem; color:#94a3b8; margin-bottom: 1rem;">Standard feed-forward Convolutional Neural Network used as the baseline comparison model.</p>
        <hr/>
        <ul>
            <li><b>Feature Extraction:</b> Alternating 2D Convolution and Max Pooling layers.</li>
            <li><b>Bottleneck:</b> Global Average Pooling or Flatten.</li>
            <li><b>Decision:</b> Dense layers culminating in a Softmax output.</li>
            <li><b>Limitation:</b> Lacks spatial discrimination; struggles with complex backgrounds.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="research-card">
        <h4 style="border-left: 3px solid #10b981; padding-left: 0.6rem;">2. Attention-Augmented CNN (Proposed)</h4>
        <p style="font-size:0.9rem; color:#94a3b8; margin-bottom: 1rem;">Our proposed model incorporating custom self-attention mechanisms over convolutional feature maps.</p>
        <hr/>
        <ul>
            <li><b>Feature Extraction:</b> Convolutional layers capturing local leaf structures.</li>
            <li><b>Attention Block:</b> Custom <code>AttentionLayer</code> capturing non-local relationships.</li>
            <li><b>Mechanism:</b> Dynamic weights prioritize lesion hotspots while suppressing healthy tissue.</li>
            <li><b>Advantage:</b> Drastically improves precision on noisy backgrounds and small lesions.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='custom-content-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #f1f5f9; font-weight: 700; margin-top:0;'>📊 Performance Gains (Pure CNN vs. CNN + Attention)</h3>", unsafe_allow_html=True)

crop_sel = st.selectbox("Select Crop Model to Compare", ["Potato Model", "Tomato Model"])

# Performance Data
data_map = {
    "Potato Model": {
        "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "cnn": [96.7, 95.2, 94.8, 95.0],
        "attention": [97.8, 96.5, 95.5, 96.0]
    },
    "Tomato Model": {
        "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "cnn": [86.0, 84.5, 85.0, 84.7],
        "attention": [78.9, 75.0, 72.0, 73.0]
    }
}

selected_data = data_map[crop_sel]

# Render comparison bar chart using modern dark matplotlib theme styles
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

x = np.arange(len(selected_data["metrics"]))
width = 0.35

rects1 = ax.bar(x - width/2, selected_data["cnn"], width, label='Baseline CNN', color='#4f46e5', edgecolor='none', alpha=0.9)
rects2 = ax.bar(x + width/2, selected_data["attention"], width, label='CNN + Attention', color='#10b981', edgecolor='none', alpha=0.9)

ax.set_ylabel('Score (%)', color='#94a3b8', fontsize=10)
ax.set_title(f'Performance Comparison: {crop_sel}', color='#f1f5f9', fontsize=12, pad=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(selected_data["metrics"], color='#cbd5e1', fontsize=9)
ax.tick_params(colors='#64748b')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color((1, 1, 1, 0.08))
ax.spines['bottom'].set_color((1, 1, 1, 0.08))
ax.legend(facecolor='#0f172a', edgecolor=(1, 1, 1, 0.1), labelcolor='#f1f5f9')
ax.set_ylim(50, 105)

# Add value labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', color='#f1f5f9', fontsize=8, fontweight='semibold')

autolabel(rects1)
autolabel(rects2)

# Grid lines styling
ax.yaxis.grid(True, linestyle='--', alpha=0.08, color='#ffffff')

st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# ─── SECTION 3: Dataset split breakdown ───────────────────────────────────────
st.markdown("<h3 style='color: #f1f5f9; font-weight: 700; margin-top: 2rem;'>📊 Dataset Distributions</h3>", unsafe_allow_html=True)
col_t1, col_t2 = st.columns([1.2, 1.8])

with col_t1:
    st.markdown("""
    <div class="research-card" style="height: 100%;">
        <h4 style="border-left: 3px solid #f59e0b; padding-left: 0.6rem;">Image Database Summary</h4>
        <p style="font-size:0.9rem; color:#94a3b8; margin-bottom: 1rem;">Distribution of training, validation, and testing partitions extracted from the experimental datasets.</p>
        <hr/>
        <table style="width:100%; border-collapse:collapse; color:#f1f5f9; font-size: 0.9rem;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06); font-weight:bold; color: #94a3b8;">
                <td style="padding:8px 0;">Crop</td>
                <td style="padding:8px 0; text-align:right;">Train</td>
                <td style="padding:8px 0; text-align:right;">Val</td>
                <td style="padding:8px 0; text-align:right;">Test</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                <td style="padding:8px 0; font-weight:600;">Potato</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">1,506</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">323</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">323</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                <td style="padding:8px 0; font-weight:600;">Tomato</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">12,712</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">2,724</td>
                <td style="padding:8px 0; text-align:right; color:#34d399;">2,724</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_t2:
    # Render a pie chart showing total database share
    fig2, ax2 = plt.subplots(figsize=(7, 4.3))
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('none')

    sizes = [2152, 18160]
    labels = ['Potato Dataset', 'Tomato Dataset']
    colors = ['#f59e0b', '#ef4444']

    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors,
                                       autopct='%1.1f%%', shadow=False, startangle=140,
                                       textprops=dict(color='#f1f5f9', fontsize=9))

    for autotext in autotexts:
        autotext.set_color('#0f172a')
        autotext.set_weight('bold')

    ax2.axis('equal')
    ax2.set_title("Proportion of Images by Crop Class in Global Database", color='#f1f5f9', pad=15, fontweight='bold', fontsize=12)

    st.pyplot(fig2)