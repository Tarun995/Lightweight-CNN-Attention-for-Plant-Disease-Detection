# Weights — Google Drive Folder

All model weights are hosted in a single Google Drive folder (viewer access enabled for public download).

**Google Drive Folder:**
https://drive.google.com/drive/folders/11f_gsqnwHH1Iq9WUzKZNqF8IJ3pRWoeR?usp=drive_link

**Folder Contents:**
- potato.keras
- tomato.keras
- maize.keras
- yolo_leaf_best.pt
- yolo_lesion_best.pt
- u2net.pth

**How to Download**

Folder ID: `11f_gsqnwHH1Iq9WUzKZNqF8IJ3pRWoeR`

1. Install `gdown` (handles Google Drive downloads):
```bash
pip install gdown
```

2. From the repository root, run the download script:

**PowerShell:**
```powershell
.\scripts\download_weights_gdown.ps1
```

**Bash/macOS/Linux:**
```bash
bash scripts/download_weights_gdown.sh
```

The script will:
- Download all files from the Google Drive folder to `models/`.
- Organize them into subfolders (`models/disease/`, `models/yolo/`, `models/u2net/`).
- Compute SHA256 checksums to `models/checksums.txt`.
- Prompt you to commit locally (will NOT push).
