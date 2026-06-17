# Contributing

Thank you for your interest in contributing to PlantDiseaseDetection. A few notes to get started:

1. Model weights
   - Large weight files are excluded from the repository. Do NOT commit `.keras`, `.pt`, or `.pth` files.
   - Preferred: Use Git LFS to manage model weights. After installing Git LFS, run:

```
git lfs install
git lfs track "models/disease/*.keras"
git lfs track "models/yolo/*.pt"
git lfs track "models/u2net/*.pth"
```

   - Alternatively, host weights on a cloud storage (Google Drive, AWS S3) and add download links in `README.md`.

2. Development setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Running locally

```
streamlit run app.py
```

4. Code style & branches
   - Create a feature branch for changes: `git checkout -b feature/your-change`.
   - Open a pull request describing the change and include sample data or screenshots when relevant.

If you want, provide URLs for model weights and I'll add them to `README.md`.
