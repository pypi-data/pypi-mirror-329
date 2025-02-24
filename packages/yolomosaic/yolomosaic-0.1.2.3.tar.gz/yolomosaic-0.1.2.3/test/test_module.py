from yolomosaic.ymosaic import ortho_inference

input_file = "/home/jithin-mathew/Documents/YOLOmosaic/test/images/OUTPUT.tif"
#mask_type = "segment"
mask_type = "detect"
model = "/home/jithin-mathew/Documents/YOLOmosaic/models/best.pt"

ortho_inference(input_file, model, mask_type, tile_size=2048, overlap=0.2, conf=0.50)

