# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:38:00 2020

@author: johndoe
"""

import debug_reader
import cv2
import os
from findWindow import findWindow
from screenshot import takeScreenshot
from scoreboardClassifier import determineScoreboard
from segmentation import getSegmentations
from segmentation import drawDebugRectangles
from segmentation import overlayResults
from ocr import applyOcr
from jarls import queryStructure

cv2.namedWindow('final', cv2.WINDOW_GUI_EXPANDED)
cv2.waitKey(1)

debug_reader.debug_mode = 1

while True:

    debug_reader.update()
    # 1) Find MWO window, set error and wait if not found
    hwnd = findWindow('mechwarrior online')
    if (not debug_reader.debug_mode and not hwnd):
        print("Mwo not found, waiting")
        cv2.waitKey(5000)
        continue
    # 2) take screenshot
    if(debug_reader.debug_mode):
        screen = cv2.imread("screenshot_debug.png")
    else:
        screen = takeScreenshot(hwnd)
    if(len(screen) < 30):
        print("Not a valid screenshot (mwo minimized?)")
        cv2.waitKey(3000)
        continue
    finalImage = screen.copy()

    # 3) convert to gray for OCR
    gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,150,255,cv2.THRESH_BINARY) # | cv2.THRESH_OTSU) # TODO: OTSU may actually hurt?
    gray = cv2.bitwise_not(img_bin) # ugly. Works because gray is 0/255 only
    # output image after we make sure we have a scoreboard in the picture
    os.mkdir(debug_reader.final_time)
    
    
    # 4) Determine screenshot-type
    scoreBoardType = determineScoreboard(gray)
    if (scoreBoardType != "preGameQP"):
        print("Invalid gametype (Not implemented yet) or no scoreboard visible")
        cv2.waitKey(3000)
        continue
    
    
    # dump gray image for later examination
    cv2.imwrite(debug_reader.final_time + "/screenshot_gray.png", gray)
    # 5) get segmentation for gametype
    segs = getSegmentations(scoreBoardType)
    if (segs == []):
        print("image segmentation not found")
        cv2.waitKey(3000)
        continue
    
    imgSeg = drawDebugRectangles(screen, segs)
    cv2.imwrite(debug_reader.final_time + "/segmented.png", imgSeg)
    
    # 6) get the actual pilot names
    pilotnames = applyOcr(gray, segs)

    # 7) get jarls list values
    pilotstats = queryStructure(pilotnames)
    
    # 8) put the final image together and show it
    finalImage = overlayResults(finalImage, segs, pilotnames, pilotstats)
    cv2.imshow('final', finalImage)
    cv2.imwrite(debug_reader.final_time + "/screenshot_final.png", finalImage)
    cv2.waitKey(5000)

    
    
    