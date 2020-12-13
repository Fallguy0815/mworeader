# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:39:32 2020

@author: johndoe
"""

import win32gui

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def findWindow(windowName):
    windowName = windowName.lower()
    win32gui.EnumWindows(enum_cb, toplist)
    wnd = [(hwnd, title) for hwnd, title in winlist if windowName in title.lower()]
    
    if(not wnd):
        return wnd
    else:
        return wnd[0][0]
