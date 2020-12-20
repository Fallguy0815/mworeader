# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:20:24 2020

@author: johndoe
"""

import pytesseract
from pytesseract import Output
import cv2
import sys

# gray: screenshot in binary
# segs: array of shape teams(2) * lances(3) * pilots(4) * points(2) * point(2)
#  points is upper left, lower right, each with x,y


def toGray(img, threshold):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY) # | cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
    gray = cv2.bitwise_not(img_bin) # ugly. Works because gray is 0/255 only
    return gray


img = cv2.imread('ocr_g_0_Eidreft.png')
for i in range(255):
    pn = toGray(img.copy(),i)
    text = pytesseract.image_to_string(pn, output_type=Output.DICT, config='--psm 7 -c preserve_interword_spaces=0 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')
    text = text['text'][:-2]
    if (text == "Eidreff"):
        print (str(i) + text)
sys.exit(0)

