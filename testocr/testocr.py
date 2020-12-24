# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:20:24 2020

@author: johndoe
"""

import pytesseract
from pytesseract import Output
import numpy as np
import cv2
import sys
import time

# gray: screenshot in binary
# segs: array of shape teams(2) * lances(3) * pilots(4) * points(2) * point(2)
#  points is upper left, lower right, each with x,y


def toGray(img, threshold):
	g1 = img.copy()
	g1 = cv2.cvtColor(g1, cv2.COLOR_RGB2GRAY)
	thotsu = 0
	g1, img_bin1 = cv2.threshold(g1,thotsu,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
	print("otsu says :" + str(g1))
	
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	thresh, img_bin = cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY) # | cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
	gray = cv2.bitwise_not(img_bin) # ugly. Works because gray is 0/255 only
	return gray


img = cv2.imread('ocr_c_debug.png')
threshold = 128
img = cv2.resize(img,(img.shape[1]*4, img.shape[0]*4), interpolation = cv2.INTER_LANCZOS4)
while True:
	pn = toGray(img.copy(),threshold)
	print(pn.shape[0])
	print(pn.shape[1])
	free = np.zeros((60 + pn.shape[0],60 + pn.shape[1]))
	print (free.shape[0])
	print (free.shape[1])
	free[30:30+pn.shape[0],30:30+pn.shape[1]] = pn

	
	#text = pytesseract.image_to_string(pn, output_type=Output.DICT, config='--psm 7 -c preserve_interword_spaces=0 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')
	#text = text['text'][:-2]
	cv2.imshow('threshold', free)
	key = cv2.waitKeyEx(0)
	print(str(key))
	if (key == 2555904): # right
		threshold = threshold + 1
	if (key == 2424832): #left
		threshold = threshold - 1
	if (key == 2490368): #up
		threshold = threshold + 10
	if (key == 2621440):
		threshold = threshold - 10
	if (key == 13):
		sys.exit(0)
	print("new threshold: " + str(threshold))
sys.exit(0)

