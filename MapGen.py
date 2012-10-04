### Random map generator/handler
import random, pygame, math, sys
from pygame.locals import *
import pygcurse
import FovAlgo as fov
import AITracker as ait
from AITracker import *
import GuiHandler as gui


MAX_H_W = 10
MIN_H_W = 6
MAX_ROOMS = 30
MAX_ENEMY = 4

level = 0
all_enemies = []
down_stairs = []
up_stairs = []
rooms = []
buildings = []
empty_tiles = []
floor_tiles = []
current_rooms = 0
current_buildings = 0
area = 'city'


class Object: #A visible character on the window
    def __init__(self, x, y, char, name, color, blocks=False, cognitive=False):
        global floor_tiles
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.cognitive = cognitive
        if self.cognitive:
            self.cognitive.owner = self



    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def check(self, dx, dy):
        target = None
        tmpx = self.x + dx
        tmpy = self.y + dy
        for Object in all_enemies:
            if Object.x == tmpx and Object.y == tmpy and Object.cognitive.status == 'alive':
                target = Object
                break
        if target is not None:
            self.cognitive.mel_attack(target)
        if tmpx == 0 or tmpx == gui.MAPWIDTH - 1 or tmpy == 0 or tmpy == gui.MAPHEIGHT - 1:
            if tmpx == 0:
                self.x = gui.MAPWIDTH - 2
            elif tmpx == gui.MAPWIDTH - 1:
                self.x = 1
            elif tmpy == 0:
                self.y = gui.MAPHEIGHT - 2
            elif tmpy == gui.MAPHEIGHT - 1:
                self.y = 1
            mp = make_city()
            gui.win.setscreencolors(None, None, True)
            return
        else:
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        global objects
        if self in objects:
            objects.remove(self)
            objects.insert(0, self)

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked=blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        self.explored = False

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


    
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 - 1) <= other.x2 and (self.x2 + 1) >= other.x1 and (self.y1 - 1) <= other.y2 and (self.y2 + 1) >= other.y1


def is_blocked(x,y):
    if mp[x][y].blocked:
        return True
    for Object in objects:
        if Object.blocks and Object.x == x and Object.y == y:
            return True
    return False 

def ai_go():
    global fov_mp
    global objects
    global player
    ait.fov_mp = fov_mp
    ait.objects = objects
    ait.player = player
    for Object in all_enemies:
        if Object.cognitive.ai != None and Object.cognitive.status == 'alive':
            Object.cognitive.ai.take_turn()

def hor_hall(x1, x2, y):
    global mp
    for x in range(min(x1, x2), max(x1, x2) + 1):
        mp[x][y].blocked = False
        mp[x][y].block_sight = False

def ver_hall(y1, y2, x):
    global mp
    for y in range(min(y1, y2), max(y1, y2) + 1):
        mp[x][y].blocked = False
        mp[x][y].block_sight = False        

def make_room(room):
    global mp, floor_tiles   
    for x in range(room.x1, room.x2 + 1):
        for y in range(room.y1, room.y2 + 1):
            mp[x][y].blocked = False
            mp[x][y].block_sight = False
            floor_tiles.append(((x),(y))) 

def make_building(building):
    global mp, floor_tiles
    walltiles = []
    
    for x in range(building.x1 + 1, building.x2):
        for y in range(building.y1 + 1, building.y2):
            floor_tiles.append(((x),(y)))
    for x in range(building.x1, building.x2 + 1):
        for y in range(building.y1, building.y2 + 1):
            if x == building.x1 or x == building.x2:
                    if y >= building.y1 and y <= building.y2:
                        mp[x][y].blocked = True
                        mp[x][y].block_sight = True
                        walltiles.append((x,y)) 
    for y in range(building.y1, building.y2 + 1):                          
        for x in range(building.x1, building.x2 + 1):
            if y == building.y1 or y == building.y2:
                    if x >= building.x1 and x <= building.x2:
                        mp[x][y].blocked = True
                        mp[x][y].block_sight = True
                        walltiles.append((x,y))
    door = (walltiles[(random.randint(1, len(walltiles)) - 1)]) #return door as object type mp tile
    mp[door[0]][door[1]].blocked = False   
    mp[door[0]][door[1]].block_sight = False   
            

def make_map():
    global mp, current_rooms, rooms, level, mapDownStairs, mapUpStairs
    up_stairs = []
    down_stairs = []
    if level < 5:
        mapDownStairs = True
    else:
        mapDownStairs = False
    mapUpStairs = True
    mp = [[Tile(True)
    for y in range(gui.MAPHEIGHT)]
    for x in range(gui.MAPWIDTH)]
    for r in range(MAX_ROOMS):
        w = random.randint(MIN_H_W, MAX_H_W)
        h = random.randint(MIN_H_W, MAX_H_W)
        x = random.randint(1, gui.MAPWIDTH - w - 2)
        y = random.randint(1, gui.MAPHEIGHT - h - 2)

        new_room = Rectangle(x, y, w, h)
        failedrooms = 0
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                failedrooms += 1
                break

        if not failed:
            make_room(new_room)
            place_objects(new_room)

            (new_x, new_y) = new_room.center()

            if current_rooms != 0:
                (prev_x, prev_y) = rooms[current_rooms-1].center()
                if random.randint(0, 1) == 1:
                    hor_hall(prev_x, new_x, prev_y)
                    ver_hall(prev_y, new_y, new_x)
                else:
                    ver_hall(prev_y, new_y, prev_x)
                    hor_hall(prev_x, new_x, new_y)

            rooms.append(new_room)
            current_rooms += 1
    place_stairs()
    return mp

def make_city():
    global mp, current_buildings, buildings, mapDownStairs, mapUpStairs,floor_tiles, all_enemies, up_stairs, down_stairs, objects
    objects = []
    all_enemies = []
    up_stairs = []
    down_stairs = []
    current_buildings = 0
    buildings = []
    floor_tiles = []
    mapUpStairs = False
    mapDownStairs = True
    mp = [[Tile(False)
    for y in range (gui.MAPHEIGHT)]
    for x in range (gui.MAPWIDTH)]
    for r in range (MAX_ROOMS):
        w = random.randint(MIN_H_W, MAX_H_W)
        h = random.randint(MIN_H_W, MAX_H_W)
        x = random.randint(2, gui.MAPWIDTH - w - 3)
        y = random.randint(2, gui.MAPHEIGHT - h - 3)

    
        new_building = Rectangle(x, y, w, h)

        failedbuildings = 0
        failed = False
        for other_building in buildings:
            if new_building.intersect(other_building):
                failed = True
                failedbuildings += 1
                break
        if not failed:
            make_building(new_building)
            buildings.append(new_building)
            place_objects(new_building)
            current_buildings += 1
    place_stairs()
    return mp

def place_objects(room):
    global all_enemies
    enemies = random.randint(0, MAX_ENEMY)
    items_placed = 0 #reset each time the function is called(each room)
    for n in range(enemies):
        acceptable_tile = False
        while acceptable_tile != True:
            x = random.randint(room.x1, room.x2)
            y = random.randint(room.y1, room.y2)
            if mp[x][y].blocked != True:
                acceptable_tile = True
        enemy_list = {'zombie':5, 'brute':2, 'zombling':4}
        enemy = roll(enemy_list)
        if enemy == 'zombie':
            z_cog = ait.Cognitive(2, 2, 1, 2, 1, ai=ait.Enemy())
            new_enemy = Object(x, y, 'Z', 'zombie', pygame.Color(15,170,15), blocks=True, cognitive=z_cog)
            objects.append(new_enemy)
            all_enemies.append(new_enemy)
        elif enemy == 'brute':
            b_cog = ait.Cognitive(4, 1, 2, 3, 1, ai=ait.Enemy())
            new_enemy = Object(x, y, 'b', 'brute', pygame.Color(70,15,15), blocks=True, cognitive=b_cog)
            objects.append(new_enemy)
            all_enemies.append(new_enemy)
        elif enemy == 'zombling':
            zg_cog = ait.Cognitive(1, 4, 1, 1, 1, ai=ait.Enemy())
            new_enemy = Object(x, y, 'g', 'zombling', pygame.Color(150,15,15), blocks=True, cognitive=zg_cog)
            objects.append(new_enemy)
            all_enemies.append(new_enemy)

def place_stairs():
    global mp, floor_tiles, mapDownStairs, mapUpStairs, up_stairs, down_stairs
    totstairs = random.randint(1, int(((gui.MAPHEIGHT * gui.MAPWIDTH) // 1200)))
    if mapDownStairs == True:
        for n in range(totstairs):
            ftile = floor_tiles[random.randint(0, len(floor_tiles) - 1)]
            stairs = Object(ftile[0], ftile[1], '>', 'stairs down', pygame.Color(120, 50, 10))
            down_stairs.append(stairs)
            objects.append(stairs)
    if mapUpStairs == True:
        for n in range(totstairs):
            ftile = floor_tiles[random.randint(0, len(floor_tiles) - 1)]
            stairs = Object(ftile[0], ftile[1], '<', 'stairs up', pygame.Color(120, 50, 10))
            up_stairs.append(stairs)
            objects.append(stairs)

def roll(opts): #### roll() requires a dict with a key identifier, and the value assoc. as the number of chances the key recieves
    cur_key = 0
    total_chances = sum(opts.values())
    choice = random.randint(1, total_chances)
    for value in opts.values():
        if choice <= value:
            return (opts.keys())[cur_key]
        elif choice > value:
            choice -= value
            cur_key += 1
        else:
            print('Error in funct \'roll\'. Shutting down.')
            quit()

def rand_player_pos():
    global empty_tiles

    mx = len(empty_tiles)
    start_pos = empty_tiles[random.randint(0,mx)]
    player.x = start_pos[0]  
    player.y = start_pos[1]  

def render_all():
    global mp, dirtytiles, fov_mp, MSGX, HBAR_WID
    fov_mp = fov.compute(mp, player.x, player.y, gui.MAPHEIGHT, gui.MAPWIDTH)
    ait.fov_mp = fov_mp
    for y in range(gui.MAPHEIGHT):
        for x in range(gui.MAPWIDTH):
            if fov_mp[x][y] == 1:
                mp[x][y].explored = True
                wall = mp[x][y].block_sight
                if wall:
                    gui.win.putchars('#', x, y, fgcolor=(90,40,0,255)) #BROWN
                else: 
                    gui.win.putchars('.', x, y, fgcolor=(255,255,255,255)) #WHITE
            elif mp[x][y].explored:   
                wall = mp[x][y].block_sight
                if wall:
                   gui.win.putchars('#', x, y, fgcolor=(70,70,70,255))
                else: 
                    gui.win.putchars('.', x, y, fgcolor=(70,70,70,255))
    for Object in objects:
        if fov_mp[Object.x][Object.y] == 1:
            gui.win.putchars(Object.char, x=Object.x, y=Object.y, fgcolor=Object.
                color)
    
    if player.cognitive.hp > (7 * player.cognitive.con):
        healthcolor = (0,255,0,255)
    elif player.cognitive.hp > (4 * player.cognitive.con):
        healthcolor = (255,255,0,255)
    else:
        healthcolor = (255,0,0,255)
    healthbar = pygcurse.PygcurseTextbox(gui.win, region = (0, gui.MAPHEIGHT, gui.HBARWID, 1), bgcolor=None, fgcolor=healthcolor, border=None, text="Health: " + str(player.cognitive.hp), wrap=False)
    healthbar.update()
    gui.win.putchars('Level ' + str(level) + ' of the ' + area, 0, gui.MAPHEIGHT + 1, fgcolor = pygame.Color(125, 170, 125))
    gui.win.putchars(player.char, player.x, player.y, player.color)
    gui.msg_update()
    gui.win.update()
    gui.win.blittowindow()
    gui.win.putchars('     ', 8, gui.MAPHEIGHT, fgcolor = (0,0,0,255))
    gui.win.setscreencolors(pygame.Color(215,215,215), None, False)
    gui.win.fill(region=(gui.MSGX, gui.MAPHEIGHT, gui.MSG_MAX_WID, gui.MSG_HEIGHT))

def create_mp():
    global mp, current_rooms, rooms, empty_tiles, all_enemies, objects, floor_tiles, empty_tiles, area, current_buildings
    objects = [player]
    current_rooms = 0
    current_buildings = 0
    rooms = []
    floor_tiles = []
    empty_tiles = []
    all_enemies = []
    mp = []
    gui.win.setscreencolors(None, None, True)
    if area == 'dungeon':
        mp = make_map()
    elif area == 'city':
        mp = make_city()
    for x in range(gui.MAPWIDTH):
        for y in range(gui.MAPHEIGHT):
            if not is_blocked(x, y):
                empty_tiles.append((x, y))
    rand_player_pos()
    render_all()
    return mp

def init():
    global mp, player, objects, player_cognitive

    player = Object(0, 0, '@', 'player', pygame.Color(255,255,255), cognitive = player_cognitive)
    objects = [player]
    mp = create_mp()
    return mp

####  TEMP VARS #####

con = 50
agi = 50
pwr = 50
stg = 50
itl = 50
player_cognitive = Cognitive(con, agi, pwr, stg, itl)

#### /TEMP VARS #####
