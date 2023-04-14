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
    grayscale = rgb2gray(image)
    deblured = cv2.GaussianBlur(grayscale, (5, 5), 0)

    angle = determine_skew(deblured)
    rotated = rotate(deblured, angle, resize=True) * 255
    io.imsave(image_path, rotated.astype(np.uint8))


def get_image_text(image_path):
    try:
        preprocess_image(image_path)
    except Exception:
        pass
    image = Image.open(image_path)

    model_name = "rus_htr"
    traineddata_dir = "tesseract_data"
    words_list_dir = "tesseract_data"

    cfg = rf"-l {model_name} --tessdata-dir {traineddata_dir} --user-words {words_list_dir} --psm 6 --oem 3"
    text = pytesseract.image_to_string(image, config=cfg)

    return text


def convert_images_to_text(images_path):
    lines_text = []
    for filename in os.listdir(images_path):
        for line in get_image_text(path_join(images_path, filename)).split('\n'):
            if line.strip():
                lines_text.append(line)

    return lines_text
