import os
import sys
sys.path.append('/home/jlb638/Desktop/package')

from src.experiment_helpers.measuring import get_metric_dict
from PIL import Image

images=[Image.open("ArcaneJinx.jpg"),Image.open("nsfw.png")]

metric_dict=get_metric_dict(["girl","person"],images,images)
for k,v in metric_dict.items():
    print(k,v)