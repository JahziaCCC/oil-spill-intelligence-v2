import json
import numpy as np
import requests
from PIL import Image
from io import BytesIO

from sentinel import (
    get_token,
    iso_z,
    PROCESS_API,
)


def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)



def build_evalscript():

    return """
//VERSION=3

function setup() {

  return {

    input:[
      {
        bands:[
          "VV",
          "dataMask"
        ]
      }
    ],

    output:{
      bands:1,
      sampleType:"UINT8"
    }

  }

}



function toDB(x){

    return 10.0 * Math.log(x) / Math.LN10;

}



function evaluatePixel(s){


    if(s.dataMask==0)

        return [0];


    var db = toDB(s.VV);


    var v = (db + 25) / 25;


    v = Math.max(0, Math.min(1, v));


    return [
        Math.round(v * 255)
    ];

}
"""



def download_preview(bbox, time_from, time_to):

    cfg = load_config()


    token = get_token()


    headers = {

        "Authorization": f"Bearer {token}",

        "Content-Type": "application/json"

    }



    body = {


        "input":{


            "bounds":{

                "bbox":bbox,

                "properties":{

                    "crs":
                    "http://www.opengis.net/def/crs/EPSG/0/4326"

                }

            },


            "data":[

                {

                    "type":"sentinel-1-grd",

                    "dataFilter":{

                        "timeRange":{

                            "from":iso_z(time_from),

                            "to":iso_z(time_to)

                        },

                        "mosaickingOrder":"mostRecent"

                    }

                }

            ]

        },


        "output":{


            # رفع الدقة لمنع خطأ Copernicus
            # الحد الأعلى 1500 متر/بكسل

            "width":1500,

            "height":1500,


            "responses":[

                {

                    "identifier":"default",

                    "format":{

                        "type":"image/png"

                    }

                }

            ]

        },


        "evalscript":build_evalscript()

    }



    try:


        r = requests.post(

            PROCESS_API,

            headers=headers,

            json=body,

            timeout=180

        )



        if not r.ok:


            print("\n❌ Copernicus Process API Error")

            print("Status:", r.status_code)

            print(r.text[:1000])

            return None



        img = Image.open(

            BytesIO(r.content)

        ).convert("L")



        return np.array(img)



    except Exception as e:


        print("\n❌ Image download failed")

        print(e)

        return None
