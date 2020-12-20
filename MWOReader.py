# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:38:00 2020

@author: johndoe
"""

import constants
import cv2
import os
import numpy as np
from time import localtime, mktime, sleep
from findWindow import findWindow
from screenshot import takeScreenshot
from scoreboardClassifier import determineScoreboard
from segmentation import getSegmentations
from segmentation import drawDebugRectangles
from segmentation import getOverlay
from ocr import applyOcr
from jarls import queryStructure
from overlay import createOverlay
from overlay import hideOverlay
from overlay import combineOverlay

constants.debugOutputFiles = 0
constants.debugOutputConsole = 1
constants.debugFakeInput = 0
constants.debugWindow = 1
constants.debugMoveWindow = 1
constants.overlay = 1
constants.skipjarl = 0
constants.skipocr = 0
constants.overlayTitle = "a0e28dbb-1273-464e-b1ad-e5acc1ecb4fb"

firstNVSmessage = 1


def debugOutputString(text):
    if (constants.debugOutputConsole == 1):
        print(text)

if (constants.debugWindow == 1):
    cv2.namedWindow('final', cv2.WINDOW_GUI_EXPANDED | cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO )
    cv2.waitKey(1)
    if (constants.debugMoveWindow  == 1):
        cv2.moveWindow('final', 1921, 0) # Move to the right monitor
        cv2.waitKey(1)

if (constants.overlay == 1):
    cv2.namedWindow(constants.overlayTitle, cv2.WINDOW_GUI_NORMAL)
    cv2.waitKey(1)


hideOverlay()
lastTime = 0.0
while True:
    constants.updateTimestamp()
    # 1) Find MWO window, set error and wait if not found
    hwnd = findWindow('mechwarrior online')
    if (not constants.debugFakeInput == 1  and not hwnd):
        debugOutputString("Mwo not found, waiting")
        hideOverlay()
        cv2.waitKey(5000)
        continue
    # 2) take screenshot
    if(constants.debugFakeInput == 1):
        debugOutputString("using debug screen")
        screen = cv2.imread("screenshot_debug.png")
    else:
        screen = takeScreenshot(hwnd)
    
    if(len(screen) < 30):
        debugOutputString("Not a valid screenshot (mwo minimized?) ")
        hideOverlay()
        cv2.waitKey(3000)
        continue
    finalImage = screen.copy()
    ocrImage = screen.copy()

    
    # 3) Determine screenshot-type
    scoreBoardType = determineScoreboard(screen)
    if (scoreBoardType == ""):
        if (constants.debugOutputConsole == 1):
            if (firstNVSmessage == 1):
                print("Invalid gametype (Not implemented yet) or no scoreboard visible")
                firstNVSmessage = 0
            else:
                print(".",end='', flush=True)
                sleep(1)
        hideOverlay()
        cv2.waitKey(1500)
        continue
    firstNVSmessage = 1
    if(mktime(localtime())-lastTime < 180.0):
       debugOutputString("last ocr scoreboard photo was taken less than 3 minutes ago, assume still the same game")
       cv2.waitKey(1500)
       continue
    
    # dump gray image for later examination
    if (constants.debugOutputFiles):
        os.mkdir(constants.finalTime)
        cv2.imwrite(constants.finalTime + "/screenshot_color.png",finalImage)
    # 4) get segmentation for gametype
    segs = getSegmentations(scoreBoardType)
    if (segs == []):
        debugOutputString("image segmentation not found")
        hideOverlay()
        cv2.waitKey(3000)
        continue
    
    imgSeg = drawDebugRectangles(screen, segs)
    if (constants.debugOutputFiles == 1):
        cv2.imwrite(constants.finalTime + "/segmented.png", imgSeg)
    
    
    # 5) get the actual pilot names
    pilotnames = applyOcr(ocrImage, segs)

    # 6) get jarls list values
    pilotstats = queryStructure(pilotnames)
    
    # 7) put the final image together and show it
    imgOverlay = np.zeros((1080,1920,3), np.uint8)
    imgOverlay = getOverlay(imgOverlay, segs, pilotnames, pilotstats)
    if (constants.debugOutputFiles):
        cv2.imwrite(constants.finalTime + "/overlay.png", imgOverlay)
    if (constants.debugWindow == 1):
        combined = combineOverlay(finalImage, imgOverlay)
        sb = combined[30:820,80:1780]
        cv2.imshow('final', sb)
    if (constants.overlay == 1):
        createOverlay(hwnd, imgOverlay)
    lastTime = mktime(localtime())
    cv2.waitKey(3000)
    
    
    
    