import torch
import cv2
import numpy as np

def u2net_remove_background_from_numpy(net, image_np):
    """
    Remove background from leaf image numpy array using salient object detection (U2-Net).
    Returns masked image array.
    """
    # Resize and normalize for U2-Net model input (320x320)
    image = cv2.resize(image_np, (320, 320)) / 255.0
    image = image.transpose((2, 0, 1))  # HWC to CHW
    image = np.expand_dims(image, axis=0)
    image = torch.from_numpy(image).float()

    with torch.no_grad():
        d1, *_ = net(image)
        mask = d1[0][0].cpu().numpy()
        mask = cv2.resize(mask, (image_np.shape[1], image_np.shape[0]))
        # Normalize mask
        mask_min = mask.min()
        mask_max = mask.max()
        if mask_max - mask_min > 0:
            mask = (mask - mask_min) / (mask_max - mask_min)
        else:
            mask = np.zeros_like(mask)
        # Threshold mask to create a binary mask
        mask = (mask > 0.2).astype(np.uint8) * 255

    # Apply mask to image
    result = cv2.bitwise_and(image_np, image_np, mask=mask)
    return result
