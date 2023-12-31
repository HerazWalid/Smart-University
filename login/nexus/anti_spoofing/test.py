import os
import cv2
import numpy as np
import argparse
import warnings
import time
from ultralytics import YOLO


from .src.anti_spoof_predict import AntiSpoofPredict
from .src.generate_patches import CropImage
from .src.utility import parse_model_name
warnings.filterwarnings('ignore')

SAMPLE_IMAGE_PATH = "./videos/"

# def check_image(image):
#     height, width, channel = image.shape
#     if width/height != 3/4:
#         print("Image is not appropriate!!!\nHeight/Width should be 4/3.")
#         return False
#     else:
#         return True


def test(i,image,bbox,device_id,model_dir="./AI/anti_spoofing/resources/anti_spoof_models"):
                    model_test = AntiSpoofPredict(device_id)
                    image_cropper = CropImage()
                    # Get the coordinates of the bounding box
                    image_bbox =[bbox[0],bbox[1],bbox[2]-bbox[0]+1,bbox[3]-bbox[1]+1]
                    prediction = np.zeros((1, 3))
                    test_speed = 0
                    # sum the prediction from single model's result
                    for model_name in os.listdir(model_dir):
                        h_input, w_input, model_type, scale = parse_model_name(model_name)
                        param = {
                        "org_img": image,
                        "bbox": image_bbox,
                        "scale": scale,
                        "out_w": w_input,
                        "out_h": h_input,
                        "crop": True,
                                }
                        if scale is None:
                            param["crop"] = False
                        img1 = image_cropper.crop(**param)
                        start = time.time()
                        prediction += model_test.predict(img1, os.path.join(model_dir, model_name))
                        test_speed += time.time()-start

                    # draw result of prediction
                    label = np.argmax(prediction)
                    value = prediction[0][label]/2
                    if label == 1:
                        i+=1
                        print("Real Face. Score: {:.2f}.".format( value))
                        result_text = "RealFace Score: {:.2f}".format(value)
                        color = (255, 0, 0)
                    else:
                        i=0
                        print("Fake Face. Score: {:.2f}.".format(value))
                        result_text = "FakeFace Score: {:.2f}".format(value)
                        color = (0, 0, 255)
                    print("Prediction cost {:.2f} s".format(test_speed))
                    return  i,label,result_text,color
                

# if __name__ == "__main__":
#     desc = "test"
#     parser = argparse.ArgumentParser(description=desc)
#     parser.add_argument(
#         "--device_id",
#         type=int,
#         default=0,
#         help="which gpu id, [0/1/2/3]")
#     parser.add_argument(
#         "--model_dir",
#         type=str,
#         default="./resources/anti_spoof_models",
#         help="model_lib used to test")
#     parser.add_argument(
#         "--image_name",
#         type=str,
#         default="image_F1.jpg",
#         help="image used to test")
#     args = parser.parse_args()
#     test(args.image_name, args.model_dir, args.device_id)
