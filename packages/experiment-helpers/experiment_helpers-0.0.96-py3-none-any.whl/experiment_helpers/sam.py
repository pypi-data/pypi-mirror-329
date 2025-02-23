from segment_anything import SamPredictor, sam_model_registry
from PIL import Image
import cv2
import numpy as np

#NEVERMIND SAM KIND OF SUCKS BECAUSE IT SEGMENTS THINGS BUT WE DONT KNOW WHAT EACH THING IS

pretrained_path="/scratch/jlb638/segment_checkpoints/sam_vit_h_4b8939.pth"

def sam_mask(image:Image.Image, sam_predictor:SamPredictor,prompt:str)->Image.Image:
    cv_img=np.array(image)
    sam_predictor.set_image(cv_img)
    masks, _, _ = sam_predictor.predict(prompt)
