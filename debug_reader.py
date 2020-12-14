# -*- coding: utf-8 -*-
import time

global debug_mode
global final_time
global overlayTitle

def update():
    global debug_mode
    global final_time
    current_time= time.localtime()
    final_time = time.strftime("%Y_%m_%d__%H_%M_%S", current_time)
    return final_time