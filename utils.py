# A file to hold all shared libs and functions.
# Use 'from util import *' to use them

from cv2 import INTER_LINEAR
import numpy as np
import cv2 as cv
import pyautogui as gui
import time
import random
import glob
import re

DEFAULT_GAME_RES = (1920, 1080)
DEFAULT_HUD_SCALE = 1.0
ROOM2_TIME_LIMIT = 120
resolution = gui.size()
images = {}

# Change these parameters according to your game options
game_res = (1920, 1080)
# Hud scaling isn't quite accurate...
hud_scale = 1.0

def findImage(ref_img, thresh=0.7):
    ''' Find an image using openCV template matching.
    
            ### Parameters:
                `ref_img` (string): filename of target image
                `thresh` (float): how lenient/strict the matcher should be, default of 0.7
            
            ### Returns:
                `center` (tuple): (x, y) coords of the center of found image
    '''
    img = np.array(gui.screenshot())
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = images[ref_img]
    w, h = template.shape[::-1]
    center = (-1, -1)

    coords = cv.matchTemplate(grayscale_img, template, cv.TM_CCOEFF_NORMED)

    locs = np.where(coords >= thresh)
    for pt in zip(*locs[::-1]):
        center = (pt[0] + int(w/2), pt[1] + int(h/2))
    return center

# Currently only supports fullscreen
def scale_images():
    ''' Scale asset images to expected resolution/HUD scale. '''
    for img in glob.glob('./assets/img/*.png'):
        key = re.search('img\\\\(.*)\.png', img)[1]
        image = cv.imread(img, 0)
        if game_res != DEFAULT_GAME_RES or hud_scale != DEFAULT_HUD_SCALE:
            scale_x = game_res[0] / DEFAULT_GAME_RES[0]
            scale_y = scale_x
            # Only scale y by 16:9 equivalent
            if re.search('\_h$', key) == None:
                scale_x *= hud_scale
                if key != 'map_frame_offset':
                    scale_y *= hud_scale
            interp = cv.INTER_AREA
            if game_res[0] > DEFAULT_GAME_RES[0] or game_res[1] > DEFAULT_GAME_RES[1]:
                interp = cv.INTER_LINEAR
            image = cv.resize(image, None, fx=scale_x, fy=scale_y, interpolation=interp)
        if re.search('_h$', key) != None:
            key = key[:-2]
        images[key] = image
        
