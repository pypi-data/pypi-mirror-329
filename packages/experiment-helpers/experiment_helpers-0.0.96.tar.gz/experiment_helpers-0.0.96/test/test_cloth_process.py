import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
import torch
from PIL import Image
from datasets import load_dataset
import torch
from torchvision.transforms import PILToTensor

from src.experiment_helpers.cloth_process import check_or_download_model,load_seg_model,get_palette,generate_mask
from src.experiment_helpers.clothing import get_segmentation_model,get_mask,clothes_segmentation


checkpoint="/scratch/jlb638/fashion_segmentation/cloth_segm.pth"

check_or_download_model(checkpoint)

device="cpu"

palette=get_palette(4)

net = load_seg_model(checkpoint, device=device)
for i,row in enumerate(load_dataset("jlbaker361/humans",split="train")):
    image=row["splash"] #Image.open("ArcaneJinx.jpg").convert("RGB")
    cloth_seg = generate_mask(image, net=net, device=device)
    segmentation_model=get_segmentation_model(device,torch.float32)
    '''tensor_img=PILToTensor()(image)
    tensor_img=tensor_img.to(torch.float32)
    cloth_seg=clothes_segmentation(image,segmentation_model,0)'''
    cloth_seg.save(f"segmented_{i}.jpg")
    if i>5:
        break
    #cloth_seg.save("masked_jinx.jpg")