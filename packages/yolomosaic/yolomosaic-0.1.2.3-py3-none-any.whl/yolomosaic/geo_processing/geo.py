import pandas as pd
import geopandas as gpd
import rasterio
#from rasterio.transform import Affine
from shapely.geometry import Polygon


class geo_coordinates:

    error_count = 0 # Global variable
    
    def __init__(self, tiff_path, csv_path, shape_file_name, mask_type):
        self.tiff_path = tiff_path
        self.csv_path = csv_path
        self.shape_file_name = shape_file_name
        self.mask_type = mask_type

    #getting matrix transformation from the GeoTIFF file
    def get_transform(tiff_path):
        with rasterio.open(tiff_path) as src:
            transform = src.transform
        return transform

    #converting Pixel to spacial coordinates
    def pixel_to_bbox_coords(row, transform):
        minx, miny = transform * (row['minx'], row['miny'])
        maxx, maxy = transform * (row['maxx'], row['maxy'])
        return Polygon([(minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])
        
        
    def pixel_to_polygon_coords(row, transform):
        polygon_points = row['polygon']
        
        polygon_points = polygon_points.strip('[[]]').split(',')
        polygon_coords = []

        try:        
            for i in range(0, len(polygon_points), 2):
                x_pixel = int(polygon_points[i])
                y_pixel = int(polygon_points[i + 1])
        
                # Transform the pixel coordinates to spatial coordinates using the affine transformation
                x_spatial, y_spatial = transform * (x_pixel, y_pixel)
                polygon_coords.append((x_spatial, y_spatial))
        
            if polygon_coords and polygon_coords[0] != polygon_coords[-1]:
                polygon_coords.append(polygon_coords[0])  # Close the polygon
        except Exception:
            #global error_count
            geo_coordinates.error_count+=1
            pass
        return Polygon(polygon_coords)  # Return the Polygon object with spatial coordinates
        
        
    def generate_spatial_coordinates(csv_path, tiff_path, shape_file_name, mask_type):
        print("Conveting pixel coordinates to spatial coordinates...")
        
        df = pd.read_csv(csv_path)
        
        transform = geo_coordinates.get_transform(tiff_path)
        
        #convert each row to a polygon
        if mask_type == "detect":
            # For detection, convert bounding boxes to spatial coordinates
            df['geometry'] = df.apply(geo_coordinates.pixel_to_bbox_coords, transform=transform, axis=1)
            #create a GDF
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
        
            #fetching the ESPG code from the GeoTIFF file
            with rasterio.open(tiff_path) as src:
                transform = src.transform
                crs = src.crs  # Extract the CRS from the TIFF file
        
            gdf.set_crs(crs, allow_override=True, inplace=True)
        
            # Step 6: Reproject to EPSG:4326 (WGS 84)
            gdf.to_crs("EPSG:4326", inplace=True)
        
            #save to Shapefile on desired location
            gdf.to_file(shape_file_name)
        
        elif mask_type == "segment":
            
            geometries = []
            # For segmentation, convert polygons to spatial coordinates
            for index, row in df.iterrows():
                polygon = geo_coordinates.pixel_to_polygon_coords(row, transform)
                if polygon:
                    geometries.append(polygon)
        
            print(geo_coordinates.error_count," polygons could not be processed.")
            # Create GeoDataFrame from the polygons
            gdf = gpd.GeoDataFrame({'geometry': geometries})

            # Fetch the CRS (Coordinate Reference System) from the GeoTIFF
            with rasterio.open(tiff_path) as src:
                crs = src.crs
                if crs is not None:
                    gdf.set_crs(crs, allow_override=True)
                else:
                    gdf.set_crs("EPSG:4326", allow_override=True, inplace=True)
                    gdf.to_crs("EPSG:4326", inplace=True)
	            
            # Save to Shapefile at the specified location
            gdf.to_file(shape_file_name)
            print(f"Shapefile saved to {shape_file_name}")
                
