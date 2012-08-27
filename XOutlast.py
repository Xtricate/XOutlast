### Outlast in pygcurse
import pygame, math, sys, random
from pygame.locals import *
import pygcurse
import MapGen as gen
import FovAlgo as fov

MAPWIDTH=gen.MAPWIDTH
MAPHEIGHT=gen.MAPHEIGHT

PlayerTurn = True

win = pygcurse.PygcurseWindow(80, 50, 'Xtricate Presents: Outlast')
win.autoupdate = False

dirtytiles = []

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

def rand_player_pos():
     mx = len(gen.empty_tiles)
     start_pos = gen.empty_tiles[random.randint(0,mx)]
     player.x = start_pos[0]  
     player.y = start_pos[1]  

def init_render():
    global mp

    win.update()

def render_all():
    global mp, dirtytiles
    fov_mp = fov.compute(mp, player.x, player.y, MAPHEIGHT, MAPWIDTH)
    print len(fov_mp)
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            if fov_mp[x][y] == 1:
                wall = mp[x][y].block_sight
                if wall:
                    win.putchars('#', x, y, fgcolor=(90,40,0,255)) #BROWN
                else: 
                    win.putchars('.', x, y, fgcolor=(255,255,255,255)) #WHITE
    for Object in objects:
        win.putchars(Object.char, x=Object.x, y=Object.y, fgcolor=Object.color)
    win.update()
    win.setscreencolors(None, None, False)
    win.putchars('.', player.x, player.y, fgcolor=(255,255,255,255))


def start_game():
    global mp
    mp = gen.make_map()
    rand_player_pos()
 #   init_render()
    mainloop()

def mainloop():
    render_all()
    while 1:
        handle_keys()

player = Object(0, 0, '@', pygame.Color(255,255,255))
objects = [player]

start_game()
