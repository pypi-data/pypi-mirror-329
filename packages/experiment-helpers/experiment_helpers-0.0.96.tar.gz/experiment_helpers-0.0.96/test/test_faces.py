import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
from src.experiment_helpers.elastic_face_iresnet import face_mask
from facenet_pytorch import MTCNN

from PIL import Image

src=Image.open("ArcaneJinx.jpg")
mtcnn=MTCNN(device="cpu")
masked=face_mask(src,mtcnn,10)
masked.save("masked_jinx.jpg")