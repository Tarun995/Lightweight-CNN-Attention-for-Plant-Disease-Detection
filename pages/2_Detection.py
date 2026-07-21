import streamlit as st
import numpy as np
from PIL import Image
import cv2
from utils.page_setup import inject_sidebar

st.set_page_config(
    page_title="Disease Detection - Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

inject_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: radial-gradient(ellipse at top, #0d1f2d 0%, #090e16 55%, #050810 100%);
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Page Header ── */
.page-hero {
    text-align: center;
    padding: 2.5rem 1rem 3rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 3rem;
}
.page-eyebrow {
    display: inline-block;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.72rem;
    font-weight: 700;
    color: #34d399;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.page-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 55%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.8rem;
}
.page-subtitle {
    font-size: 1.05rem;
    color: #64748b;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Step cards (upload area) ── */
.step-row {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 2.5rem;
    align-items: stretch;
}
.step-num {
    width: 28px;
    height: 28px;
    min-width: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: #fff;
    font-size: 0.8rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.6rem;
}

/* ── Cards ── */
.glass-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.glass-card-sm {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
}

/* ── Diagnosis banner ── */
.banner-healthy {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.04));
    border: 1px solid rgba(16,185,129,0.28);
    border-radius: 18px;
    padding: 2.2rem 2rem;
    text-align: center;
    box-shadow: 0 0 40px rgba(16,185,129,0.08);
    margin-bottom: 2.5rem;
}
.banner-infected {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.04));
    border: 1px solid rgba(239,68,68,0.28);
    border-radius: 18px;
    padding: 2.2rem 2rem;
    text-align: center;
    box-shadow: 0 0 40px rgba(239,68,68,0.08);
    margin-bottom: 2.5rem;
}
.banner-label {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    display: inline-block;
    margin-bottom: 1rem;
}
.banner-label-healthy { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.banner-label-infected { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.2); }
.banner-disease {
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0.4rem 0;
}
.banner-conf {
    font-size: 1rem;
    opacity: 0.75;
    margin-top: 0.3rem;
}

/* ── Image strip ── */
.img-caption {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: center;
    margin-top: 0.5rem;
}
.img-step-badge {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 6px;
    padding: 0.15rem 0.6rem;
    font-size: 0.68rem;
    font-weight: 700;
    color: #818cf8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.4rem;
}

/* ── Treatment boxes ── */
.treatment-box {
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    height: 100%;
}
.treatment-action {
    background: rgba(251,191,36,0.04);
    border: 1px solid rgba(251,191,36,0.14);
}
.treatment-context {
    background: rgba(99,102,241,0.04);
    border: 1px solid rgba(99,102,241,0.12);
}
.treatment-section-label {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.7rem;
}
.treatment-item {
    font-size: 0.87rem;
    color: #cbd5e1;
    margin-bottom: 0.5rem;
    padding-left: 0.3rem;
    display: flex;
    gap: 0.5rem;
}

/* ── CTA buttons ── */
.cta-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.8rem;
    flex-wrap: wrap;
}
.cta-btn {
    flex: 1;
    min-width: 180px;
    text-align: center;
    text-decoration: none;
    padding: 0.85rem 1.2rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.88rem;
    display: block;
    transition: opacity 0.2s;
}
.cta-btn:hover { opacity: 0.85; }
.cta-green { background: linear-gradient(135deg, #10b981, #059669); color: #fff; box-shadow: 0 4px 16px rgba(16,185,129,0.2); }
.cta-red   { background: linear-gradient(135deg, #ef4444, #dc2626); color: #fff; box-shadow: 0 4px 16px rgba(239,68,68,0.2); }

/* ── Crop type cards (pre-upload) ── */
.crop-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.25s ease;
    height: 100%;
    position: relative;
}
.crop-card:hover { border-color: rgba(16,185,129,0.25); transform: translateY(-3px); }
.crop-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    border-radius: 50px;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}
.b-potato { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); color: #f59e0b; }
.b-tomato { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); color: #ef4444; }
.b-corn   { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); color: #10b981; }

.crop-badge-experimental {
    position: absolute;
    top: 0.9rem;
    right: 0.9rem;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: #fbbf24;
    background: rgba(251, 191, 36, 0.12);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: 20px;
    padding: 0.2rem 0.55rem;
}

/* ── Section divider ── */
.section-divider {
    border: 0;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 2.5rem 0;
}

/* ── Upload area nudge ── */
.upload-nudge {
    background: rgba(16,185,129,0.04);
    border: 1px dashed rgba(16,185,129,0.2);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    color: #475569;
    font-size: 0.95rem;
}

/* ── Settings sidebar-style panel ── */
.settings-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
}
.settings-label {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #475569;
    margin-bottom: 0.5rem;
    display: block;
}

/* ── Experimental notice (corn) ── */
.experimental-note {
    background: rgba(251,191,36,0.06);
    border: 1px solid rgba(251,191,36,0.22);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    font-size: 0.8rem;
    color: #fbbf24;
    margin-top: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Imports ─────────────────────────────────────────────────────────────────
from utils.model_loader import load_yolo_leaf, load_yolo_lesion, load_u2net, load_disease_models
from utils.disease_info import LABELS, DISEASE_GUIDE, FERTILIZER_LINKS, PESTICIDE_LINKS
from utils.pipeline import detect_leaf, remove_background, detect_lesions, predict_disease

# ─── Page Hero ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">🔬 Multi-Stage Deep Learning</div>
    <div class="page-title">Crop Disease Diagnosis</div>
    <div class="page-subtitle">
        Upload a leaf image and our pipeline will localize the leaf, remove background clutter,
        isolate lesions, and classify the disease — all in under 2 seconds.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Guidance helper ─────────────────────────────────────────────────────────
def show_disease_guidance(crop, label):
    info = DISEASE_GUIDE.get(crop, {}).get(label, None)
    fert = FERTILIZER_LINKS.get(crop, "#")
    pest = PESTICIDE_LINKS.get(crop, "#")

    if info is None or label == "Healthy":
        st.markdown(f"""
        <div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.14);
                    border-radius:14px;padding:1.8rem;text-align:center;margin-top:0.5rem;">
            <div style="font-size:2rem;margin-bottom:0.6rem;">🌱</div>
            <h3 style="color:#34d399;margin:0 0 0.5rem;font-weight:700;font-size:1.2rem;">Plant is Healthy</h3>
            <p style="color:#64748b;margin:0 0 1.4rem;font-size:0.9rem;line-height:1.6;">
                No signs of active infection detected. Maintain current watering, nutrient, and spacing routines.
            </p>
            <a href="{fert}" target="_blank" style="background:#10b981;color:#fff;text-decoration:none;
               padding:0.65rem 1.4rem;border-radius:8px;font-weight:700;font-size:0.85rem;display:inline-block;">
                🌾 Browse Crop Nutrient Products
            </a>
        </div>
        """, unsafe_allow_html=True)
        return

    immediate_items = "".join([
        f"<div class='treatment-item'><span style='color:#fbbf24;'>⚡</span><span>{s}</span></div>"
        for s in info["Immediate"]
    ])
    causes_items = "".join([
        f"<div class='treatment-item'><span style='color:#f87171;'>🦠</span><span>{s}</span></div>"
        for s in info["Causes"]
    ])
    further_items = "".join([
        f"<div class='treatment-item'><span style='color:#818cf8;'>🛡️</span><span>{s}</span></div>"
        for s in info["Further"]
    ])

    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown(f"""
        <div class="treatment-box treatment-action">
            <div class="treatment-section-label" style="color:#fbbf24;">⚡ Immediate Actions</div>
            {immediate_items}
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="treatment-box treatment-context">
            <div class="treatment-section-label" style="color:#f87171;">🦠 Pathogen & Cause</div>
            {causes_items}
            <div class="treatment-section-label" style="color:#818cf8;margin-top:1.2rem;">🛡️ Long-term Prevention</div>
            {further_items}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cta-row">
        <a href="{fert}" target="_blank" class="cta-btn cta-green">🛒 Shop Fertilizers</a>
        <a href="{pest}" target="_blank" class="cta-btn cta-red">🧪 Shop Fungicides</a>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — CONFIGURE  +  STEP 2 — UPLOAD   (horizontal, equal-weight panels)
# ═══════════════════════════════════════════════════════════════════════════════
cfg_col, up_col = st.columns([1, 1], gap="large")

with cfg_col:
    st.markdown('<span class="settings-label">Step 1 · Configure</span>', unsafe_allow_html=True)
    with st.container(border=True):
        crop = st.selectbox(
            "🌾 Crop Type",
            options=["potato", "tomato", "corn"],
            format_func=lambda x: x.capitalize()
        )
        if crop == "corn":
            st.markdown("""
            <div class="experimental-note">
                ⚠️ <span>Corn detection is <b>experimental</b> — the model runs live, but hasn't
                been formally benchmarked yet. Treat predictions as indicative, not verified.</span>
            </div>
            """, unsafe_allow_html=True)
        st.divider()
        default_bg = (crop != "corn")
        bg_remove = st.checkbox(
            "Background Removal (U²-Net)",
            value=default_bg,
            help="Isolates the leaf from complex backgrounds using saliency maps."
        )
        use_lesion = st.checkbox(
            "Lesion Segmentation (YOLO)",
            value=False,
            disabled=not bg_remove,
            help="Detects and focuses on disease lesion regions within the leaf."
        )
        st.divider()
        confidence = st.slider(
            "Detection Confidence",
            min_value=0.05, max_value=0.9, value=0.15, step=0.05,
            help="Minimum confidence threshold for the YOLO leaf detector."
        )

with up_col:
    st.markdown('<span class="settings-label">Step 2 · Upload Image</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        f"Select a {crop.capitalize()} leaf image",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )
    if not uploaded_file:
        st.markdown("""
        <div class="upload-nudge">
            <div style="font-size:2.5rem;margin-bottom:0.7rem;">📷</div>
            <div style="font-weight:600;color:#475569;margin-bottom:0.3rem;">No image selected yet</div>
            <div style="font-size:0.85rem;">Supports JPG, PNG, JPEG · Use the uploader above</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show a thumbnail preview of the uploaded image
        preview = Image.open(uploaded_file).convert("RGB")
        st.image(preview, caption="Uploaded — ready to analyse", use_container_width=True)
        uploaded_file.seek(0)   # reset so numpy can read it later

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — ANALYSE  (only shows once an image is uploaded)
# ═══════════════════════════════════════════════════════════════════════════════
if uploaded_file is None:
    # Pretty placeholder cards
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.8rem;">
        <div style="font-size:0.7rem;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#334155;margin-bottom:0.4rem;">Supported crops</div>
        <div style="font-size:1.4rem;font-weight:700;color:#334155;">Upload an image above to begin analysis</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    crop_cards = [
        ("🥔", "Potato", "b-potato", "Solanum tuberosum",
         "3 disease classes: Early Blight, Late Blight, and Healthy specimens.", False),
        ("🍅", "Tomato", "b-tomato", "Solanum lycopersicum",
         "10 classes covering bacterial spots, viruses, molds, mites, and blights.", False),
        ("🌽", "Corn", "b-corn", "Zea mays",
         "4 classes: Gray Leaf Spot, Common Rust, Northern Blight, Healthy.", True),
    ]
    for col, (icon, name, badge_cls, sci, desc, experimental) in zip([c1, c2, c3], crop_cards):
        with col:
            exp_badge = '<div class="crop-badge-experimental">Experimental</div>' if experimental else ""
            st.markdown(f"""
            <div class="crop-card">
                {exp_badge}
                <div style="font-size:3rem;margin-bottom:0.8rem;">{icon}</div>
                <span class="crop-badge {badge_cls}">{name}</span>
                <div style="font-size:0.75rem;color:#475569;font-style:italic;margin:0.3rem 0 0.8rem;">{sci}</div>
                <div style="font-size:0.88rem;color:#64748b;line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Load models ──────────────────────────────────────────────────────────
    prog = st.progress(0, text="🔄 Loading neural network weights…")
    try:
        yolo_leaf = load_yolo_leaf()
        if bg_remove:
            u2net = load_u2net()
        if use_lesion:
            yolo_lesion = load_yolo_lesion()
        disease_models = load_disease_models()
        prog.progress(20, text="✅ Models loaded")
    except Exception as ex:
        prog.empty()
        st.error(f"Failed to load models: {ex}")
        st.stop()

    img_rgb = np.array(Image.open(uploaded_file).convert("RGB"))

    # ── Run pipeline ─────────────────────────────────────────────────────────
    try:
        prog.progress(30, text="🔍 Stage 1 / 4 — Leaf Detection (YOLOv8)…")
        box, leaf_overlay = detect_leaf(yolo_leaf, img_rgb, conf=confidence)

        classifier_input = img_rgb
        clean_rgb = None
        lesion_overlay_img = None
        found_lesions = False
        fallback = None

        if bg_remove:
            prog.progress(55, text="✂️ Stage 2 / 4 — Background Removal (U²-Net)…")
            clean_rgb = remove_background(u2net, img_rgb, box)
            classifier_input = clean_rgb

            if use_lesion:
                prog.progress(72, text="🔬 Stage 3 / 4 — Lesion Isolation (YOLOv8)…")
                found_lesions, lesion_overlay_img, lesion_masked, fallback = detect_lesions(
                    yolo_lesion, clean_rgb, conf=confidence
                )
                classifier_input = lesion_masked if found_lesions else fallback

        prog.progress(88, text="🧠 Stage 4 / 4 — Disease Classification…")
        model = disease_models[crop]
        idx, logits = predict_disease(model, classifier_input)
        disease_label = LABELS[crop][idx]
        confidence_score = float(logits[idx]) * 100

        prog.progress(100, text="✅ Analysis complete!")
        import time; time.sleep(0.4)
        prog.empty()

        # ── RESULT BANNER ────────────────────────────────────────────────────
        if disease_label == "Healthy":
            st.balloons()
            st.markdown(f"""
            <div class="banner-healthy">
                <span class="banner-label banner-label-healthy">{crop.capitalize()} · Healthy</span>
                <div class="banner-disease" style="color:#10b981;">🌱 {disease_label}</div>
                <div class="banner-conf" style="color:#a7f3d0;">
                    Diagnostic Confidence: <b>{confidence_score:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="banner-infected">
                <span class="banner-label banner-label-infected">{crop.capitalize()} · Infected</span>
                <div class="banner-disease" style="color:#ef4444;">🍂 {disease_label}</div>
                <div class="banner-conf" style="color:#fca5a5;">
                    Diagnostic Confidence: <b>{confidence_score:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if crop == "corn":
            st.markdown("""
            <div class="experimental-note" style="margin-top:-1.2rem;margin-bottom:1.8rem;">
                ⚠️ <span>This result is from an <b>experimental, unbenchmarked</b> corn model —
                treat it as a preview, not a verified diagnosis.</span>
            </div>
            """, unsafe_allow_html=True)

        # ── PIPELINE IMAGES (always shown, clean horizontal strip) ───────────
        st.markdown("""
        <div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;
                    letter-spacing:2px;color:#334155;margin-bottom:1rem;">
            Pipeline Stages
        </div>
        """, unsafe_allow_html=True)

        stages = [("1", "📸 Original", img_rgb),
                  ("2", "🔍 Leaf Detected", leaf_overlay)]
        if bg_remove and clean_rgb is not None:
            stages.append(("3", "✂️ Background Removed", clean_rgb))
        if use_lesion and lesion_overlay_img is not None:
            lbl = "🔬 Lesions Found" if found_lesions else "🔬 No Lesions"
            stages.append(("4", lbl, lesion_overlay_img if found_lesions else fallback))

        img_cols = st.columns(len(stages), gap="small")
        for col, (num, caption_text, img) in zip(img_cols, stages):
            with col:
                st.markdown(f"<div class='img-step-badge'>Step {num}</div>", unsafe_allow_html=True)
                st.image(img, use_container_width=True)
                st.markdown(f"<div class='img-caption'>{caption_text}</div>", unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # ── TREATMENT / GUIDANCE ─────────────────────────────────────────────
        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;
                        letter-spacing:2px;color:#334155;margin-bottom:0.4rem;">
                Agronomic Guidance
            </div>
            <div style="font-size:1.5rem;font-weight:800;color:#f1f5f9;">
                {'🌱 Care Recommendations' if disease_label == 'Healthy' else f'💊 Treatment — {disease_label}'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        show_disease_guidance(crop, disease_label)

    except Exception as e:
        prog.empty()
        st.error(f"Analysis error: {e}")
        st.info("💡 Make sure the image clearly shows a potato, tomato, or corn leaf.")