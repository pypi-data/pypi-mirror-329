import os 
import argparse # for receiving input arguments
import time

# NATIVE IMPORTS 
from yolomosaic.utils.general import get_orthomosaic_metadata
from yolomosaic.orthomosaic.orthomosaic_preprocessing import orthomozaic_processing
from yolomosaic.computer_vision.model_inference import run_tiled_inference, generate_coordinate_file
from yolomosaic.geo_processing.geo import geo_coordinates

def ortho_inference(input_path, model, mask_type, output_path=None, tile_size=2048, overlap=0.2, conf=0.50):
    # Input and output paths
    
    # DEFAULT ARGUMENTS
    tile_size = 2048
    overlap_ratio = 0.2
    confidence_threshold = 0.50
    mask_type = "detect"
    model_path_detection = "./best.pt" 
    model_path_segmentation = "./best.pt"
    
    ################### I/O directory SETTING ############
    if input_path == None:
        print("No Input file provided, please provide the path to orthomozaic file.")
        exit()
    else:
    	input_orthomozaic = input_path
    	if os.path.isfile(input_orthomozaic):
    	    print("Input orthomozaic : ", os.path.basename(input_orthomozaic))
    	    
    	else:
    	    print("Invalid file path, please check the input")
    	    exit()
    
    if output_path == None:
        directory_path = os.path.dirname(input_orthomozaic)
        
        dir_name = os.path.basename(input_orthomozaic).split(".")[0]+"_output"
        new_dir_path = os.path.join(directory_path, dir_name)

        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            directory_path = new_dir_path
            print(f"Directory {new_dir_path} created.")
        else:
            directory_path = new_dir_path
            print(f"Directory {new_dir_path} already exists.")
    else:
        directory_path = output_path
    
    output_jpg_file_path = os.path.join(directory_path, os.path.basename(input_orthomozaic).split(".")[0]+".png")
    
    print('Output set to : '+ output_jpg_file_path)
    
    ################### MODEL SETTING ############
    
    if model == None:
        print("No valid model provided... exiting program")
        exit()
    else: 
        if os.path.isfile(model) and model.endswith(".pt"):
            if mask_type == "detect":
                model_path_detection  = model
                print(mask_type, " model path set to ", model_path_detection)
            elif mask_type == "segment":
                model_path_segmentation  = model
                print(mask_type, " model path set to ", model_path_segmentation)
                
    ################### FINE PARAMETER SETTING ############
    
    if tile_size == None:
        pass
    else:
        tile_size = tile_size
        
    if overlap == None:
        pass
    else:
        overlap_ratio = overlap
        
    if conf == None:
        pass
    else:
        confidence_threshold = conf
    
    if mask_type == "segment":
        #mask_type = "segment"
        print("Mask type set to ", mask_type)
    else:
        mask_type == "detect"
        print("Mask type set to ", mask_type)
        
    ########## End of arguments ####################
    
    ########## 	PRINTING METADATA  #################
    metadata = get_orthomosaic_metadata(input_orthomozaic)
    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Failed to retrieve metadata.")
    
    ########## 	ORTHOMOSAIC CONVERSION  #################
    
    if metadata['size'] > 5:     
    	success = orthomozaic_processing.orthomozaic_to_png(input_orthomozaic, output_jpg_file_path)
    else:
        success = orthomozaic_processing.orthomozaic_to_png(input_orthomozaic, output_jpg_file_path)
    
    if success:
        print("{GREEN}Conversion successful!{RESET}")
    else:
        print("{RED}Conversion failed.{RESET}")

    ####################################################    
    print("starting inference...")
    
    start_time = time.time()
    if mask_type == "segment": 
        plot_boundaries = run_tiled_inference(model_path_segmentation, confidence_threshold, tile_size, overlap_ratio, output_jpg_file_path) # conf, tile_size, overlap
    elif mask_type == "detect":
        plot_boundaries = run_tiled_inference(model_path_detection, confidence_threshold, tile_size, overlap_ratio, output_jpg_file_path) # conf, tile_size, overlap
    end_time = time.time()  
    elapsed_time = (end_time - start_time)/60
    print(f"Time taken to run inference on the orthomozaic: {elapsed_time:.4f} minutes")

    csv = generate_coordinate_file(plot_boundaries, mask_type, directory_path, input_orthomozaic)
    
    shape_file_name = os.path.join(directory_path, os.path.basename(input_orthomozaic).split(".")[0]+".shp")
    
    geo_coordinates.generate_spatial_coordinates(csv, input_orthomozaic, shape_file_name, mask_type)
    
if __name__ == '__main__':
    main()
