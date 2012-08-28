### Random map generator
import random

MAPWIDTH=80
MAPHEIGHT=45

MAX_H_W = 10
MIN_H_W = 6
MAX_ROOMS = 30
MAX_ENEMY = 10

all_enemies = []

rooms = []
empty_tiles = []
current_rooms = 0

class Object: #A visible character on the window
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked=blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

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
        x = random.randint(room.x1, room.x2)
        y = random.randint(room.y1, room.y2)
        enemy_list = {'zombie':5, 'brute':4}
        enemy = roll(enemy_list)
        if enemy == 'zombie':
            new_enemy = Object(x, y, 'z', pygame.color(15,170,15))
            all_enemies.append(new_enemy)
        elif enemy == 'brute':
            new_enemy = Object(x, y, 'b', pygame.color(70,15,15))
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

