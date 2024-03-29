from utils import *

res_ratio = (game_res[0] / DEFAULT_GAME_RES[0], 
             game_res[1] / DEFAULT_GAME_RES[1])

def clickConfirm(ref_img, thresh=0.7):
    ''' Clicks a button and confirms. 
        
            ### Parameters:
                `ref_img` (string): filename of target image
    '''
    x, y = findImage(ref_img, thresh)
    if (x, y) == (-1, -1):
        raise NameError('template not found...')
    gui.moveTo(x, y)
    gui.move(random.randint(1, 5), 0)
    gui.click()
    time.sleep(random.uniform(0.15, 0.30))
    gui.keyDown('enter')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('enter')

# The skill rotation is based on a specific set of keybinds for the Artillerist class.
def rotation(iters=3):
    ''' Executes a full skill rotation for `iters` number of times.
                   
                ### Parameters:
                    `iters` (int): number of times to do skill rotation, default of 3
    '''
    align()
    # while (findImage('./assets/img/portal.png') == (-1, -1)):
    for i in range(iters):
        # One-shot burst
        # Resolution-dependent
        gui.moveTo(resolution[0]/2 - 200 * res_ratio[0],
                   resolution[1]/2 - 150 * res_ratio[0])
        gui.keyDown('w')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('w')
        # Cast time
        time.sleep(random.uniform(0.6, 0.8))
        kite()
        
        # One-shot burst
        # Resolution-dependent
        gui.moveTo(resolution[0]/2 - 200 * res_ratio[0],
                   resolution[1]/2 - 150 * res_ratio[0])
        gui.keyDown('s')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('s')
        gui.keyDown('s')
        time.sleep(random.uniform(0.075, 0.125))
        gui.keyUp('s')
        # Cast time
        time.sleep(random.uniform(1.75, 2.0))
        kite()
        
        # Defensive
        gui.keyDown('d')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('d')
        # Cast time
        time.sleep(random.uniform(0.25, 0.5))
        
        # Other (turret)
        gui.keyDown('f')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('f')
        # Cast time
        time.sleep(random.uniform(0.75, 1.0))
        
        # Mini burst
        # Resolution-dependent
        gui.moveTo(resolution[0]/2 - 200 * res_ratio[0],
                   resolution[1]/2 - 100 * res_ratio[0])
        gui.keyDown('a')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('a')
        # Cast time
        time.sleep(random.uniform(0.6, 0.8))
        
        # DoT
        gui.keyDown('r')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('r')
        # Cast time
        time.sleep(random.uniform(1.25, 1.5))
        # kite()
        # Wait for cds
        # time.sleep(random.uniform(4.5, 5.0))
    # One-shot burst
    # Resolution-dependent
    gui.moveTo(resolution[0]/2 - 200 * res_ratio[0],
               resolution[1]/2 - 150 * res_ratio[0])
    gui.keyDown('w')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('w')
    
    # Cast time
    time.sleep(random.uniform(2.0, 2.5))

def kite():
    ''' Primitive kiting by moving in a rectangle. Probably drifts in some direction over time. '''
    # Resolution-dependent
    # X cursor offset
    l = 900 * res_ratio[0]
    # Y cursor offset
    l2 = 350 * res_ratio[0]
    x, y = (resolution[0]/2, resolution[1]/2)
    # Up
    x1, y1 = (x, y-l2)
    # Left
    x2, y2 = (x-l, y)
    # Down
    x3, y3 = (x, y+l2)
    # Right
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
    ''' Move towards the bottom left of the map (for initial alignment). '''
    # Resolution-dependent
    # X cursor offset
    l = 600 * res_ratio[0]
    # Y cursor offset
    l2 = 350 * res_ratio[0]
    x, y = (resolution[0]/2, resolution[1]/2)
    # Down
    x3, y3 = (x, y+l2)
    # Right
    x4, y4 = (x+l, y)
    gui.moveTo(x3, y3)
    gui.click(button='right')
    time.sleep(0.75)
    gui.moveTo(x4, y4)
    gui.click(button='right')
    time.sleep(0.5)

def repair(ref_img):
    ''' Repairs armor.
               
                ### Parameters:
                    `ref_img` (string): filename of target image
    '''
    x, _ = findImage(ref_img)
    if x > -1:
        gui.keyDown('alt')
        gui.keyDown('p')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('p')
        gui.keyUp('alt')
        time.sleep(random.uniform(1.5, 2.0))
        clickConfirm('pet', thresh=0.75)
        time.sleep(random.uniform(0.5, 1.0))
        clickConfirm('repair')
        gui.keyDown('esc')
        time.sleep(random.uniform(0.05, 0.1))
        gui.keyUp('esc')
    print('armor\'s all good!')