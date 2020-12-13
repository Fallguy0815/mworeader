# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:39:32 2020

@author: johndoe
"""

from findWindow import findWindow
import debug_reader
import win32gui
import winxpgui
import win32con
import win32api
import time
import cv2

def hideOverlay():
    hwndCv = findWindow(debug_reader.overlayTitle)
    wndLongStyle = win32gui.GetWindowLong(hwndCv, win32con.GWL_STYLE)
    wndLongStyle = wndLongStyle & (~(win32con.WS_VISIBLE))
    win32gui.SetWindowLong(hwndCv,win32con.GWL_STYLE,wndLongStyle)
    win32gui.SetWindowPos(hwndCv,1, 1,1,2,2, win32con.SWP_HIDEWINDOW)
    

def createOverlay(hwnd, imgOverlay):
    bbox = win32gui.GetWindowRect(hwnd)
    time.sleep(0.2)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    if (height < 10 or width < 10):
        return
    
    
    hwndCv = findWindow(debug_reader.overlayTitle)
    cv2.resizeWindow(debug_reader.overlayTitle,width,height)
    
    wndLongEx = win32gui.GetWindowLong(hwndCv, win32con.GWL_EXSTYLE)
    additionalStyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE
    wndLongEx = wndLongEx | additionalStyle 
    wndLongStyle = win32con.WS_VISIBLE | win32con.WS_POPUP
    win32gui.SetWindowLong(hwndCv, win32con.GWL_EXSTYLE, wndLongEx)
    win32gui.SetWindowLong(hwndCv, win32con.GWL_STYLE, wndLongStyle)
    win32gui.SetWindowPos(hwndCv,-1, bbox[0], bbox[1], width, height, 0)
    winxpgui.SetLayeredWindowAttributes(hwndCv, win32api.RGB(0,0,0), 255, win32con.LWA_COLORKEY )
    cv2.imshow(debug_reader.overlayTitle,imgOverlay)
    cv2.waitKey(1)
    