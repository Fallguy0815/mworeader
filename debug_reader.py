# -*- coding: utf-8 -*-
import time

global debug_mode
global final_time

def update():
    global debug_mode
    global final_time
    debug_mode = 1
    current_time= time.localtime()
    final_time = time.strftime("%Y_%m_%d__%H_%M_%S", current_time)
    return final_time