import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
from accelerate import Accelerator

from src.experiment_helpers.ip_attention_value import load_ip_adapter_single


image =Image.open("ArcaneJinx.jpg")

accelerator=Accelerator(log_with="wandb",gradient_accumulation_steps=4)
accelerator.init_trackers(project_name="testing_bullshit")




for v in ["key","value","vanilla","ip"]:
    print(v)
    gen=torch.Generator().manual_seed(42)
    pipeline=StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

    if v=="key" or v=="value":

        load_ip_adapter_single(pipeline,"h94/IP-Adapter", subfolder="models", weight_name="ip-adapter_sd15.bin",variant=v)
        pipeline.set_ip_adapter_scale(0.9)
    elif v=="ip":
        pipeline.load_ip_adapter("h94/IP-Adapter", subfolder="models", weight_name="ip-adapter_sd15.bin")
        pipeline.set_ip_adapter_scale(0.9)

    pipeline=pipeline.to(accelerator.device)

    if v=="vanilla":
        new_image=pipeline("going for a walk", num_inference_steps=30).images[0]
    else:

        new_image=pipeline("going for a walk", num_inference_steps=30, ip_adapter_image=image).images[0]

    new_image.save(f"ip_test_{v}.jpg")


