# a file to hold all shared libs and functions.
# use 'from lib import *' to use them

import numpy as np
import cv2 as cv
import pyautogui as gui
import time
import random
import glob
import re

DEFAULT_GAME_RES = (1920, 1080)
DEFAULT_HUD_SCALE = 1.0
resolution = gui.size()
images = {}

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

# currently only supports 16:9 aspect ratio, fullscreen
def scale_images(res, hud_scale):
    for img in glob.glob('./assets/img/*.png'):
        key = re.search('img\\\\(.*)\.png', img)[1]
        print(key)
        image = cv.imread(img, 0)
        if res != DEFAULT_GAME_RES or hud_scale != DEFAULT_HUD_SCALE:
            scale = res[0] / DEFAULT_GAME_RES[0]
            dims = np.flip(tuple(int(round(s * scale * hud_scale)) for s in image[::-1].shape))
            image = cv.resize(image, dims, interpolation=cv.INTER_AREA)
        images[key] = image