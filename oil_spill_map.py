import folium


def create_oil_spill_map(
    latitude,
    longitude,
    area_km2,
    probability,
    classification,
    confidence,
    scene_id,
    output_file="oil_spill_detection_map.html"
):

    """
    إنشاء خريطة تفاعلية لرصد الانسكاب النفطي
    """


    # إنشاء الخريطة

    m = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=9

    )


    # تحديد لون المؤشر

    if probability >= 75:

        color = "red"

    elif probability >= 45:

        color = "orange"

    else:

        color = "green"



    # إضافة العلامة

    popup = f"""
    <b>Oil Spill Intelligence</b><br><br>

    Latitude: {latitude}<br>
    Longitude: {longitude}<br><br>

    Area: {area_km2} km²<br>

    Probability: {probability}%<br>

    Classification: {classification}<br>

    Confidence: {confidence}%<br><br>

    Scene:<br>
    {scene_id}

    """



    folium.Marker(

        location=[

            latitude,

            longitude

        ],

        popup=folium.Popup(

            popup,

            max_width=350

        ),

        icon=folium.Icon(

            color=color,

            icon="tint",

            prefix="fa"

        )

    ).add_to(m)



    # دائرة تمثل نطاق البقعة

    radius = max(

        200,

        area_km2 * 500

    )


    folium.Circle(

        location=[

            latitude,

            longitude

        ],

        radius=radius,

        color=color,

        fill=True,

        popup=f"{probability}%"

    ).add_to(m)



    # حفظ الخريطة

    m.save(output_file)



    return output_file
