import numpy as np
import cv2 as cv
import pyautogui as gui
import time
import random

# for exiting script
import keyboard
from multiprocessing import Process

LOAD_IN_TIME = 9
LOAD_OUT_TIME = 26
CHAOS_TIME = 50
DEFENSIVE = ['d']
AOE = ['w', 's']
OTHER = ['a', 'f']
resolution = gui.size()

def findImage(ref_img):
    img = np.array(gui.screenshot())
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(ref_img, 0)
    w, h = template.shape[::-1]
    center = (-1, -1)

    coords = cv.matchTemplate(grayscale_img, template, cv.TM_CCOEFF_NORMED)
    thresh = 0.7

    locs = np.where(coords >= thresh)
    for pt in zip(*locs[::-1]):
        center = (pt[0] + int(w/2), pt[1] + int(h/2))
    return center

def clickConfirm(ref_img):
    x, y = findImage(ref_img)
    gui.moveTo(x, y)
    gui.move(random.randint(1, 5), 0)
    gui.click()
    time.sleep(random.uniform(0.15, 0.30))
    gui.keyDown('enter')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('enter')

def rotation():
    align()
    # while (findImage('./assets/img/portal.png') == (-1, -1)):
    for i in range(3):
        # one-shot burst
        gui.moveTo(resolution[0]/2 - 200, resolution[1]/2 - 150)
        gui.keyDown('w')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('w')
        # cast time
        time.sleep(random.uniform(0.6, 0.8))

        kite()
        # one-shot burst
        gui.moveTo(resolution[0]/2 - 200, resolution[1]/2 - 150)
        gui.keyDown('s')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('s')
        gui.keyDown('s')
        time.sleep(random.uniform(0.075, 0.125))
        gui.keyUp('s')
        # cast time
        time.sleep(random.uniform(1.75, 2.0))

        kite()
        # defensive
        gui.keyDown('d')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('d')
        # cast time
        time.sleep(random.uniform(0.25, 0.5))
        
        # other (turret)
        gui.keyDown('f')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('f')
        # cast time
        time.sleep(random.uniform(0.75, 1.0))
        
        # mini burst
        gui.moveTo(resolution[0]/2 - 200, resolution[1]/2 - 100)
        gui.keyDown('a')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('a')
        # cast time
        time.sleep(random.uniform(0.6, 0.8))
        
        # dot
        gui.keyDown('r')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('r')
        # cast time
        time.sleep(random.uniform(1.25, 1.5))
        
        # kite()
        
        # wait for cds
        # time.sleep(random.uniform(4.5, 5.0))
    # one-shot burst
    gui.moveTo(resolution[0]/2 - 200, resolution[1]/2 - 150)
    gui.keyDown('w')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('w')
    # cast time
    time.sleep(random.uniform(2.0, 2.5))

def kite():
    l = 900
    l2 = 400
    x, y = (resolution[0]/2, resolution[1]/2)
    # up
    x1, y1 = (x, y-l2)
    # left
    x2, y2 = (x-l, y)
    # down
    x3, y3 = (x, y+l2)
    # right
    x4, y4 = (x+l, y)
    
    gui.moveTo(x1, y1)
    gui.click(button='right')
    time.sleep(1.0)

    gui.moveTo(x2, y2)
    gui.click(button='right')
    time.sleep(1.25)
    
    gui.moveTo(x3, y3)
    gui.click(button='right')
    time.sleep(1.0)
    
    gui.moveTo(x4, y4)
    gui.click(button='right')
    time.sleep(1.25)
    
def align():
    l = 600
    l2 = 400
    x, y = (resolution[0]/2, resolution[1]/2)
    # down
    x3, y3 = (x, y+l2)
    # right
    x4, y4 = (x+l, y)
    gui.moveTo(x3, y3)
    gui.click(button='right')
    time.sleep(0.75)
    gui.moveTo(x4, y4)
    gui.click(button='right')
    time.sleep(0.5)

def repair(ref_img):
    x, y = findImage(ref_img)
    if x > -1:
        gui.keyDown('alt')
        gui.keyDown('p')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('p')
        gui.keyUp('alt')
        time.sleep(random.uniform(1.5, 2.0))
        clickConfirm('./assets/img/pet.png')
        time.sleep(random.uniform(0.5, 1.0))
        clickConfirm('./assets/img/repair.png')
        gui.keyDown('esc')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('esc')
    print('armor\'s all good!')
    
def calc_map_center(bar_img):
    img = np.array(gui.screenshot())
    grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(bar_img, 0)
    template_offset = cv.imread('./assets/img/map_frame_offset.png', 0)
    template_map = cv.imread('./assets/img/map.png', 0)
    w_bar, h_bar = template.shape[::-1]
    w_offset, h_offset = template_offset.shape[::-1]
    w_map, h_map = template_map.shape[::-1]
    corner_bar = (-1, -1)

    coords = cv.matchTemplate(grayscale_img, template, cv.TM_CCOEFF_NORMED)
    thresh = 0.7

    locs = np.where(coords >= thresh)
    for pt in zip(*locs[::-1]):
        corner_bar = (pt[0] + int(w_bar), pt[1] + int(h_bar+h_offset))
    if corner_bar[0] > -1:
        return (corner_bar[0] - int(w_map/2), corner_bar[1] + int(h_map/2))
    return corner_bar

def calc_dir(map_center):
    print("map center: ", map_center)
    portal = findImage('./assets/img/portal.png')
    print("portal at: ", portal)
    # find angle of center TO portal
    angle = np.arctan2(portal[1] - map_center[1],
                       portal[0] - map_center[0])
    # retrieve direction vector to walk along
    direction = (np.cos(angle), np.sin(angle))
    return direction, portal

def find_portal():
    l = 300
    portal = (-1, -1)
    enter_prompt = findImage('./assets/img/move_portal.png')
    map_center = calc_map_center('./assets/img/map_frame.png')
    while(enter_prompt == (-1, -1)):
        dir, portal = calc_dir(map_center)
        if portal == (-1, -1):
            break
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.move(l * dir[0], l * dir[1])        
        gui.click(button='right')
        enter_prompt = findImage('./assets/img/move_portal.png')
    gui.keyDown('g')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('g') 
    
def executeScript():
    while True:
        # click into window
        time.sleep(random.uniform(1, 2))

        repair('./assets/img/armor.png')

        # enter dungeon
        gui.keyDown('g')
        time.sleep(random.uniform(0.05,0.1))
        gui.keyUp('g')
        time.sleep(random.uniform(0.30, 0.45))
        clickConfirm('./assets/img/enter.png')
        time.sleep(random.uniform(LOAD_IN_TIME, LOAD_IN_TIME + 0.5))

        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.click()
        time.sleep(random.uniform(3.7, 3.9))

        rotation()
        # with Manager() as manager:
        #     event = manager.Event()
        #     event.set()
        #     time.sleep(0.1)
        #     p1 = Process(target = kite, args=(event, ))
        #     p1.start()
        #     p2 = Process(target = rotation, args=(event, ))
        #     p2.start()
        #     p1.join()
        #     p2.join()
            
        # find_portal()
        # time.sleep(random.uniform(3.5, 4.0))

        # exit dungeon
        clickConfirm('./assets/img/leave.png')
        time.sleep(random.uniform(LOAD_OUT_TIME, LOAD_OUT_TIME + 0.5))
    
def exitScript(p):
    p.terminate()
    raise SystemExit()
    
if __name__ == '__main__':
    p = Process(target=executeScript)
    p.start()
    keyboard.add_hotkey('0', exitScript, args=(p,))
    