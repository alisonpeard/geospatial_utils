#!/bin/bash
# transform all shapefiles
# on command line: 
# cd <directory with shapefiles>
# bash shp_to_gpkg.sh
for file in *.shp; do ogr2ogr -f GPKG "${file/.shp/.gpkg}" $file; done
