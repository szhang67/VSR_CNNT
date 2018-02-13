from os.path import exists, join, basename, abspath
from os import listdir
from scipy import interpolate
from PIL import Image
import cv2
import numpy as np
from numpy import array
from random import shuffle
from math import floor

def input_transform(im, upscale_factor):
    im_size = im.size
    im = im.resize((x / upscale_factor for x in im_size), resample=0)
    im = im.resize(im_size, Image.BICUBIC)
    # im = interpolate.interp2d(im_size[0], im_size[1], im, kind='cubic')
    return im

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in [".png", ".jpg", ".jpeg"])

def load_img(filename):
    img = Image.open(filename).convert('YCbCr')
    y, Cb, Cr = img.split()
    return y

def data_preprocess(upscale_factor, root_dir, preprocessed_dir):
    for x in listdir(root_dir):
        if is_image_file(x):
            filename = join(root_dir, x)
            input = load_img(filename)
            output = input_transform(input, upscale_factor)
            cv2.imwrite(join(preprocessed_dir, x) + '.jpg', array(output))#check if this is okay and totensor

def train_test_split(upscale_factor, root_dir, preprocessed_dir, split_ratio):
    data_preprocess(upscale_factor, root_dir, preprocessed_dir)
    file_list = listdir(abspath(preprocessed_dir))
    shuffle(file_list) #is it necessary since there is shuffle in dataloader
    split_idx = floor(len(file_list) * split)
    training = file_list[:split_idx]
    testing = file_list[split_idx:]
    return training, testing
#where to put totensor()
#do I need to save train and test data to a folder each time?
#if justing doing image SR, how many train/test