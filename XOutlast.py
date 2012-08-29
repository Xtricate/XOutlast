### Outlast in pygcurse
import pygame, math, sys, random
from pygame.locals import *
import pygcurse
import MapGen as gen
import AITracker as ait

MAPWIDTH=gen.MAPWIDTH
MAPHEIGHT=gen.MAPHEIGHT

debug_mode = False


dirtytiles = []

class Game:
    def __init__(self, flags=None):
        global mp
        mp = gen.init()
        gen.render_all()
        mainloop()
            

def handle_keys():
    global playerx, playery, game_state

    turnkeys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            quit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSLASH:
            if gen.win.fullscreen == True:
                gen.win.fullscreen = False
            else:
                gen.win.fullscreen = True
            gen.render_all()
        if ait.game_state == 'normal':        
            if event.type == pygame.KEYUP and event.key in turnkeys:
                if event.key == pygame.K_UP: gen.player.check(0, -1) 
                if event.key == pygame.K_DOWN: gen.player.check(0, 1)
                if event.key == pygame.K_LEFT: gen.player.check(-1, 0)
                if event.key == pygame.K_RIGHT: gen.player.check(1, 0)
                gen.ai_go()
                gen.render_all()
        elif ait.game_state == 'dead':
            gen.render_all()
        else:
            return 'didnt-take-turn'

def mainloop():
    while 1:
        handle_keys()
        victory_check()

def victory_check():
    if len(gen.all_enemies) == 0:
        print('Win!')

game = Game()

