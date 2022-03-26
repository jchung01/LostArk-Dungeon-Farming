from lib import *
from general import *

MAP_OFFSET_X = 1595
MAP_OFFSET_Y = 40
map_center = (-1, -1)
start = 0
res_ratio = (game_res[0] / DEFAULT_GAME_RES[0], 
             game_res[1] / DEFAULT_GAME_RES[1])

# Lost Ark's rescaling formula:
# Basically what the 16:9 equivalent resolution would be,
# with added black bars on top/bottom
# Implication: no y scaling compared to 16:9 equivalent!
#
# (x1, y1) is 1920x1080
# (x2, y2) is current resolution
# x: res_ratio(x2, x1) * x
# y: res_ratio(x2, x1) * y + (y2 - 9*x2/16)/2
# gui.moveTo((res_ratio[0] * (MAP_OFFSET_X+297/2)), 
#          res_ratio[0]*(MAP_OFFSET_Y+255/2)+(game_res[1] - 9*game_res[0]/16)/2)
def scaleMap(base_x=MAP_OFFSET_X, base_y=MAP_OFFSET_Y):
    x = res_ratio[0] * base_x
    y = res_ratio[0] * base_y + \
        (game_res[1] - 9/16 * game_res[0])/2
    return (x, y, 296, 255)
    

map_center = scaleMap(base_x=MAP_OFFSET_X+297*(1.0+(1.0-hud_scale))/2,
                      base_y=MAP_OFFSET_Y+255*hud_scale/2)[:2]
# gui.moveTo(map_center)

def calc_dir1(target_img):
    ''' Calculates the direction vector from the center of the map to a target.
               
                ### Parameters:
                    `target_img` (string): filename of target image
                    
                ### Returns:
                    `direction` (tuple): (x, y) direction vector
                    `target` (tuple): (x, y) position of target
    '''
    # map_center = calc_map_center('./assets/img/map_frame.png')
    print("map center: ", map_center)
    target = findImage(target_img)
    print("target at: ", target)
    # find angle of center TO target
    angle = np.arctan2(target[1] - map_center[1],
                       target[0] - map_center[0])
    # retrieve direction vector to walk along
    direction = (np.cos(angle), np.sin(angle))
    return direction, target

def calc_dir2(position):
    ''' Calculates the direction vector from the center of the map to a target (pixel version).
               
                ### Parameters:
                    `position` (tuple): (x, y) position of target pixel
                    
                ### Returns:
                    `direction` (tuple): (x, y) direction vector
    '''
    # map_center = calc_map_center('./assets/img/map_frame.png')
    print("map center: ", map_center)
    print("target at: ", position)
    # find angle of center TO target
    angle = np.arctan2(position[1] - map_center[1],
                       position[0] - map_center[0])
    # retrieve direction vector to walk along
    direction = (np.cos(angle), np.sin(angle))
    return direction

def closest_cmp(position):
    ''' Comparator for pixel position from map center.
               
                ### Parameters:
                    `position` (tuple): (x, y) position of pixel
                    
                ### Returns:
                    `dist` (float): distance between map center and position
    '''
    dist = np.linalg.norm(np.array(map_center) - np.array(position))
    return dist

# -- functions to find specific targets -- #
def find_portal():
    ''' Finds portal on map, then moves to and enters it. '''
    # tune parameter to adjust consistency of getting to portal
    l = 300 * res_ratio[0]
    
    portal = (-1, -1)
    enter_prompt = findImage('move_portal')
    # move until portal found
    while(enter_prompt == (-1, -1)):
        dir, portal = calc_dir1('portal')
        # lost/didn't find the portal location
        if portal == (-1, -1):      
            gui.click(button='right')
            time.sleep(random.uniform(1,2))
            break
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.move(l * dir[0], l * dir[1])        
        gui.click(button='right')
        enter_prompt = findImage('move_portal')
    gui.keyDown('g')
    time.sleep(random.uniform(0.05, 0.1))
    gui.keyUp('g') 

def find_elites():
    ''' Finds the furthest elite, moves towards it, and does skill rotation. 
    
                Fails on conditions:
                - if dead
                - if 3 minutes have passed in Room 2
                - if no more elites exist on the map
    '''
    # distance traveled
    l = 350 * res_ratio[0]
    # elite attack detection radius
    r = 30 * res_ratio[0]
    
    start = time.time()
    while True:
        dead = findImage('dead')
        if dead != (-1, -1):
            break
        if time.time() - start > ROOM2_TIME_LIMIT:
            break
        elites = find_elite_color()
        # sort list of elite positions, closest to center first
        elites = sorted(elites, key=lambda pos: closest_cmp(pos))
        try:
            dir = calc_dir2(elites[-1])
        except:
            print('can\'t find any more elites...')
            break
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.move(l * dir[0], l * dir[1]) 
        gui.mouseDown(button='right')
        time.sleep(random.uniform(3,4))
        gui.mouseUp(button='right')
        if np.any(np.array([np.linalg.norm(np.array(map_center) - np.array(position)) <= r for position in elites])):
            rotation(iters=1) 
        
def find_elite_color():    
    ''' Gets a list of all potential elite "positions". (by pixel color) 
                    
                ### Returns:
                    `coord_list` (list[tuple]): list of coordinates of elite pixel color
    '''
    # HSV2RGB Elite color range
    low = (100,165,100)
    high = (110,255,255)
    #low = (100,150,0)
    #high = (110,255,255)
    # img = cv.imread('./out_raw.png')
    # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = np.array(gui.screenshot(region=scaleMap()))
    img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(img_HSV, low, high)
    img_masked = cv.bitwise_and(img, img, mask=mask)
    # cv.imwrite('out_raw.png', cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # cv.imwrite('out2.png', cv.cvtColor(img_masked, cv.COLOR_BGR2RGB))
    indices = np.any(img_masked != [0, 0, 0], axis=-1)
    coord_list = np.flip(np.argwhere(indices), axis=1)
    coord_list = list(map(tuple, coord_list))
    x_offset, y_offset = scaleMap()[:2]
    coord_list = map(lambda coords: (coords[0] + x_offset, coords[1] + y_offset), coord_list)
    return coord_list

def find_boss():
    ''' Finds the boss, moves towards it, and does skill rotation. 
    
                Fails on conditions:
                - if dead
                - if 3 minutes have passed in Room 2
                - if boss no longer exists on the map
    '''
    # tune parameter to adjust consistency of getting to portal
    l = 300 * res_ratio[0]
    
    boss = findImage('boss')
    print('boss: ', boss)
    portal = findImage('portal')
    while(boss != (-1, -1)):
        dead = findImage('dead')
        if dead != (-1, -1):
            break
        if time.time() - start > ROOM2_TIME_LIMIT:
            break
        dir, boss = calc_dir1('boss')
        gui.moveTo(resolution[0]/2, resolution[1]/2)
        gui.move(l * dir[0], l * dir[1])        
        gui.mouseDown(button='right')
        time.sleep(random.uniform(2,3))
        gui.mouseUp(button='right')
    print('boss not found')
    while(portal == (-1, -1)):
        dead = findImage('dead')
        if dead != (-1, -1):
            break
        if time.time() - start > ROOM2_TIME_LIMIT:
            break
        rotation(iters=1)
        boss = findImage('boss')
        if (boss != (-1, -1)):
            find_boss()
        portal = findImage('portal')
#r = 20
#img_test = cv.imread('./assets/img/test2.png')
#cv.circle(img_test, calc_map_center('./assets/img/map_frame_test.png'), r, (0, 0, 255), cv.LINE_4)
#cv.imwrite('out.png', img_test)