### Outlast in pygcurse
import pygame, math, sys
from pygame.locals import *
import pygcurse

MAPWIDTH=20
MAPHEIGHT=20

playerx = MAPWIDTH // 2
playery = MAPHEIGHT // 2

PlayerTurn = True

win = pygcurse.PygcurseWindow(80, 50, 'Xtricate Presents: Outlast')
win.autoupdate = False

class Object: #A visible character on the window
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
 
    def move(self, dx, dy):
        if not mp[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked=blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

def make_map():
    global mp

    mp = [[Tile(False)
    for y in range(MAPHEIGHT)]
    for x in range(MAPWIDTH)]
#def make_room(topleftx, toplefty, bottomleftx, bottomlefty):



def handle_keys():
    global playerx, playery

    turnkeys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and event.key in turnkeys:
            if event.key == pygame.K_UP: player.move(0, -1) 
            if event.key == pygame.K_DOWN: player.move(0, 1)
            if event.key == pygame.K_LEFT: player.move(-1, 0)
            if event.key == pygame.K_RIGHT: player.move(1, 0)

            render_all()
        elif event.type == QUIT:
            quit()


def render_all():
    global mp
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            wall = mp[x][y].block_sight
            if wall:
                win.putchars('#', x, y, fgcolor=(255,0,0,255)) #RED
            else: 
                win.putchars('.', x, y, fgcolor=(255,255,255,255)) #WHITE
    
    for Object in objects:
        win.putchars(Object.char, x=Object.x, y=Object.y, fgcolor=Object.color)
        win.update()
        win.setscreencolors(None, None, clear=True)


def mainloop():
    make_map()
    render_all()
    while 1:
        handle_keys()

player = Object(playerx, playery, '@', pygame.Color(255,255,255))
objects = [player]

mainloop()
