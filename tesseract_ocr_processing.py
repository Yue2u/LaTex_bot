import pytesseract
import numpy as np
import cv2
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew
from PIL import Image

import os
from utils import path_join


def preprocess_image(image_path):
    image = np.array(Image.open(image_path))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, image = cv2.threshold(image, 95, 255, cv2.THRESH_BINARY)    
    image = cv2.GaussianBlur(image, (7, 7), 0)
    io.imsave(image_path, image.astype(np.uint8))


def get_image_text(image_path):
    preprocess_image(image_path)
    image = Image.open(image_path)

    model_name = "rus_htr_2"
    traineddata_dir = "tesseract_data"
    words_list_dir = "tesseract_data"

    cfg = rf"-l {model_name} --tessdata-dir {traineddata_dir} --user-words {words_list_dir} --psm 6 --oem 3"
    text = pytesseract.image_to_string(image, config=cfg)

    return text


def convert_images_to_text(images_path):
    lines_text = []
    for filename in os.listdir(images_path):
        for line in get_image_text(path_join(images_path, filename)).split("\n"):
            if line.strip():
                lines_text.append(line)

    return lines_text
