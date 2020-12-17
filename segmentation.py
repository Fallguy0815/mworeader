# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:23:58 2020

@author: johndoe
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median, quantiles


blue = (255,0,0)
green = (0, 255, 0)
red = (0 ,0 ,255)
graycolor = (128, 128, 128)
colors = [blue, red, green, graycolor]

def getSegmentations(gametype):
    segmentations = []
    loopBounds = [] # team, lance, pilots
    if (gametype == "preGameQP"):
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

def putText(img, text, pos):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255,255,255), 1)

def createStatsGraph(img, percentiles):
    # img[100:,0:,] = np.full((720, 1700), 255)
    cv2.rectangle(img,(0,590),(1920,820),(10,10,10),-1)
    #img[600:600+220,0:+1700] = np.ones((220,1700,3), np.uint8)
    team1 = percentiles[0]
    team2 = percentiles[0]
    
    team1.sort()
    team2.sort()
    
    mean1 = round(mean(team1),2)
    mean2 = round(mean(team2),2)
    
    med1 = round(median(team1),2)
    med2 = round(median(team2),2)

    q1 = quantiles(team1)
    q2 = quantiles(team2)
    
    line11 = "Avg: " + str(mean1) + " median: " + str(med1)
    line12 = "qs: " + str(q1)
    line21 = "Avg: " + str(mean2) + " median: " + str(med2)
    line22 = "qs: " + str(q2)
    
    
    print (line11 + line12)
    print (line21 + line22)
    

    putText(img, line11, (120,650))
    putText(img, line12, (120,680))
    putText(img, line21, (1500,650))
    putText(img, line22, (1500,680))
    
    
    data = []
    with plt.xkcd():
    # This figure will be in XKCD-style
        print(plt.style.available)            
        plt.style.use(['dark_background'])
        fig, ax = plt.subplots(figsize=(20, 4), dpi=50)
        ax.boxplot([team1,team2], vert=False, showmeans=True) #, cmap=cm.coolwarm)
        fig.canvas.draw()
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        open_cv_image = data[:, :, ::-1].copy()
        open_cv_image[np.where((open_cv_image==[0,0,0]).all(axis=2))] = [10,10,10]
    
    print(open_cv_image.shape)
    img[600:600+200,410:410+1000] = open_cv_image[:,:]
    return img



def getOverlay(screen, segs, pilotnames, pilotstats):
    percentiles = [[],[]]
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
                    percentile = int(stats['prank'].replace('%', ''))
                    percentiles[teamNr].append(percentile)
                cv2.putText(screen, output, (sPoint[0]+130, sPoint[1]+17), cv2.FONT_HERSHEY_TRIPLEX, 0.6, color, 1)
        
    createStatsGraph(screen, percentiles)
    return screen                    
    