import numpy
from shapely.geometry import Point, Polygon
import json
import simplekml

fn = "jac_keys.csv"
fd = open(fn, "r")

lines = fd.readlines()

export_keys_dict = {"keys":[]}

for line in lines:
    line = line.strip("\n")
    name, lat, lon, cap, count = line.split("\t")
    if cap == "\u2302":
        cap = "none"
    d = {
        "name" : name.replace("'", ""),
        "lat" : float(lat),
        "lng" : float(lon),
        "capsule" : cap,
        "count" : int(count)
    }
    export_keys_dict["keys"].append(d)

keys = export_keys_dict.get("keys")

keys_in_poly = {"keys" : [] }

CharlestonBox = [
        (38.3374823, -81.6950226),
        (38.3544457, -81.7084122),
        (38.3738276, -81.7171669),
        (38.3805562, -81.7042923),
        (38.3829784, -81.6692734),
        (38.3700593, -81.6431808),
        (38.3587533, -81.6196632),
        (38.3462338, -81.6043854),
        (38.3396366, -81.5899658),
        (38.3291337, -81.5676498),
        (38.3164744, -81.5535736),
        (38.3066418, -81.5501404),
        (38.2999063, -81.5640450),
        (38.2984244, -81.5803528),
        (38.3233431, -81.6122818),
        (38.3312883, -81.6388893),
        (38.3416562, -81.6536522),
        (38.3477147, -81.6682434),
        (38.3369437, -81.6948509),
        (38.3374823, -81.6950226)
    ]

CharlestonPolygon = Polygon(CharlestonBox)

for key in keys:    
    point = Point(key.get("lat"),key.get("lng"))    
    if CharlestonPolygon.contains(point):
        print("----", key)
        keys_in_poly["keys"].append(key)
    
    # if polygon.contains(point):
    #     print("----", key)
    #     keys_in_poly["keys"].append(key)

kml = simplekml.Kml()

for portal_info in keys_in_poly.get("keys"):
    kml.newpoint(name=portal_info.get("name"), coords=[(portal_info.get("lng"), portal_info.get("lat"))],description=f"Keys: {portal_info.get('count')}" )    
    
kml.save("jac_keys.kml")

with open("keys_in_poly.json", "w") as outfile:
    json.dump(keys_in_poly,outfile,indent=4,sort_keys=True)

with open("ALL_KEYS.json", "w") as outfile:
    json.dump(export_keys_dict,outfile,indent=4,sort_keys=True)
