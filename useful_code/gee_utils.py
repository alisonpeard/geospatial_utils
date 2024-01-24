# handy GEE functions

# folium plotting
import folium

def add_ee_layer(self, ee_image_object, vis_params, name):
    """Adds a method for displaying Earth Engine image tiles to folium map."""
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add Earth Engine drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

ee.Initialize()
from shapely.geometry import box

def get_fabdem(wd: str, aoi: gpd.GeoDataFrame, buffer=2000, scale=30):
    
    BUFFER = 20000 # 20km
    bbox = box(*aoi.to_crs(3857).total_bounds)
    bbox = box(*gpd.GeoDataFrame(index=[0], crs='epsg:3857', geometry=[bbox.buffer(BUFFER)]).to_crs(4326).total_bounds)
    
    bbox_ee = ee.Geometry.Polygon(bbox.__geo_interface__['coordinates'],
                                            proj=ee.Projection('EPSG:4326'))
    
    fabdem = ee.ImageCollection("projects/sat-io/open-datasets/FABDEM")
    fabdem = ee.Image(fabdem.filterBounds(bbox_ee).mosaic()).clip(bbox_ee)
    
    geemap.ee_export_image(fabdem, filename=os.path.join(wd, "fabdem.tif"), scale=30, region=bbox_ee)
    
# get_fabdem("<event_dir>", <aoi_gdf>)

durationPalette = ['C3EFFE', '1341E8', '051CB0', '001133']

m = folium.Map(location=[lon, lat], zoom_start=5)

# map extent
vizParams = {'min': 0, 'max': 1, 'palette': '001133'}
m.add_ee_layer(storm.select('flooded').selfMask(), vizParams, f"{stormDartmouthId} - Inundation Extent")

# durations
durationPalette = ['C3EFFE', '1341E8', '051CB0', '001133'];
m.add_ee_layer(storm.select('duration').selfMask(), {'min': 0, 'max': 4, 'palette': durationPalette},
  f"index_dict[stormDartmouthId] - Duration")

# all floods to view satellite-derived flood plain
m.add_ee_layer(gfdFloodedSum.selfMask(), {'min': 0, 'max': 10, 'palette': durationPalette}, 'GFD Satellite Observed Flood Plain');

# 
jrc = gfd.select('jrc_perm_water').sum().gte(1)
m.add_ee_layer(jrc.selfMask(), {'min': 0, 'max': 1, 'palette': 'C3EFFE'}, 'JRC Permanent Water')

m


# get property names of a feature 
FeatureCollection.first().propertyNames().getInfo()
Feature.get('property_name')

