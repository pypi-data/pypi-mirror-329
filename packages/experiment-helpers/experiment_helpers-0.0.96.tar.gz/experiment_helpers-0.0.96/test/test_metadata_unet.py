from PIL import Image
import os
import sys
sys.path.append('/home/jlb638/Desktop/package')

from src.experiment_helpers.metadata_unet import *


from diffusers.utils import load_image, make_image_grid
from PIL import Image
import cv2
import numpy as np
import unittest
import torch

original_image = load_image(
    "https://hf.co/datasets/huggingface/documentation-images/resolve/main/diffusers/input_image_vermeer.png"
)

image = np.array(original_image)

low_threshold = 100
high_threshold = 200

image = cv2.Canny(image, low_threshold, high_threshold)
image = image[:, :, None]
image = np.concatenate([image, image, image], axis=2)
canny_image = Image.fromarray(image)

#TODO: test with/without controlnet, with/without both kinds of metadata (8 tests!)
num_metadata=5
num_metadata_3d=1
metadata_3d_channel_list=[4,8,16]
metadata_3d_input_channels=3
metadata_3d_dim=256

batch_size=2

n_control=6

metadata=torch.rand((batch_size,num_metadata))
metadata_3d=torch.rand((batch_size,num_metadata_3d, metadata_3d_input_channels, metadata_3d_dim, metadata_3d_dim, metadata_3d_dim))

class TestMeta(unittest.TestCase):
    def test_forward(self):
        for pipe_class in [DiffusionPipeline,StableDiffusionControlNetPipeline]:
            for use_metadata in [True,False]:
                for use_metadata_3d in [True,False]:
                    with self.subTest(pipe_class=pipe_class, use_metadata=use_metadata,use_metadata_3d=use_metadata_3d):
                        kwargs={"num_inference_steps":2,"prompt":"mona lisa"}
                        if pipe_class==DiffusionPipeline:
                            pipe=DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
                        else:
                            controlnet = [ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny") for _ in range(n_control)]
                            pipe=StableDiffusionControlNetPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",controlnet=controlnet)
                            kwargs["image"]=[canny_image for _ in range(n_control)]
                        pipe.unet=MetaDataUnet.from_unet(pipe.unet,use_metadata=use_metadata,
                            num_metadata=num_metadata, 
                            num_metadata_3d=num_metadata_3d, 
                            metadata_3d_channel_list=metadata_3d_channel_list,
                            metadata_3d_dim=metadata_3d_dim,
                            use_metadata_3d=use_metadata_3d)
                        if use_metadata:
                            kwargs["metadata"]=metadata
                        if use_metadata_3d:
                            kwargs["metadata_3d"]=metadata_3d
                        forward_metadata(pipe, **kwargs)
                        
                        
if __name__=="__main__":
    unittest.main()