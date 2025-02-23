import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
from src.experiment_helpers.clothing import get_segmentation_model,clothes_segmentation
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from torchvision.transforms import PILToTensor,Normalize
import torch

# Load an image from a URL
good_image_url_list=[
"https://familydoctor.org/wp-content/uploads/2018/02/41808433_l-848x566.jpg",
"https://sites.nd.edu/manuscript-studies/files/2020/12/47827af98c5ae74189cbf0c5617b452f.png",
"https://thumbs.dreamstime.com/b/full-body-confident-happy-black-woman-standing-white-background-portrait-118890037.jpg",
"https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/handsome-man-in-white-t-shirt-full-body-michal-bednarek.jpg"
]

bad_image_url_list=[
"https://getwallpapers.com/wallpaper/full/3/9/2/719130-beautiful-horse-wallpaper-2560x1440-samsung.jpg",
"https://www.pixelstalk.net/wp-content/uploads/2016/06/Free-Download-HD-Car-Wallpapers-Desktop.jpg",
"https://www.pixelstalk.net/wp-content/uploads/2016/10/Forest-Wallpaper-For-Home.jpg",
"https://www.pixelstalk.net/wp-content/uploads/images6/Fire-Desktop-Wallpaper-620x413.jpg"
]

for name,image_url_list in zip(["good!!!","bad!!!"],[good_image_url_list,bad_image_url_list]):
    print(name)
#image_url = 'https://getwallpapers.com/wallpaper/full/3/9/2/719130-beautiful-horse-wallpaper-2560x1440-samsung.jpg'  # Replace with your image URL
    for image_url in image_url_list:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert('RGB')

        model=get_segmentation_model("cpu",torch.float32)
        segmented=clothes_segmentation(image,model,5)

        #segmented.save("segment.jpg")