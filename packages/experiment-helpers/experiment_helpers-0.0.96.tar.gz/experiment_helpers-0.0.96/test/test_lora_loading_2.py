import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
from src.experiment_helpers.better_ddpo_pipeline import BetterDefaultDDPOStableDiffusionPipeline
from src.experiment_helpers.lora_loading import save_lora_weights, load_lora_weights,save_pipeline_hf,get_pipeline_from_hf, fix_lora_weights
from peft import LoraConfig,PeftModel
from diffusers import StableDiffusionPipeline
from src.experiment_helpers.utils import print_trainable_parameters

lora_config = LoraConfig(
                r=4,
                lora_alpha=4,
                init_lora_weights="gaussian",
                target_modules=["to_k", "to_q", "to_v", "to_out.0"],)

fix_lora_weights("jlbaker361/ddpo_512_wikiart-subjects_dcgan")

pipeline=StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-base")
unet=pipeline.unet

print_trainable_parameters(unet)
unet=PeftModel.from_pretrained(unet,"jlbaker361/ddpo_512_wikiart-subjects_dcgan")
print_trainable_parameters(unet)
pipeline("prompt",num_inference_steps=2)
