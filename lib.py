# a dummy file to hold all shared libs and functions.
# use 'from lib import *' to use them

import numpy as np
import cv2 as cv
import pyautogui as gui
import time
import random

resolution = gui.size()

def findImage(ref_img, thresh=0.7):
    img = np.array(gui.screenshot())
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(ref_img, 0)
    w, h = template.shape[::-1]
    center = (-1, -1)

    coords = cv.matchTemplate(grayscale_img, template, cv.TM_CCOEFF_NORMED)

    locs = np.where(coords >= thresh)
    for pt in zip(*locs[::-1]):
        center = (pt[0] + int(w/2), pt[1] + int(h/2))
    return center