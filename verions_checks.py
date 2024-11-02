import torch
import torchvision
import torchaudio

import timm
import huggingface_hub
import transformers
import diffusers
import kornia
import skorch
import lightning as lt
import sklearn

import numpy as np
import scipy as sc

import pandas as pd

import cv2
#import tensorflow as tf

print('Current Package Versions')
print(f'torch:  {torch.__version__}, CUDA: {torch.cuda.is_available()}')
print('torchaudio: ', torchaudio.__version__)
print('huggingface_hub: ', huggingface_hub.__version__)
print('transformers: ', transformers.__version__)
print('diffusers: ', diffusers.__version__)



