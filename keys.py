import numpy
from shapely.geometry import Point, Polygon
import json
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import simplekml

config_parms = load(open("config.yml", "r"),Loader=Loader)

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

bbox_coords = config_parms.get("bbox")
print (bbox_coords)
BoundingBox = []
for vertex in bbox_coords:
    LAT, LON = vertex.split(",")
    LAT = float(LAT)
    LON = float(LON)
    BoundingBox.append( (LAT, LON) )
print(BoundingBox)


POLYGON = Polygon(BoundingBox)

for key in keys:    
    point = Point(key.get("lat"),key.get("lng"))    
    if POLYGON.contains(point):
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
