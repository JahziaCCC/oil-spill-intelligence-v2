import numpy as np
from scipy import ndimage



def detect_dark_spots(img):

    img = img.astype(float)


    # إزالة قيم NoData (الصفر)
    valid_pixels = img[img > 0]


    stats = {

        "image_mean": round(float(np.mean(img)), 2),

        "image_min": round(float(np.min(img)), 2),

        "image_max": round(float(np.max(img)), 2),

        "threshold": 0,

        "candidate_pixels": 0,

        "objects_found": 0

    }



    if len(valid_pixels) == 0:

        return {

            "detected": False,

            "ratio": 0,

            "area_pixels": 0,

            "stats": stats

        }



    # حساب العتبة من البيانات الحقيقية فقط
    threshold = np.percentile(
        valid_pixels,
        8
    )


    stats["threshold"] = round(
        float(threshold),
        2
    )



    # البقع الداكنة فقط داخل البيانات الصحيحة
    mask = (

        (img > 0)

        &

        (img < threshold)

    )



    stats["candidate_pixels"] = int(
        np.sum(mask)
    )



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


    stats["objects_found"] = int(count)



    if count == 0:

        return {

            "detected": False,

            "ratio":0,

            "area_pixels":0,

            "stats":stats

        }




    sizes = ndimage.sum(

        mask,

        labels,

        range(1, count + 1)

    )



    # إزالة البقع الصغيرة جداً

    min_size = img.size * 0.00003



    valid_objects = [

        s for s in sizes

        if s > min_size

    ]



    stats["valid_objects"] = len(valid_objects)



    if len(valid_objects) == 0:

        return {

            "detected":False,

            "ratio":0,

            "area_pixels":0,

            "stats":stats

        }




    # اختيار أكبر بقعة

    largest = np.argmax(sizes) + 1



    largest_mask = labels == largest



    area_pixels = int(
        sizes[largest - 1]
    )



    ratio = (

        area_pixels /

        np.sum(img > 0)

    )



    cy, cx = ndimage.center_of_mass(

        largest_mask

    )



    return {


        "detected": True,


        "mask": largest_mask,


        "ratio": float(ratio),


        "center": (

            int(cx),

            int(cy)

        ),


        "area_pixels": area_pixels,


        "stats": stats

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


    value = min(

        95,

        50 + (ratio * 1000)

    )


    return round(value,2)
