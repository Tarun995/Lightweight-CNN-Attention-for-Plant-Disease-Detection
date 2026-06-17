import cv2
import numpy as np
from utils.u2net_bg_removal import u2net_remove_background_from_numpy

def _bgr2rgb(img_bgr):
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def predict_disease(model, img_rgb):
    """
    Run disease prediction model on preprocessed RGB image.
    Returns predicted class index and logits.
    """
    H, W = model.input_shape[1:3]
    arr = cv2.resize(img_rgb, (W, H)).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    logits = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(logits))
    return idx, logits

def detect_leaf(yolo_leaf, img_rgb, conf=0.1):
    """
    Detect leaf bounding box using YOLO.
    Returns bounding box coordinates (x1, y1, x2, y2) and visual overlay image.
    """
    res = yolo_leaf(img_rgb, conf=conf, verbose=False)[0]
    overlay = _bgr2rgb(res.plot())
    if res.boxes is None or res.boxes.xyxy.shape[0] == 0:
        raise ValueError("No leaf detected. Please upload a clear leaf image.")
    # Use first detection as leaf ROI for cleaning
    x1, y1, x2, y2 = map(int, res.boxes.xyxy[0])
    h, w = img_rgb.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    return (x1, y1, x2, y2), overlay

def remove_background(u2net, img_rgb, box):
    """
    Crop leaf ROI and remove background using U2-Net.
    """
    x1, y1, x2, y2 = box
    cropped = img_rgb[y1:y2, x1:x2]
    clean = u2net_remove_background_from_numpy(u2net, cropped)  # RGB
    return clean

def detect_lesions(yolo_lesion, clean_rgb, conf=0.1):
    """
    Detect lesion regions in the background-removed leaf.
    Returns:
    - found (bool): whether lesions were detected
    - overlay (numpy array): visual YOLO detection overlay
    - masked (numpy array): image blacked out except in lesion boxes
    - clean_rgb (numpy array): raw input clean image
    """
    res = yolo_lesion(clean_rgb, conf=conf, verbose=False)[0]
    overlay = _bgr2rgb(res.plot())
    if res.boxes is None or res.boxes.xyxy.shape[0] == 0:
        # No lesions found; return clean image as fallback
        return False, overlay, clean_rgb, clean_rgb

    # Build a simple rectangular mask from detected boxes
    mask = np.zeros(clean_rgb.shape[:2], dtype=np.uint8)
    for xyxy in res.boxes.xyxy:
        x1, y1, x2, y2 = map(int, xyxy)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(clean_rgb.shape[1], x2), min(clean_rgb.shape[0], y2)
        mask[y1:y2, x1:x2] = 255
    masked = cv2.bitwise_and(clean_rgb, clean_rgb, mask=mask)
    return True, overlay, masked, clean_rgb
