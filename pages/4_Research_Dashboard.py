import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Research Dashboard - Plant Disease Detection",
    page_icon="🔬",
    layout="wide"
)

# Custom dark design system styling
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
.research-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
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
st.markdown("### 🧬 Architecture Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="research-card">
        <h4>1. Baseline CNN Architecture</h4>
        <p style="font-size:0.9rem; color:#94a3b8;">Standard feed-forward Convolutional Neural Network used as the baseline comparison model.</p>
        <hr style="opacity:0.15;"/>
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
        <h4>2. Attention-Augmented CNN (Proposed)</h4>
        <p style="font-size:0.9rem; color:#94a3b8;">Our proposed model incorporating custom self-attention mechanisms over convolutional feature maps.</p>
        <hr style="opacity:0.15;"/>
        <ul>
            <li><b>Feature Extraction:</b> Convolutional layers capturing local leaf structures.</li>
            <li><b>Attention Block:</b> Custom <code>AttentionLayer</code> capturing non-local relationships.</li>
            <li><b>Mechanism:</b> Dynamic weights prioritize lesion hotspots while suppressing healthy tissue.</li>
            <li><b>Advantage:</b> Drastically improves precision on noisy backgrounds and small lesions.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ─── SECTION 2: Model Performance Comparisons ────────────────────────────────
st.markdown("### 📊 Performance Gains (Pure CNN vs. CNN + Attention)")

crop_sel = st.selectbox("Select Crop Model to Compare", ["Potato Model", "Tomato Model", "Corn Model"])

# Performance Data
data_map = {
    "Potato Model": {
        "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "cnn": [82.4, 83.1, 82.2, 82.6],
        "attention": [90.4, 92.7, 89.6, 90.6]
    },
    "Tomato Model": {
        "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "cnn": [81.8, 80.5, 81.2, 80.8],
        "attention": [91.3, 90.8, 91.3, 91.0]
    },
    "Corn Model": {
        "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "cnn": [92.1, 91.8, 92.0, 91.9],
        "attention": [97.8, 97.5, 97.8, 97.6]
    }
}

selected_data = data_map[crop_sel]
df_compare = pd.DataFrame({
    "Metric": selected_data["metrics"],
    "Baseline CNN": selected_data["cnn"],
    "CNN + Attention": selected_data["attention"]
}).set_index("Metric")

# Render comparison bar chart
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

x = np.arange(len(selected_data["metrics"]))
width = 0.35

rects1 = ax.bar(x - width/2, selected_data["cnn"], width, label='Baseline CNN', color='#4f46e5')
rects2 = ax.bar(x + width/2, selected_data["attention"], width, label='CNN + Attention', color='#22c55e')

ax.set_ylabel('Score (%)', color='#f1f5f9')
ax.set_title(f'Performance Comparison: {crop_sel}', color='#f1f5f9', fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(selected_data["metrics"], color='#f1f5f9')
ax.tick_params(colors='#f1f5f9')
ax.legend(facecolor='#0f172a', edgecolor='none', labelcolor='#f1f5f9')
ax.set_ylim(50, 105)

# Add value labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='#f1f5f9', fontsize=9)

autolabel(rects1)
autolabel(rects2)

# Grid lines styling
ax.yaxis.grid(True, linestyle='--', alpha=0.15, color='#94a3b8')

st.pyplot(fig)

# ─── SECTION 3: Dataset split breakdown ───────────────────────────────────────
st.markdown("### 📊 Dataset Distributions")
col_t1, col_t2 = st.columns([1.2, 1.8])

with col_t1:
    st.markdown("""
    <div class="research-card" style="height: 100%;">
        <h4>Image Database Summary</h4>
        <p style="font-size:0.9rem; color:#94a3b8;">Distribution of training, validation, and testing partitions extracted from the experimental datasets.</p>
        <hr style="opacity:0.15;"/>
        <table style="width:100%; border-collapse:collapse; color:#f1f5f9;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); font-weight:bold;">
                <td style="padding:8px 0;">Crop</td>
                <td style="padding:8px 0; text-align:right;">Train</td>
                <td style="padding:8px 0; text-align:right;">Val</td>
                <td style="padding:8px 0; text-align:right;">Test</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding:8px 0;">Potato</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">1,720</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">324</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">215</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding:8px 0;">Tomato</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">10,930</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">2,733</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">1,366</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding:8px 0;">Corn</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">3,852</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">480</td>
                <td style="padding:8px 0; text-align:right; color:#a7f3d0;">480</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_t2:
    # Render a pie chart showing total database share
    fig2, ax2 = plt.subplots(figsize=(7, 4.3))
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('none')
    
    sizes = [2259, 15029, 4812]
    labels = ['Potato Dataset', 'Tomato Dataset', 'Corn Dataset']
    colors = ['#f59e0b', '#ef4444', '#10b981']
    explode = (0, 0.05, 0)  # explode tomato (largest)
    
    wedges, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%1.1f%%', shadow=False, startangle=140,
                                      textprops=dict(color='#f1f5f9'))
    
    for autotext in autotexts:
        autotext.set_color('#1e293b')
        autotext.set_weight('bold')
        
    ax2.axis('equal')
    ax2.set_title("Proportion of Images by Crop Class in Global Database", color='#f1f5f9', pad=15)
    
    st.pyplot(fig2)
