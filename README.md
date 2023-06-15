# Ingress Inventory Keys to KML

```bash
usage: keys.py [-h] -f FILENAME [-c CONFIG_FILENAME] [-k KML_FILENAME] [-o KEYS_FILENAME] [-i POLY_KEYS_FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME           Tab seperated file from inventory plugin export.
  -c CONFIG_FILENAME    Config File for BBOX
  -k KML_FILENAME       KML Filename
  -o KEYS_FILENAME      Filename for JSON formatted output
  -i POLY_KEYS_FILENAME
                        Filename for JSON formatted output of Keys in Polygon
```

example:

```bash
user@host:$ python keys.py -f my_keys.csv
```