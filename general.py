from lib import *

def clickConfirm(ref_img):
    x, y = findImage(ref_img)
    gui.moveTo(x, y)
    gui.move(random.randint(1, 5), 0)
    gui.click()
    time.sleep(random.uniform(0.15, 0.30))
    gui.keyDown('enter')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('enter')

def rotation(iters=3):
    align()
    # while (findImage('./assets/img/portal.png') == (-1, -1)):
    for i in range(iters):
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