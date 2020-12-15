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
    loopBounds = [] # team, lance, pilots
    if (gametype == "preGameQp"):
        loopBounds = [2,3,4]
    if (gametype == "preGameSolaris"):
        loopBounds = [2,1,2]
    if (loopBounds == []):
        return loopBounds # gametype not defined
    start = np.array([350,200])
    box = np.array([292,24])
    end = start + box
    current = np.copy(start)

    for teams in range(loopBounds[0]):
        lBoxes = []
        for lances in range(loopBounds[1]):
            pBoxes = []
            for pilots in range(loopBounds[2]):
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

def getOverlay(screen, segs, pilotnames, pilotstats):
    print(len(segs))
    for teamNr in range(len(segs)):
        for lanceNr in range(len(segs[teamNr])):
            for pilotNr in range(len(segs[teamNr][lanceNr])):
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
    