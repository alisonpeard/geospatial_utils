import os
from pyproj import Transformer

def notify(title, subtitle, message):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}" beep'
              """.format(message, title, subtitle))
    
def transform_coordinates(x, y, from_crs="EPSG:4326", to_crs="EPSG:3857"):
    transformer = Transformer.from_crs(from_crs, to_crs)
    coordinates = transformer.transform(y, x)
    return coordinates