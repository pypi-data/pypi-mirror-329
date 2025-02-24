# YOLOmosaic
A Python library for visualizing YOLO detections and segmented instances on large orthomosaic images, with the ability to generate shapefiles for GIS integration


### NOTE

This project uses GDAL==3.4.1, to install GDAL on ubuntu. Use the following command: 

```
sudo apt-get install libgdal-dev
```
Proceed with 
```
pip3 install GDAL==3.4.1
```

#### Example usage under CLI mode

```
ymosaic --input /home/user/Documents/YOLOmosaic/test/images/OUTPUT.tif --type "segment" --model /home/user/Documents/YOLOmosaic/models/best.pt
```

Expected output:

```
Input orthomozaic :  OUTPUT.tif
Directory /home/user/Documents/YOLOmosaic/test/images/OUTPUT_output already exists.
Output set to : /home/user/Documents/YOLOmosaic/test/images/OUTPUT_output/OUTPUT.png
segment  model path set to  /home/user/Documents/YOLOmosaic/models/best.pt
Mask type set to  segment
driver_long_name: GeoTIFF
raster_x_size: 3299
raster_y_size: 3693
band_count: 4
projection: PROJCS["WGS 84 / UTM zone 14N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-99],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32614"]]
geotransform: (633491.5605675817, 0.005575933715099989, 0.0, 5193232.824243805, 0.0, -0.005575933715099989)
size: 0.048758922
band_1_metadata: {}
band_2_metadata: {}
band_3_metadata: {}
band_4_metadata: {}
The file {output_png_image} exists.
{GREEN}Conversion successful!{RESET}
starting inference...
Loading model
Checking for CUDA devices
/home/user/.local/lib/python3.10/site-packages/torch/cuda/__init__.py:129: UserWarning: CUDA initialization: CUDA unknown error - this may be due to an incorrectly set up environment, e.g. changing env variable CUDA_VISIBLE_DEVICES after program start. Setting the available devices to be zero. (Triggered internally at ../c10/cuda/CUDAFunctions.cpp:108.)
  return torch._C._cuda_getDeviceCount() > 0
Using device: cpu
Running tiled inference...
Performing prediction on 6 slices.
Time taken to run inference on the orthomozaic: 0.2340 minutes
Detection complete... Saving results
Conveting pixel coordinates to spatial coordinates...
0  polygons could not be processed.
/home/user/.local/lib/python3.10/site-packages/pyogrio/geopandas.py:662: UserWarning: 'crs' was not provided.  The output dataset will not have projection information defined and may not be usable in other systems.
  write(
02/23/2025 01:32:59 - INFO - pyogrio._io -   Created 71 records
Shapefile saved to /home/user/Documents/YOLOmosaic/test/images/OUTPUT_output/OUTPUT.shp

```

#### Example usage as python program 

```
from yolomosaic.ymosaic import ortho_inference

input_file = "/home/user/Documents/YOLOmosaic/test/images/OUTPUT.tif"
mask_type = "segment"
model = "/home/user/Documents/YOLOmosaic/models/best.pt"

ortho_inference(input_file, model, mask_type, tile_size=2048, overlap=0.2, conf=0.50)

```
