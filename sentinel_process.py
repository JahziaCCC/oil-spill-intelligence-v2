import requests
import numpy as np
from PIL import Image
from io import BytesIO

from sentinel import (
    get_token,
    iso_z,
    PROCESS_API,
)

def build_evalscript_preview():

    return """
//VERSION=3
function setup() {
  return {
    input: [{ bands:["VV","dataMask"] }],
    output: { bands:1, sampleType:"UINT8" }
  };
}

function toDB(x){
    return 10.0*Math.log(x)/Math.LN10;
}

function evaluatePixel(s){

    if(s.dataMask==0) return [0];

    var db = toDB(s.VV);

    var v = (db + 25.0)/25.0;

    v = Math.max(0,Math.min(1,v));

    return [Math.round(v*255)];
}
"""


def download_preview(
    bbox,
    time_from,
    time_to,
    width=1024,
    height=1024,
):

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                }
            },
            "data": [{
                "type": "sentinel-1-grd",
                "dataFilter": {
                    "timeRange": {
                        "from": iso_z(time_from),
                        "to": iso_z(time_to)
                    }
                }
            }]
        },

        "output": {
            "width": width,
            "height": height,
            "responses": [{
                "identifier":"default",
                "format":{"type":"image/png"}
            }]
        },

        "evalscript": build_evalscript_preview()
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
