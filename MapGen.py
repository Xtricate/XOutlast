### Random map generator/handler
import random, pygame, math, sys
from pygame.locals import *
import pygcurse
import FovAlgo as fov
import AITracker as ait
from AITracker import *

MAPWIDTH=80
MAPHEIGHT=45

MAX_H_W = 10
MIN_H_W = 6
MAX_ROOMS = 30
MAX_ENEMY = 4

all_enemies = []

rooms = []
empty_tiles = []
current_rooms = 0

win = pygcurse.PygcurseWindow(80, 50, 'Xtricate Presents: Outlast')
win.autoupdate = False

class Object: #A visible character on the window
    def __init__(self, x, y, char, name, color, blocks=False, cognitive=False):
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
        for Object in objects:
            if Object.x == tmpx and Object.y == tmpy:
                target = Object
                break
        if target is not None:
            self.cognitive.mel_attack(target)
        else:
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        global objects
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
    for Object in objects:
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
    global mp, empty_tiles
    for x in range(room.x1, room.x2 + 1):
        for y in range(room.y1, room.y2 + 1):
            mp[x][y].blocked = False
            mp[x][y].block_sight = False
            empty_tiles.append((x, y))

def make_map():
    global mp, current_rooms, rooms
    mp = [[Tile(True)
    for y in range(MAPHEIGHT)]
    for x in range(MAPWIDTH)]
    for r in range(MAX_ROOMS):
        w = random.randint(MIN_H_W, MAX_H_W)
        h = random.randint(MIN_H_W, MAX_H_W)
        x = random.randint(1, MAPWIDTH - w - 2)
        y = random.randint(1, MAPHEIGHT - h - 2)

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
        enemy_list = {'zombie':5, 'brute':2}
        enemy = roll(enemy_list)
        if enemy == 'zombie':
            z_cog = ait.Cognitive(2, 2, 1, 3, 1, ai=ait.Enemy())
            new_enemy = Object(x, y, 'z', 'zombie', pygame.Color(15,170,15), blocks=True, cognitive=z_cog)
            objects.append(new_enemy)
            all_enemies.append(new_enemy)
        elif enemy == 'brute':
            b_cog = ait.Cognitive(4, 1, 3, 3, 1, ai=ait.Enemy())
            new_enemy = Object(x, y, 'b', 'brute', pygame.Color(70,15,15), blocks=True, cognitive=b_cog)
            objects.append(new_enemy)
            all_enemies.append(new_enemy)

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
     mx = len(empty_tiles)
     start_pos = empty_tiles[random.randint(0,mx)]
     player.x = start_pos[0]  
     player.y = start_pos[1]  

def render_all():
    global mp, dirtytiles, fov_mp
    fov_mp = fov.compute(mp, player.x, player.y, MAPHEIGHT, MAPWIDTH)
    ait.fov_mp = fov_mp
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            if fov_mp[x][y] == 1:
                mp[x][y].explored = True
                wall = mp[x][y].block_sight
                if wall:
                    win.putchars('#', x, y, fgcolor=(90,40,0,255)) #BROWN
                else: 
                    win.putchars('.', x, y, fgcolor=(255,255,255,255)) #WHITE
            elif mp[x][y].explored:   
                wall = mp[x][y].block_sight
                if wall:
                    win.putchars('#', x, y, fgcolor=(70,70,70,255))
                else: 
                    win.putchars('.', x, y, fgcolor=(70,70,70,255))
    for Object in objects:
        if fov_mp[Object.x][Object.y] == 1:
            win.putchars(Object.char, x=Object.x, y=Object.y, fgcolor=Object.
                color)

    win.putchars('Health:', 0, MAPHEIGHT + 1, fgcolor=(255,0,0,255))
    if player.cognitive.hp > (7 * player.cognitive.con):
        healthcolor = (0,255,0,255)
    elif player.cognitive.hp > (4 * player.cognitive.con):
        healthcolor = (255,255,0,255)
    else:
        healthcolor = (255,0,0,255)
    win.putchars(str(player.cognitive.hp), 8, MAPHEIGHT + 1, fgcolor = healthcolor)


    win.putchars(player.char, player.x, player.y, player.color)

    win.update()
    win.putchars('    ', 8, MAPHEIGHT + 1, fgcolor = (0,0,0,255))
    win.setscreencolors(pygame.Color(215,215,215), None, False)

def init():
    global mp, player, objects, player_cognitive
    player = Object(0, 0, '@', 'player', pygame.Color(255,255,255), cognitive = player_cognitive)
    objects = [player]
    mp = make_map()
    rand_player_pos()
    return mp

####  TEMP VARS #####

con = 5
agi = 5
pwr = 4
stg = 4
itl = 5
player_cognitive = Cognitive(con, agi, pwr, stg, itl)

#### /TEMP VARS #####
