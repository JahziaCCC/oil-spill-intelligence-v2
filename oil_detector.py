import numpy as np
from scipy import ndimage



def detect_dark_spots(img):

    img = img.astype(float)


    valid_pixels = img[img > 0]


    stats = {

        "image_mean": round(float(np.mean(img)), 2),

        "image_min": round(float(np.min(img)), 2),

        "image_max": round(float(np.max(img)), 2),

        "threshold": 0,

        "candidate_pixels": 0,

        "objects_found": 0,

        "valid_objects": 0

    }



    if len(valid_pixels) == 0:

        return None



    threshold = np.percentile(

        valid_pixels,

        8

    )


    stats["threshold"] = round(

        float(threshold),

        2

    )



    mask = (

        (img > 0)

        &

        (img < threshold)

    )



    stats["candidate_pixels"] = int(

        np.sum(mask)

    )



    mask = ndimage.binary_opening(

        mask,

        iterations=2

    )


    mask = ndimage.binary_closing(

        mask,

        iterations=3

    )



    labels, count = ndimage.label(mask)



    stats["objects_found"] = int(count)



    if count == 0:

        return None



    sizes = ndimage.sum(

        mask,

        labels,

        range(1, count + 1)

    )



    min_size = img.size * 0.00003



    valid_objects = [

        s for s in sizes

        if s > min_size

    ]



    stats["valid_objects"] = len(valid_objects)



    if len(valid_objects) == 0:

        return None



    largest = np.argmax(sizes) + 1


    largest_mask = labels == largest



    area_pixels = int(

        sizes[largest - 1]

    )



    valid_area = np.sum(

        img > 0

    )



    ratio = (

        area_pixels /

        valid_area

    )



    cy, cx = ndimage.center_of_mass(

        largest_mask

    )



    return {

        "detected": True,


        "mask": largest_mask,


        "ratio": float(ratio),


        # مهم لـ main.py

        "area": area_pixels,


        "area_pixels": area_pixels,


        "center": (

            int(cx),

            int(cy)

        ),


        "stats": stats

    }





def risk_score(ratio):


    if ratio >= 0.05:

        return {

            "level": "HIGH",

            "score": 90

        }


    elif ratio >= 0.02:

        return {

            "level": "MEDIUM",

            "score": 70

        }


    elif ratio >= 0.005:

        return {

            "level": "LOW",

            "score": 50

        }


    else:

        return {

            "level": "VERY LOW",

            "score": 20

        }





def confidence(ratio):


    value = min(

        95,

        50 + (ratio * 1000)

    )


    return round(

        value,

        2

    )
