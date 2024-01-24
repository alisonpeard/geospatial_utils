import os
os.environ['USE_PYGEOS'] = '0'
import numpy as np
import xarray as xr
import geopandas as gpd
from shapely.geometry import box, Polygon, MultiPolygon
from shapely.affinity import rotate # for aoi
from shapely.prepared import prep # for aoi

from .utils import *
from .xarray import *


def create_aoi(centroid, height=200_000, width=100_000, rotation=0, local_crs="EPSG:3857"):
    """
    Create a rotated area of interest box around a centroid.

    Parameters:
    -----------
    centroid : list
        Center of AoI in EPSG:4326.
    height : float
        Height of AoI in metres.
    width : float
        Width of AoI in metres.
    rotation:
        Rotation of AoI from pointing E->W in degrees.
    local_crs : string
        Local coordinate reference system that preserves distances.
    
    Returns:
    --------
    aoi : geopandas.GeoDataFrame
    """
    centroid = transform_coordinates(*centroid, to_crs=local_crs)
    minx, maxx = centroid[0] - (width / 2), centroid[0] + (width / 2)
    miny, maxy = centroid[1] - (height / 2), centroid[1] + (height / 2)
    aoi = box(minx, miny, maxx, maxy)
    aoi = rotate(aoi, rotation, 'center')
    aoi = gpd.GeoDataFrame(geometry=[aoi]).set_crs(local_crs)
    return aoi


def grid_bounds(geom, delta):
    """For creating grids.
    
    https://www.matecdev.com/posts/shapely-polygon-gridding.html
    """
    minx, miny, maxx, maxy = geom.bounds
    nx = int((maxx - minx) / delta)
    ny = int((maxy - miny) / delta)
    gx, gy = np.linspace(minx, maxx, nx), np.linspace(miny, maxy, ny)
    grid = []
    index = []
    # C-style ordering varies last axis (j) fastest, causality from (0, 0)->(ny, nx)
    for j in range(len(gy)-1):      # first axis (rows)
        for i in range(len(gx)-1):  # second axis (cols)
            poly_ij = Polygon([[gx[i], gy[j]], [gx[i], gy[j+1]], [gx[i+1], gy[j+1]], [gx[i+1], gy[j]]])
            grid.append(poly_ij)
            index.append([j, i])
    return grid, np.array(index)


def partition(geom, delta):
    """For creating grids.
    
    https://www.matecdev.com/posts/shapely-polygon-gridding.html
    """
    prepared_geom = prep(geom)
    bounds, index = grid_bounds(geom, delta)
    grid = list(filter(prepared_geom.intersects, bounds))
    return grid, index

def switch(a, b):
    return copy(b), copy(a)

def create_aoi_grid(centroid, mesh=10_000, height=200_000, width=100_000, rotation=0, local_crs="EPSG:3857"):
    """Create a rotated geopandas.GeoDataFrame grid.
    
    Parameters:
    -----------
    centroid : list
        Center of AoI in EPSG:4326.
    mesh : float
        Mesh size in metres.
    height : float
        Height of AoI in metres.
    width : float
        Width of AoI in metres.
    rotation:
        Rotation of AoI from pointing E->W in degrees.
    local_crs : string
        Local coordinate reference system that preserves distances.
    
    Returns:
    --------
    aoi : geopandas.GeoDataFrame
    """
    def transpose_indices(index):
        # this ensures indices are always ordered to reflect causality
        index = index.tolist()
        index = [[x[1], x[0]] for x in index]
        return np.array(index)

    if (90 <= rotation < 180) | (270 <= rotation < 360): height, width = switch(height, width)
    boundary = create_aoi(centroid, height, width, local_crs=local_crs).geometry[0]
    grid, index = partition(boundary, mesh)
    if (90 <= rotation < 180) | (270 <= rotation < 360): index = transpose_indices(index)
    grid = MultiPolygon(grid)
    grid = rotate(grid, rotation, 'center') # [rotate(x, rotation, 'center') for x in grid]
    return gpd.GeoSeries(list(grid.geoms)), index


def grid_gdf_to_numpy(gdf, column):
    nx = int(gdf['j'].max() + 1)
    ny = int(gdf['i'].max() + 1)
    mat = np.zeros([ny, nx])
    for row in gdf.itertuples():
        i, j = int(row.i), int(row.j)
        mat[i, j] = getattr(row, column)
    return mat


def grid_zonal_statistics(grid, index, gdf, crs, columns=['speed', 'direction']):
    grid = gpd.GeoDataFrame(geometry=grid).set_crs(crs)
    grid['indices'] = index.tolist()
    gdf = gpd.sjoin(grid, gdf, how='left', predicate='intersects')
    
    # need these to keep track of order of grid cells
    gdf['i'] = gdf['indices'].apply(lambda x: int(x[0]))
    gdf['j'] = gdf['indices'].apply(lambda x: int(x[1]))
    
    gdf = gdf[['i', 'j'] + columns + ['geometry']].groupby('geometry').mean().reset_index()[['i', 'j'] + columns + ['geometry']]
    gdf = gpd.GeoDataFrame(gdf, geometry="geometry").set_crs(crs)
    return gdf


def npz_to_gdf_grid(npz_file, field_name="value"):
    array = npz_file['array']
    rotation = npz_file['rotation']
    centroid = npz_file['centroid']
    height = npz_file["height"]
    width = npz_file['width']
    mesh = npz_file["mesh"]
    crs = npz_file["crs"]
    
    grid, indices = create_aoi_grid(centroid, mesh=mesh, height=height, width=width,
                                                 rotation=rotation, local_crs=crs)
    
    values = []
    for i, j in indices:
        values.append(array[i, j])
        
    gdf = gpd.GeoDataFrame(values, columns=[field_name], geometry=grid).set_crs(crs)
    return gdf