import numpy as np


def detect_dark_spots(img, threshold=35):
    """
    كشف البقع الداكنة في صورة SAR.
    img : numpy array (Grayscale)
    """

    mask = img < threshold

    dark_pixels = int(mask.sum())
    total_pixels = mask.size

    ratio = dark_pixels / total_pixels

    return mask, ratio


def centroid(mask):
    """
    حساب مركز البقعة الداكنة.
    """

    ys, xs = np.where(mask)

    if len(xs) == 0:
        return None

    x = int(xs.mean())
    y = int(ys.mean())

    return x, y


def risk_score(ratio):

    if ratio > 0.06:
        return 90

    if ratio > 0.03:
        return 70

    if ratio > 0.015:
        return 55

    return 20
