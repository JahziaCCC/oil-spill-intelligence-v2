import numpy as np
from scipy import ndimage


def detect_dark_spots(img):

    # عتبة تكيفية بدلاً من رقم ثابت
    threshold = np.percentile(img, 8)

    mask = img < threshold

    # إزالة النقاط الصغيرة
    mask = ndimage.binary_opening(mask, iterations=2)

    # دمج الأجزاء القريبة
    mask = ndimage.binary_closing(mask, iterations=3)

    labels, count = ndimage.label(mask)

    if count == 0:
        return None

    sizes = ndimage.sum(mask, labels, range(1, count + 1))

    largest = np.argmax(sizes) + 1

    largest_mask = labels == largest

    area = int(sizes[largest - 1])

    ratio = area / mask.size

    cy, cx = ndimage.center_of_mass(largest_mask)

    return {
        "mask": largest_mask,
        "ratio": ratio,
        "center": (int(cx), int(cy)),
        "area": area,
    }


def risk_score(ratio):

    if ratio > 0.05:
        return 90

    if ratio > 0.02:
        return 70

    if ratio > 0.005:
        return 50

    return 20
