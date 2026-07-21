def calculate_oil_probability(
    dark_ratio,
    area_km2,
    elongation,
    compactness,
    confidence
):
    """
    حساب احتمالية أن تكون البقعة انسكاب نفطي
    النتيجة من 0 إلى 100
    """

    score = 0


    # 1) نسبة الظلام
    if dark_ratio >= 0.02:
        score += 25

    elif dark_ratio >= 0.005:
        score += 15

    else:
        score += 5



    # 2) المساحة
    if area_km2 >= 5:
        score += 25

    elif area_km2 >= 0.5:
        score += 15

    else:
        score += 5



    # 3) الاستطالة
    if elongation >= 5:
        score += 25

    elif elongation >= 2:
        score += 15

    else:
        score += 5



    # 4) الشكل الدائري
    # البقع النفطية غالباً أقل انتظاماً

    if compactness < 0.3:
        score += 15

    elif compactness < 0.6:
        score += 10

    else:
        score += 5



    # 5) ثقة الكشف
    score = score * (confidence / 100)



    probability = round(
        min(score, 100),
        2
    )


    if probability >= 75:

        classification = "HIGH PROBABILITY OIL SPILL"


    elif probability >= 45:

        classification = "POSSIBLE OIL SPILL"


    else:

        classification = "LOW PROBABILITY"



    return {

        "probability": probability,

        "classification": classification

    }
