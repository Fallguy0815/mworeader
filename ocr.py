# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:20:24 2020

@author: johndoe
"""

import constants
import pytesseract
from pytesseract import Output
import cv2
import json

# gray: screenshot in binary
# segs: array of shape teams(2) * lances(3) * pilots(4) * points(2) * point(2)
#  points is upper left, lower right, each with x,y

def debugOutputString(text):
    if (constants.debugOutputConsole == 1):
        print(text)

def replaceKnownErrors(pa):
    retList = []
    with open("lut.json") as f:
        data = json.load(f)
        for pilot in pa:
            if pilot in data:
                debugOutputString(pilot + " ==>" + data[pilot])
                retList.append(data[pilot])
            else:
                retList.append(pilot)
    return retList




def toGray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #gray, img_bin = cv2.threshold(gray,150,255,cv2.THRESH_BINARY) # | cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
    gray, img_bin = cv2.threshold(gray,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
    gray = cv2.bitwise_not(img_bin) # ugly. Works because gray is 0/255 only
    return gray

def applyOcr(img, segs):
    if (constants.debugFakeInput == 1 and constants.skipocr == 1):
       return [[['Dasher', 'Dancer', 'Prancer', 'Vixen'], ['', '', '', ''], ['', '', '', '']], [['Comet', 'Cupid', 'Donner', 'Blitzen'], ['Rudolph', '', '', ''], ['', '', '', '']]]
    pilotnames = []
    index = 0
    with open("lut.json") as f:
        data = json.load(f)

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
                    colPn = img[xRange[0]:xRange[1], yRange[0]:yRange[1]]
                    pn = toGray(colPn.copy())
                    boxPn = colPn.copy()
                    text = pytesseract.image_to_string(pn, output_type=Output.DICT, config='--psm 7 -c preserve_interword_spaces=0 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')
                    text = text['text']
                    debugOutputString(text)
                    if (len(text) >= 2):
                        res = pytesseract.image_to_boxes(pn, output_type=Output.DICT, config='--psm 7 -c preserve_interword_spaces=0 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')
                        text = ""
                        # find spaces one character at a time
                        for num, char in enumerate(res['char']) :
                            if(len(res['char'])<3):
                                continue
                            text = text + char
                            (x1, y1, x2, y2) = (res['left'][num], res['top'][num], res['right'][num], res['bottom'][num])
                            cv2.rectangle(boxPn, (x1, y1), (x2, y2), (0, 255, 0), 1)
                            if (num+1 < len(res['char'])):
    
                                dist = res['left'][num+1] - res['right'][num]
                                
                                if ((char=="1" or char=="l") and dist >= 5 and dist <=6):
                                    dist = 4
                                for dummy in (range(int(dist/5))): # 5 Pixels for as a guess for a single space between any letter for now
                                    text = text + " "
                    else:
                        text = ""

                    if text in data:
                        debugOutputString(text + " ==>" + data[text])
                        text = data[text]
                    pNames.append(text)             
                    if (constants.debugOutputFiles):
                        cv2.imwrite(constants.finalTime + "/ocr_g_" + str(index) + "_" + text + ".png", pn)
                        cv2.imwrite(constants.finalTime + "/ocr_c_" + str(index) + "_" + text + ".png", colPn)
                        cv2.imwrite(constants.finalTime + "/ocr_b_" + str(index) + "_" + text + ".png", boxPn)
                        index = index + 1
                lNames.append(pNames)
            pilotnames.append(lNames) 
    return pilotnames

def getText(img, upperLeft, lowerRight):
    src = toGray(img[upperLeft[1]:lowerRight[1], upperLeft[0]:lowerRight[0]])
    text = pytesseract.image_to_string(src, config='--psm 7 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"')[:-2]
    return text
    