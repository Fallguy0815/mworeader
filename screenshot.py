# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 12:11:27 2020

@author: johndoe
"""

from PIL import ImageGrab
import win32gui
import numpy as np
import constants
from time import sleep

def takeScreenshot(hwnd):    
    sleep(0.2)
    open_cv_image = []
    try:
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)

        pil_image = img.convert('RGB') 
        open_cv_image = np.array(pil_image) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy()
    except:
        if(constants.debugOutputConsole ==1):
            print("hwnd (MWO) invalid during screenshot")
            
    return open_cv_image
    