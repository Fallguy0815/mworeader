# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:23:58 2020

@author: johndoe
"""

import cv2
import numpy as np

blue = (255,0,0)
green = (0, 255, 0)
red = (0 ,0 ,255)
graycolor = (128, 128, 128)
colors = [blue, red, green, graycolor]

def getSegmentations(gametype):
    segmentations = []
    
    if (gametype == "preGameQP"):
        start = np.array([350,200])
        box = np.array([292,24])
        end = start + box
        current = np.copy(start)

        for teams in range(2):
            lBoxes = []
            for lances in range(3):
                pBoxes = []
                for pilots in range(4):
                    end = current + box
                    # Pilot name box: 
                    pBoxes.append([np.copy(current), np.copy(end)])
                    current[1] = current[1] + box [1] + 2

                lBoxes.append(pBoxes)                                    
                current[1] = current[1] + 2
            segmentations.append(lBoxes)
            current = np.copy(start)
            current[0] = current[0] + 960
                    

        return segmentations
    # Game mode not found:
    return []


def drawDebugRectangles(img, segmentations):    
    index = 0
    for team in segmentations:
        for lance in team:
            for pilot in lance:
                sPoint = pilot[0]
                ePoint = pilot[1]
                index = index + 1
                cv2.rectangle(img,tuple(sPoint), tuple(ePoint), colors[index%4], 2)

    return img

def overlayResults(screen, segs, pilotnames, pilotstats):
    for teamNr in range(2):
        for lanceNr in range(3):
            for pilotNr in range(4):
                ocrName = pilotnames[teamNr][lanceNr][pilotNr]
                stats = pilotstats.get(ocrName, "XX")
                sPoint = segs[teamNr][lanceNr][pilotNr][0]
                output = ""
                color = (0,0,0)
                if (stats=="XX" or stats["rank"] == "Not Found"):
                    output = ocrName + "-??"
                    color = red
                else:
                    color = green
                    output = stats["rank"] + "(" + stats["prank"] + ")" #DEBUG  W/L: " + stats["wlr"] + ", K/D: " + stats["kd"]
                cv2.putText(screen, output, (sPoint[0]+130, sPoint[1]+17), cv2.FONT_HERSHEY_TRIPLEX, 0.6, color, 1)
    return screen                    
    