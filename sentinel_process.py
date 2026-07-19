import json
import datetime as dt
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
    input:[{bands:["VV","dataMask"]}],
    output:{bands:1,sampleType:"UINT8"}
  }
}

function toDB(x){
    return 10.0*Math.log(x)/Math.LN10;
}

function evaluatePixel(s){

    if(s.dataMask==0)
        return [0];

    var db = toDB(s.VV);

    var v = (db+25)/25;

    v=Math.max(0,Math.min(1,v));

    return [Math.round(v*255)];
}
"""


def download_preview(bbox, time_from, time_to):

    cfg = load_config()

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs":"http://www.opengis.net/def/crs/EPSG/0/4326"
                }
            },
            "data":[{
                "type":"sentinel-1-grd",
                "dataFilter":{
                    "timeRange":{
                        "from":iso_z(time_from),
                        "to":iso_z(time_to)
                    }
                }
            }]
        },

        "output":{
            "width":cfg["tile_width"],
            "height":cfg["tile_height"],
            "responses":[{
                "identifier":"default",
                "format":{"type":"image/png"}
            }]
        },

        "evalscript":build_evalscript()
    }

    r = requests.post(
        PROCESS_API,
        headers=headers,
        json=body,
        timeout=180
    )

    r.raise_for_status()

    img = Image.open(BytesIO(r.content)).convert("L")

    return np.array(img)
