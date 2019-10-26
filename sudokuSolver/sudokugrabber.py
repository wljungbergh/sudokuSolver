import cv2 as cv 
import numpy as np 


def load_image(image_path):
    try:
        return cv2.load_image(image_path)
    except:
        return False

def preprocess_image(image):
    image = cv.medianBlur(image, 5)
    return image

if 