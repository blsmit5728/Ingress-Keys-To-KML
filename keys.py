import numpy
from shapely.geometry import Point, Polygon
import json
from yaml import load, dump
import argparse

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import simplekml
import logging

logger = logging.getLogger(name="Ingress Keys")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter(f"IngressKeys::%(asctime)s - %(name)s - %(levelname)s - %(message)s")
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

argument_parser = argparse.ArgumentParser("keys.py")
argument_parser.add_argument("-f", dest="filename", type=str, default="example.csv", 
                             help="Tab seperated file from inventory plugin export.",
                             required=True)
argument_parser.add_argument("-c", dest="config_filename", type=str, default="example_config.yml", 
                             help="Config File for BBOX")
argument_parser.add_argument("-k", dest="kml_filename", type=str, default="output.kml",
                             help="KML Filename")
argument_parser.add_argument("-o", dest="keys_filename", type=str, default="all_keys.json",
                             help="Filename for JSON formatted output")
argument_parser.add_argument("-i", dest="poly_keys_filename", type=str, default="ploy_keys.json",
                             help="Filename for JSON formatted output of Keys in Polygon")
args = argument_parser.parse_args()

config_parms = load(open(args.config_filename, "r"),Loader=Loader)

fn = args.filename
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
BoundingBox = []
for vertex in bbox_coords:
    LAT, LON = vertex.split(",")
    LAT = float(LAT)
    LON = float(LON)
    BoundingBox.append( (LAT, LON) )

POLYGON = Polygon(BoundingBox)

count = 0
for key in keys:    
    point = Point(key.get("lat"),key.get("lng"))    
    if POLYGON.contains(point):
        count += 1
        logger.info(f"Portal \"{key.get('name')}\" is inside the Polygon")
        keys_in_poly["keys"].append(key)
logger.info(f"{count} Portals were found to reside inside the Polygon")
kml = simplekml.Kml()

for portal_info in keys_in_poly.get("keys"):
    kml.newpoint(name=portal_info.get("name"), coords=[(portal_info.get("lng"), portal_info.get("lat"))],description=f"Keys: {portal_info.get('count')}" )    
    
logger.info(f"Saving KML file to {args.kml_filename}")
kml.save(args.kml_filename)

logger.info(f"Dumping Polygon Keys to {args.poly_keys_filename}")
with open(args.poly_keys_filename, "w") as outfile:
    json.dump(keys_in_poly,outfile,indent=4,sort_keys=True)
logger.info(f"Dumping all Keys to {args.keys_filename}")
with open(args.keys_filename, "w") as outfile:
    json.dump(export_keys_dict,outfile,indent=4,sort_keys=True)
