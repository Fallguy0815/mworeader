# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:39:32 2020

@author: johndoe
"""

from findWindow import findWindow
import constants
import win32gui
import winxpgui
import win32con
import win32api
import time
import cv2
from PIL import Image
import numpy as np




def hideOverlay():
    if(constants.overlay != 1):
        return
    hwndCv = findWindow(constants.overlayTitle)
    wndLongStyle = win32gui.GetWindowLong(hwndCv, win32con.GWL_STYLE)
    wndLongStyle = wndLongStyle & (~(win32con.WS_VISIBLE))
    win32gui.SetWindowLong(hwndCv,win32con.GWL_STYLE,wndLongStyle)
    win32gui.SetWindowPos(hwndCv,1, 1,1,2,2, win32con.SWP_HIDEWINDOW)
    

def createOverlay(hwnd, imgOverlay):
    if (constants.debugOutputConsole == 1):
        print("Overlay: start")
        plc = win32gui.GetWindowPlacement(hwnd)
        # TODO: Find a "real" way to test if MWO is running Fullscreen or FullWindowed
        if (plc[0] != 2 or plc[1] != 3):
            print("******* Overlay: Does not work on fullscreen MWO ******")

    if (constants.overlay != 1):
        return
    bbox = win32gui.GetWindowRect(hwnd)
    time.sleep(0.2)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    if (height < 10 or width < 10):
        if (constants.debugOutputConsole == 1):
            print("Overlay: height/width < 10, aborting")
        return
    
    
    hwndCv = findWindow(constants.overlayTitle)
    cv2.resizeWindow(constants.overlayTitle,width,height)
    
    wndLongEx = win32gui.GetWindowLong(hwndCv, win32con.GWL_EXSTYLE)
    additionalStyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE
    wndLongEx = wndLongEx | additionalStyle 
    wndLongStyle = win32con.WS_VISIBLE | win32con.WS_POPUP
    win32gui.SetWindowLong(hwndCv, win32con.GWL_EXSTYLE, wndLongEx)
    win32gui.SetWindowLong(hwndCv, win32con.GWL_STYLE, wndLongStyle)
    win32gui.SetWindowPos(hwndCv,-1, bbox[0], bbox[1], width, height, 0)
    winxpgui.SetLayeredWindowAttributes(hwndCv, win32api.RGB(0,0,0), 255, win32con.LWA_COLORKEY )
    if (constants.debugOutputConsole == 1):
        print("Overlay: set visible")

    cv2.imshow(constants.overlayTitle,imgOverlay)
    cv2.waitKey(1)
    
    
def combineOverlay(image_src, overlay):
    # alpha blending in PIL with some mumbo jumbo to convert between PIL and CV2 color-spaces
    rgba_b = cv2.cvtColor(image_src, cv2.COLOR_RGB2RGBA)
    rgba_b[:, :, 3] = np.full((1080, 1920), 255)


    rgba_f = cv2.cvtColor(overlay, cv2.COLOR_RGB2RGBA)
    mask = cv2.cvtColor(overlay, cv2.COLOR_RGB2GRAY)
    mask, img_bin = cv2.threshold(mask,3,255,cv2.THRESH_BINARY)
    mask = cv2.bitwise_not(img_bin)
    mask = cv2.bitwise_not(mask)
    rgba_f[:, :, 3] = mask
    rgba_f = cv2.cvtColor(rgba_f, cv2.COLOR_BGRA2RGBA)
    rgba_b = cv2.cvtColor(rgba_b, cv2.COLOR_BGRA2RGBA)


    background = Image.fromarray(rgba_b, mode='RGBA')
    foreground = Image.fromarray(rgba_f, mode='RGBA')
    pil_result = Image.alpha_composite(background, foreground)

    if (constants.debugOutputFiles == 1):
        background.save(constants.finalTime + '/background.png')
        foreground.save(constants.finalTime + '/foreground.png')
        pil_result.save(constants.finalTime + "/combined_image.png")
    pil_ret = np.array(pil_result.convert('RGB')) 
    open_cv_image = pil_ret[:, :, ::-1].copy()
    return open_cv_image
    
