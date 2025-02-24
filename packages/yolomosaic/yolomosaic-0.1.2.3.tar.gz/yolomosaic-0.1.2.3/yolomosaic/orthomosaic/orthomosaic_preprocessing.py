from osgeo import gdal
import os

class orthomozaic_processing:
    def __init__(self, orthomozaic_tif, output_png_image):
        self.orthomozaic_tif = orthomozaic_tif
        self.output_png_image = output_png_image

    def orthomozaic_to_png(orthomozaic_tif, output_png_image): 
        if os.path.exists(output_png_image):
            print("The file {output_png_image} exists.")   
            return True
        else:
            try:
                options_list = [
                    '-ot Byte',
                    '-of PNG',
                    '-b 1',
                    '-b 2',
                    '-b 3',
                    '-scale'
                ]           
                options_string = " ".join(options_list)
                gdal.Translate(
                    output_png_image,
                    orthomozaic_tif,
                    options=options_string
                )

                return True
            except Exception as e:
                print(f"Error: {e}")
                return False

    def orthomozaic_to_jpg(orthomozaic_tif, output_png_image): 
        if os.path.exists(output_png_image):
            print("The file {output_png_image} exists.")   
            return True
        else:
            try:
                options_list = [
                    '-ot Byte',
                    '-of JPEG',
                    '-b 1',
                    '-b 2',
                    '-b 3',
                    '-scale'
                ]           
                options_string = " ".join(options_list)
                gdal.Translate(
                    output_png_image,
                    orthomozaic_tif,
                    options=options_string
                )

                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
