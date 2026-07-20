import numpy as np
from scipy import ndimage



def detect_dark_spots(img):

    # تطبيع الصورة
    img = img.astype(float)

    # عتبة تكيفية
    threshold = np.percentile(img, 8)

    # استخراج المناطق الداكنة
    mask = img < threshold


    # تنظيف الضوضاء
    mask = ndimage.binary_opening(
        mask,
        iterations=2
    )


    # دمج المناطق القريبة
    mask = ndimage.binary_closing(
        mask,
        iterations=3
    )


    labels, count = ndimage.label(mask)


    if count == 0:

        return {

            "detected": False,

            "ratio":0,

            "area_pixels":0

        }



    sizes = ndimage.sum(
        mask,
        labels,
        range(1, count + 1)
    )


    # إزالة البقع الصغيرة جداً
    min_size = img.size * 0.0001


    valid = [
        s for s in sizes
        if s > min_size
    ]


    if len(valid) == 0:

        return {

            "detected":False,

            "ratio":0,

            "area_pixels":0

        }



    largest = np.argmax(sizes) + 1


    largest_mask = labels == largest


    area_pixels = int(
        sizes[largest-1]
    )


    ratio = (
        area_pixels /
        mask.size
    )


    cy, cx = ndimage.center_of_mass(
        largest_mask
    )



    return {


        "detected": True,


        "mask":largest_mask,


        "ratio":float(ratio),


        "center":(
            int(cx),
            int(cy)
        ),


        "area_pixels":area_pixels

    }




def risk_score(ratio):


    if ratio >= 0.05:

        return {
            "level":"HIGH",
            "score":90
        }


    elif ratio >=0.02:

        return {
            "level":"MEDIUM",
            "score":70
        }


    elif ratio >=0.005:

        return {
            "level":"LOW",
            "score":50
        }


    else:

        return {
            "level":"VERY LOW",
            "score":20
        }



def confidence(ratio):

    # ثقة تقريبية مبدئية

    value = min(
        95,
        50 + (ratio * 1000)
    )


    return round(value,2)
