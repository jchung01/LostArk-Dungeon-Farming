from lib import *
from map_finder import *
from general import *


# for starting/stopping script
import keyboard
from multiprocessing import Process

# Tested on resolutions:
# [1920x1200, 1920x1080, 1600x1200, 1600x900]
# Only works on fullscreen (for now)

LOAD_IN_TIME = 9
LOAD_OUT_TIME = 10
DEFENSIVE = ['d']
AOE = ['w', 's']
OTHER = ['a', 'f', 'r']
    
def executeScript():
    print(res_ratio)
    scale_images()
    mainScript()
    
# the main script
def mainScript():
    while True:
        repair('armor')
        
        # enter dungeon
        gui.keyDown('g')
        time.sleep(random.uniform(0.05,0.1))
        gui.keyUp('g')
        time.sleep(random.uniform(0.5, 0.75))
        try:
            clickConfirm('enter')
        except:
            mainScript()
        time.sleep(random.uniform(LOAD_IN_TIME, LOAD_IN_TIME + 0.5))

        # room 1
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.click()
        time.sleep(random.uniform(3.7, 3.9))
        rotation()
            
        # find next room
        find_portal()
        time.sleep(random.uniform(3.5, 4.0))
        
        # room 2
        # -- TO-DO -- #
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.click()
        time.sleep(random.uniform(3.9, 4.1))
        find_elites()
        find_boss()
        find_portal()

        time.sleep(random.uniform(3.5, 4.0))
        # exit dungeon
        clickConfirm('leave')
        time.sleep(random.uniform(LOAD_OUT_TIME, LOAD_OUT_TIME + 0.5))
    
# control script using key '0'
def controlScript(p):
    if p.is_alive():
        p.terminate()
        raise SystemExit()
    else:
        p.start()
    
if __name__ == '__main__':
    pressed = 0
    p = Process(target=executeScript)
    keyboard.wait('0')
    controlScript(p)
    keyboard.wait('0')
    controlScript(p)