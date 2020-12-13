# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:20:24 2020

@author: johndoe
"""

import debug_reader
import pytesseract
from pytesseract import Output
import cv2



# gray: screenshot in binary
# segs: array of shape teams(2) * lances(3) * pilots(4) * points(2) * point(2)
#  points is upper left, lower right, each with x,y

def applyOcr(gray, segs):
    pilotnames = []
    index = 0
    for team in segs:
        lNames = []
        for lance in team:
            pNames = []
            for pilot in lance:
                # Pilot name:
                sPoint = pilot[0]
                ePoint = pilot[1]
                # tesseract expects x:y in reverse order than opencv
                yRange = [sPoint[0], ePoint[0]]
                xRange = [sPoint[1], ePoint[1]]
                pn = gray[xRange[0]:xRange[1], yRange[0]:yRange[1]]
                res = pytesseract.image_to_boxes(pn, output_type=Output.DICT, config='--psm 7 -c preserve_interword_spaces=0 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')
                text = ""
                # find spaces one character at a time
                for num, char in enumerate(res['char']) :
                    if(len(res['char'])<3):
                        continue
                    text = text + char
                    if (num+1 < len(res['char'])):
                        dist = res['left'][num+1] - res['right'][num]
                        if ((char=="1" or char=="l") and dist >= 4 and dist <=5):
                            dist = 3
                        for dummy in (range(int(dist/4))): # 4 Pixels for as a guess for a single space between any letter for now
                            text = text + " "
                
                index = index + 1
                pNames.append(text)
                if (debug_reader.debug_mode):
                    cv2.imwrite(debug_reader.final_time + "/ocr_" + str(index) + "_" + text + ".png", pn)
                
            lNames.append(pNames)
        pilotnames.append(lNames) 
    return pilotnames

def getText(img, upperLeft, lowerRight):
    src = img[upperLeft[1]:lowerRight[1], upperLeft[0]:lowerRight[0]]
    text = pytesseract.image_to_string(src, config='--psm 7 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')[:-2]
    return text
    