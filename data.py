from os.path import exists, join, basename
from os import listdir
from scipy import interpolate
from PIL import Image
import cv2
import numpy as np
from numpy import array

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

root_dir = "/home/szhang67/data/raw_data"
preprocessed_dir = "/home/szhang67/data/preprocessed"

upscale_factor = 4
for x in listdir(root_dir):
    if is_image_file(x):
        filename = join(root_dir, x)
        input = load_img(filename)
        output = input_transform(input, upscale_factor)
        cv2.imwrite(join(preprocessed_dir, x) + '.jpg', array(output))

