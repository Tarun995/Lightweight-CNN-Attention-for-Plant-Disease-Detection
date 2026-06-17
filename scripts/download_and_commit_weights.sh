#!/usr/bin/env bash
set -euo pipefail

FOLDER_ID="11f_gsqnwHH1Iq9WUzKZNqF8IJ3pRWoeR"

echo "This script will download model weights from Google Drive, compute checksums, and prepare a local git commit (will NOT push)."

# Check if gdown is installed
if ! python -m pip show gdown > /dev/null 2>&1; then
  echo "gdown not found. Installing..."
  pip install gdown
fi

# Create model directories
mkdir -p models/disease models/yolo models/u2net

echo "Downloading files from Google Drive folder (ID: $FOLDER_ID)..."
python -m gdown --folder-id "$FOLDER_ID" --quiet

# Organize downloaded files into proper subfolders
if [ -d "$FOLDER_ID" ]; then
  echo "Organizing files into models/ subdirectories..."
  
  # Move files to appropriate subdirs based on extension/name patterns
  for file in "$FOLDER_ID"/*; do
    filename=$(basename "$file")
    case "$filename" in
      *.keras)
        mv "$file" "models/disease/$filename"
        ;;
      yolo_*)
        mv "$file" "models/yolo/$filename"
        ;;
      u2net*)
        mv "$file" "models/u2net/$filename"
        ;;
      *)
        echo "Warning: unknown file $filename, skipping."
        ;;
    esac
  done
  
  rm -rf "$FOLDER_ID"
fi

# Compute checksums
checksum_file="models/checksums.txt"
rm -f "$checksum_file"
for file in models/disease/* models/yolo/* models/u2net/*; do
  if [ -f "$file" ]; then
    sha256sum "$file" >> "$checksum_file"
  fi
done

echo "Checksums written to $checksum_file"

echo "Ensuring Git LFS is initialized and .gitattributes present..."
git lfs install || true

read -p "Files downloaded. Commit now? (y/N) " resp
if [[ "$resp" =~ ^[Yy]$ ]]; then
  git add models .gitattributes models/checksums.txt WEIGHTS_URLS.md
  git commit -m "Add model weights (via gdown) and checksums"
  echo "Committed locally. Run 'git push' when ready."
else
  echo "Skipped commit. Files are downloaded locally in 'models/'."
fi
