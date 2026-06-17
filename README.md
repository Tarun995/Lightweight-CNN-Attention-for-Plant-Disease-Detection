# 🌿 Smart Plant Disease Detection System

A multi-stage deep learning pipeline combining YOLOv8 object detection, U²-Net background segmentation, and CNNs with custom Attention layers to diagnose plant leaf diseases with high precision.

---

## 🚀 Key Features
- **Leaf Localization**: YOLOv8 extracts leaf bounding boxes to crop extraneous background noise.
- **Salient Segmentation**: U²-Net computes pixel-wise saliency maps to isolate the leaf structure from soil, neighboring plants, or shadows.
- **Lesion Isolation**: YOLOv8 flags specific lesion hotspots to create a high-contrast binary mask input.
- **Attention-Augmented Classification**: Custom self-attention layers dynamically prioritize disease-bearing features during classification.
- **Model Explainability**: Integrated **Grad-CAM** visualizations highlight activation areas showing model decision-making.

---

## 📂 Project Structure
```
d:\Projects\PlantDiseaseDetection\
├── app.py                          ← Home/Landing page (Streamlit entrypoint)
├── pages/
│   ├── 2_Detection.py              ← Interactive image upload and pipeline diagnosis
│   ├── 3_Model_Analysis.py         ← Evaluation reports, confusion matrices
│   ├── 4_Research_Dashboard.py     ← Baseline CNN vs. Attention comparison
│   ├── 5_GradCAM.py                ← Grad-CAM interpretability heatmaps
│   └── 6_About.py                  ← Contributors, references, links
├── utils/
│   ├── __init__.py
│   ├── attention_layer.py          ← Canonical custom AttentionLayer serialization
│   ├── disease_info.py             ← Actionable guides, labels, links
│   ├── model_loader.py             ← Cached model loader (on-demand loading)
│   ├── pipeline.py                 ← Vision pipeline execution
│   └── u2net_bg_removal.py         ← U²-Net background extraction helper
├── models/
│   ├── disease/                    ← Potato, Tomato, Corn Keras models (gitignored)
│   ├── yolo/                       ← YOLO Leaf and Lesion weight files (gitignored)
│   └── u2net/                      ← U²-Net structure definition and weights (gitignored)
├── results/
│   ├── confusion_matrices/         ← Validation confusion matrix images
│   ├── evaluation/                 ← Model classification report CSV files
│   └── gradcam/                    ← Pre-computed sample Grad-CAM outputs
├── requirements.txt                ← Project dependencies
├── README.md                       ← This documentation file
└── .gitignore                      ← Ignores cache, virtual environments, and large models
```

---

## 📦 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/username/PlantDiseaseDetection.git
cd PlantDiseaseDetection
```

### 2. Configure Virtual Environment
We recommend using a clean virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Weights Setup

Model weight files (`.keras`, `.pth`, `.pt`) are large and hosted externally on Google Drive. Viewer access is enabled for public download.

**Google Drive Folder:**
https://drive.google.com/drive/folders/11f_gsqnwHH1Iq9WUzKZNqF8IJ3pRWoeR?usp=drive_link

**Quick Setup (Automated Download)**

1. Install `gdown` (if not already installed):
```bash
pip install gdown
```

2. Run the download script from the repository root:

**PowerShell:**
```powershell
.\scripts\download_weights_gdown.ps1
```

**Bash / macOS / Linux:**
```bash
bash scripts/download_weights_gdown.sh
```

The script will download all weights from Google Drive, organize them into `models/disease/`, `models/yolo/`, and `models/u2net/`, compute checksums, and optionally commit locally.

**Manual Download (via Google Drive UI)**

Alternatively, visit the Google Drive folder above, download the ZIP, and extract into the `models/` directory:
```
models/
├── disease/
│   ├── potato.keras
│   ├── tomato.keras
│   └── maize.keras
├── yolo/
│   ├── yolo_leaf_best.pt
│   └── yolo_lesion_best.pt
└── u2net/
    └── u2net.pth
```

See [WEIGHTS_URLS.md](WEIGHTS_URLS.md) for more details.

---

## 🖥️ Running the Application

Launch the Streamlit web interface locally:
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔬 Experimental Performance
Our attention-augmented models achieve substantial improvements over standard CNN baselines:

| Crop Model | Baseline CNN Accuracy | Proposed Attention CNN Accuracy | F1-Score |
|---|---|---|---|
| **Potato** | 82.4% | **90.4%** | **90.6%** |
| **Tomato** | 81.8% | **91.3%** | **91.0%** |
| **Corn** | 92.1% | **97.8%** | **97.6%** |
