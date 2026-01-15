img = '/home/nelson/research/paper-drone2report/case_studies/case-study-5_image_classification/weed-detection-in-soybean-crops/broadleaf/1.tif'
# -------------- IMPORTS
import sys
import rasterio
from rasterio.crs import CRS
import geopandas as gpd
from shapely.geometry import box
from osgeo import gdal, osr
from pathlib import Path

# -------------- CONSTANTS
#assigned CRS will be Web Mercator, since it's widely accepted
DEFAULT_EPSG = 3857

# -------------- COMMAND LINE PARSING
#input argument checks
if len(sys.argv) != 2:
	print ("""
	build_shapefile: a tool for converting a basic, bare tif to a geotif ready
	to be inputed to drone2report. This tool will add all the accessory 
	shapefiles, plus will add a projection to the passed .tif if missing.
	Usage:
	python build_shapefile.py <input_tif_file>
	""")
	sys.exit(0)
img = sys.argv[1]

#remove the .tif(f) extension
core = Path(img).with_suffix('')
print("core filename:", core)

# -------------- IMAGE PARSING
#extract info on the image
with rasterio.open(img) as src:
    bounds = src.bounds
    crs = src.crs
    
#safeguard: if no crs is present we assign the default
missing_CRS = False
if crs is None:
	missing_CRS = True
	crs = CRS.from_epsg(DEFAULT_EPSG)  

print("bounds: ", bounds)
print("crs: ", crs)

# -------------- CREATING FILES .shp .cpg .dbf .shx .prj
# Create footprint polygon
geometry = box(bounds.left, bounds.bottom, bounds.right, bounds.top)

# Minimal attribute table
gdf = gpd.GeoDataFrame(
    {
        "id": [1],
        "gid": [1],
        "name": ["image_extent"]
    },
    geometry=[geometry],
    crs=crs
)

# Write shapefiles
gdf.to_file(Path(img).with_suffix('.shp'))

# -------------- ADDING CRS TO TIF FILE, IF NECESSARY
if missing_CRS:
	print('The original image did not contain a projection. We add a default one')
	ds = gdal.Open(img, gdal.GA_Update)

	srs = osr.SpatialReference()
	srs.ImportFromEPSG(DEFAULT_EPSG) 

	ds.SetProjection(srs.ExportToWkt())
	ds = None
