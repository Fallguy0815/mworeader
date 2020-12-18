# -*- coding: utf-8 -*-
import time

global finalTime
global overlayTitle

# set from mwoReader
global debugOutputFiles
global debugOutputConsole
global debugWindow
global debugMoveWindow

global debugFakeInput
global skipjarl
global skipocr

global overlay
global overlayTitle



def updateTimestamp():
    global debugMode
    global finalTime
    currentTime= time.localtime()
    finalTime = time.strftime("%Y_%m_%d__%H_%M_%S", currentTime)
    return finalTime