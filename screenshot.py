# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 12:11:27 2020

@author: johndoe
"""

import debug_reader
from PIL import ImageGrab
import win32gui
import numpy as np
import cv2
from time import sleep

def takeScreenshot(hwnd):    
    sleep(0.2)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    if (debug_reader.debug_mode):
        img.save("screenshot_PIL.png", format="PNG")

    pil_image = img.convert('RGB') 
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    if (debug_reader.debug_mode):
        cv2.imwrite("screenshot_CV2.png", open_cv_image)
    return open_cv_image
    