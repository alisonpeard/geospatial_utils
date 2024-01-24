from pyproj import Transformer

def transform_coordinates(x, y, from_crs="EPSG:4326", to_crs="EPSG:3857"):
    transformer = Transformer.from_crs(from_crs, to_crs)
    coordinates = transformer.transform(y, x)
    return coordinates