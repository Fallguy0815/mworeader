# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:12:19 2020

@author: johndoe
"""

from ocr import getText

def determineScoreboard(gray):
    upperLeft = [80,35]
    lowerRight = [445, 85]
    text = getText(gray, upperLeft, lowerRight)
    # Do not test for full string (DROP PREPARATION, because on Witer maps the first part gets obscured)
    if (text[-8:] == "PARATION"):
        upperLeft = [320,560]
        lowerRight = [465, 595]
        text = getText(gray, upperLeft, lowerRight)
        if (text == "Solaris"):
            return "preGameSolaris"
        else:
            return "preGameQP"
    else:
        return ""