# Geospatial Utilities
Useful operations for manipulating xarray, geopandas, and numpy geospatial data

# Creating grids from geospatial data
Grids are specified by centroid, height, width, rotation, and mesh. For numerical simulations, transform to numpy is always done such that causality goes from [0,0]->[n,n]. E.g., for modelling waves the rotation should be chosen depending on the angle of the coastline as follows:
<img src='https://github.com/alisonpeard/geospatial_utils/assets/41169293/73099e83-6c3e-4bfd-aeed-85cce6858e74' width='800'>
<img src='https://github.com/alisonpeard/geospatial_utils/assets/41169293/54107eeb-fad0-4722-b56d-2abe7a14103b' width='500'>
<img src='https://github.com/alisonpeard/geospatial_utils/assets/41169293/ce0c3e99-dc36-415b-9437-3826ae3318b5' width='500'>
<img src='https://github.com/alisonpeard/geospatial_utils/assets/41169293/6b726280-511f-4b0d-90c4-86251d12a6cd' width='500'>
<img src='https://github.com/alisonpeard/geospatial_utils/assets/41169293/55f6ba7b-32b5-4f60-878c-0dd5d9f44440' width='500'>
