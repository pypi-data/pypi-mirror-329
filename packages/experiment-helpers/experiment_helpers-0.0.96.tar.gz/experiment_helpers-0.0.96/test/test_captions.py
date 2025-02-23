import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
import torch

from facenet_pytorch import MTCNN
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from src.experiment_helpers.clothing import get_segmentation_model,clothes_segmentation
from src.experiment_helpers.measuring import get_face_caption,get_fashion_caption

device="cpu"
if torch.cuda.is_available():
    device="cuda"
mtcnn=MTCNN(device=device)
segmentation_model=get_segmentation_model(device=device,dtype=torch.float32)


images=[Image.open("ArcaneJinx.jpg"),Image.open("walz.jpg")]

blip_processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
blip_conditional_gen = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b").eval()

for image in images:
    face=get_face_caption(image,blip_processor,blip_conditional_gen,mtcnn,10)
    fashion=get_fashion_caption(image,blip_processor,blip_conditional_gen,segmentation_model,0)
    print("face",face)
    print("fashion",fashion)