import cv2
import numpy as np

def enhance_image(image, denoise=False, contrast=False, skew_correction=False):

    if image is None:
        raise ValueError("Invalid image input: NoneType received.")

    if contrast:
        brightness = 50
        contrast_value = 80
        img = np.int16(image)
        img = img * (contrast_value / 127 + 1) - contrast_value + brightness
        image = np.clip(img, 0, 255).astype(np.uint8)

    if denoise:
        image = cv2.GaussianBlur(image, (3, 3), 0)

    return image
