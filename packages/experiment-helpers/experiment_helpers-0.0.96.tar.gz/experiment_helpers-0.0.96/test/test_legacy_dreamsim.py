import os
import sys
sys.path.append('/home/jlb638/Desktop/package')

from src.experiment_helpers.legacy_dreamsim import dreamsim

dream_model, dream_preprocess = dreamsim(pretrained=True,cache_dir="/scratch/jlb638/dreamsim",device="cpu")