#!/usr/bin/python3
# coding: utf-8
# author : Irham Mustofa Kamil
# github : github.com/irhammusthofa


import pytesseract
import os
import argparse
import cv2 as cv
import re
import statistics
try:
    import Image, ImageOps, ImageEnhance, imread
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance

def solve_captcha(path):

    """
    Convert a captcha image into a text, 
    using PyTesseract Python-wrapper for Tesseract
    Arguments:
        path (str):
            path to the image to be processed
    Return:
        'textualized' image
    """
    #image = Image.open(path).convert('RGB')
    #image = ImageOps.autocontrast(image, cutoff = 100)
    #image = ImageEnhance.Contrast(image).enhance(500)
    image = cv.imread(path,0)
    
    th, threshed1 = cv.threshold(image,100,255,cv.THRESH_BINARY)
    th, threshed2 = cv.threshold(image,110,255,cv.THRESH_BINARY)
    th, threshed3 = cv.threshold(image,120,255,cv.THRESH_BINARY)
    th, threshed4 = cv.threshold(image,150,255,cv.THRESH_BINARY)

    filename = "{}.png".format("bni_resolver")
    cv.imwrite(filename,threshed1)
    #image.save(filename)

    text1 = pytesseract.image_to_string(threshed1)
    text2 = pytesseract.image_to_string(threshed2)
    text3 = pytesseract.image_to_string(threshed3)
    text4 = pytesseract.image_to_string(threshed4)

    lst = []
    result = ""
    
    if text1:
        text1 = re.findall("\d+", text1)[0]
        lst.append(text1)
    if text2:
        text2 = re.findall("\d+", text2)[0]
        lst.append(text2)
    if text3:
        text3 = re.findall("\d+", text3)[0]
        lst.append(text3)
    if text4:
        text4 = re.findall("\d+", text4)[0]
        lst.append(text4)

    if lst:
        result = statistics.mode(lst)


    return result



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
    args = vars(argparser.parse_args())
    path = args["image"]
    #print('-- Resolving')
    captcha_text = solve_captcha(path)
    if captcha_text:
        print(captcha_text)
    else:
        print("Failed")
