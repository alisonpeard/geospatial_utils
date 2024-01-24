import os
os.environ['USE_PYGEOS'] = '0'
import xarray as xr
import geopandas as gpd



def xarray_to_geopandas(path, xvar='lon', yvar='lat', var=['data'], crs='4326'):
    ds = xr.open_dataset(path)
    data = ds[var]
    df = data.to_dataframe().reset_index()
    df = df.fillna(0.)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[xvar], df[yvar]))[var + ['geometry']]
    gdf = gdf.set_crs(crs)
    return gdf


def xarray_to_geopandas_with_time(path, xvar='lon', yvar='lat', var=['data'], timevar='time', crs='4326'):
    ds = xr.open_dataset(path)
    df = ds.to_dataframe().reset_index()
    df = df.fillna(0.)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[xvar], df[yvar]))[[timevar] + var +  ['geometry']]
    gdf = gdf.set_crs(crs)
    return gdf