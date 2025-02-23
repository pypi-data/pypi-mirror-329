import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
import torch

from segment_anything import SamPredictor, sam_model_registry
from PIL import Image
sam = sam_model_registry["<model_type>"](checkpoint="<path/to/checkpoint>")
predictor = SamPredictor(sam)
#predictor.set_image(<your_image>)