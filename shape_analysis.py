import numpy as np
from scipy import ndimage



def analyze_shape(mask):
    """
    تحليل شكل المنطقة المكتشفة

    يرجع:
    - المساحة بالبكسل
    - المحيط التقريبي
    - الاستطالة
    - Compactness
    """

    if mask is None or np.sum(mask) == 0:

        return {

            "area_pixels": 0,
            "perimeter": 0,
            "elongation": 0,
            "compactness": 0

        }



    # المساحة
    area = np.sum(mask)



    # استخراج حدود البقعة
    eroded = ndimage.binary_erosion(mask)

    boundary = mask ^ eroded

    perimeter = np.sum(boundary)



    # إحداثيات البقعة
    y, x = np.where(mask)



    if len(x) < 2:

        elongation = 0

    else:

        coords = np.column_stack((x, y))

        covariance = np.cov(coords, rowvar=False)


        eigenvalues = np.linalg.eigvalsh(
            covariance
        )

        eigenvalues = np.sort(
            eigenvalues
        )


        if eigenvalues[0] == 0:

            elongation = 0

        else:

            elongation = (
                eigenvalues[1] /
                eigenvalues[0]
            )



    # Compactness
    # كلما اقترب من 1 الشكل أكثر انتظاماً

    if perimeter == 0:

        compactness = 0

    else:

        compactness = (
            4 *
            np.pi *
            area /
            (perimeter ** 2)
        )



    return {

        "area_pixels": int(area),

        "perimeter": int(perimeter),

        "elongation": round(
            float(elongation),
            2
        ),

        "compactness": round(
            float(compactness),
            3
        )

    }
