import torch # to check for CUDA
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
import pandas as pd
import json
import os

def run_tiled_inference(model_path, conf, tile_size, overlap, output_jpg_file_path): 
    print("Loading model")
    #yolo_model_path = "./models/best.pt"
    yolo_model_path = model_path
    
    print("Checking for CUDA devices")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    print(f"Using device: {device}")
    
    detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov11',
    model_path=yolo_model_path,
    confidence_threshold=conf,
    device=device,  # or 'cuda:0'
    )
    
    print("Running tiled inference...")    
    result = get_sliced_prediction(
    output_jpg_file_path,
    detection_model,
    slice_height=tile_size,
    slice_width=tile_size,
    overlap_height_ratio=overlap,
    overlap_width_ratio=overlap,
    )
    
    plot_list = result.object_prediction_list
    
    return plot_list

   
def generate_coordinate_file(coordinates, mask_type, directory_path, input_orthomozaic):
    data = pd.DataFrame(columns=['score', 'minx', 'miny', 'maxx', 'maxy', 'width', 'height', 'class', 'polygon'])

    count = 0
    for object_prediction in coordinates:
        score = object_prediction.score.value
        bbox = object_prediction.bbox
        cat = object_prediction.category.id
        seg = object_prediction.mask
        
        if mask_type == "detect":
            width = bbox.maxx - bbox.minx
            height = bbox.maxy - bbox.miny
            data.loc[count] = [score, bbox.minx, bbox.miny, bbox.maxx, bbox.maxy, width, height, cat, None]
        elif mask_type == "segment":
            polygon = seg.segmentation 
            polygon_str = json.dumps(polygon)  # Convert the list of coordinates to a string

            data.loc[count] = [score, None, None, None, None, None, None, cat, polygon_str]            
        else:
            print("Mask type unknown")
            exit()
        count += 1
        
        

    # Print the resulting DataFrame
    csv_file_name = os.path.join(directory_path, os.path.basename(input_orthomozaic).split(".")[0]+".csv")
    data.to_csv(csv_file_name, index=False)

    print("Detection complete... Saving results")
    return csv_file_name
