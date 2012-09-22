### Outlast in pygcurse
import pygame, math, sys, random
from pygame.locals import *
import pygcurse
import MapGen as gen
import AITracker as ait
import GuiHandler as gui


MAPWIDTH=gui.MAPWIDTH
MAPHEIGHT=gui.MAPHEIGHT

debug_mode = False

dirtytiles = []

victory = False

class Game:
    def __init__(self, flags=None):
        global mp
        mp = gen.init()
        if flags == 'debug':
            for y in range(gui.MAPHEIGHT):
                for x in range(gui.MAPWIDTH):
                    mp[x][y].explored = True
        gui.message('You hear zombies all around you.', pygame.Color(0,0,255))
        gen.render_all()
        mainloop()
            

def handle_keys():
    global playerx, playery, game_state

    turnkeys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            quit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKQUOTE:
            gui.win.setscreencolors(None, None, True)
            ait.game_state = 'normal'
            game = Game(flags = 'debug') 
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSLASH:
            if gui.win.fullscreen == True:
                gui.win.fullscreen = False
            else:
                gui.win.fullscreen = True
            gen.render_all()


        if ait.game_state == 'normal':        
            if event.type == pygame.KEYUP and event.key in turnkeys:
                if event.key == pygame.K_UP: gen.player.check(0, -1) 
                if event.key == pygame.K_DOWN: gen.player.check(0, 1)
                if event.key == pygame.K_LEFT: gen.player.check(-1, 0)
                if event.key == pygame.K_RIGHT: gen.player.check(1, 0)
                if event.key == pygame.K_7: gen.player.check(-1, -1)
                if event.key == pygame.K_8: gen.player.check(0, -1)
                if event.key == pygame.K_9: gen.player.check(1, -1)
                if event.key == pygame.K_4: gen.player.check(-1, 0)
                if event.key == pygame.K_6: gen.player.check(1, 0)
                if event.key == pygame.K_1: gen.player.check(-1, 1)
                if event.key == pygame.K_2: gen.player.check(0, 1)
                if event.key == pygame.K_3: gen.player.check(1, 1)
                gui.msgs_updated = False
                gen.ai_go()
                gen.render_all()
            elif event.type == pygame.KEYUP and pygcurse.interpretkeyevent(event) == '?':
                gui.win.setscreencolors(None, None, True)
                gui.list(('7 8 9', '4 5 6   Movement Keys', '1 2 3', '', 'Arrow Keys:',  '      UP', 'LEFT DOWN RIGHT', '', '`  : debug', '\  : fullscreen', 'ESC: Quit', '', 'press any key to return'))
                gui.win.update()
                gui.win.blittowindow()
                gui.win.setscreencolors(None, None, True)


        elif ait.game_state == 'dead':
            gen.render_all()
  
        elif ait.game_state == 'menu':
            if event.type == pygame.KEYUP:
                return pygcurse.interpretkeyevent(event)
        # elif ait.game_state == 'test':

        else:
            return 'didnt-take-turn'


def MainMenu():
    while 1:
        ait.game_state = 'menu'
        gui.win.setscreencolors(None, None, True)
        options = ['Start New Game']
        headers = [gui.header('XTRICATE OUTLAST: A zombie apocalypse roguelike', pygame.Color(255,0,0)), gui.header('By Alasdair McLean', pygame.Color(170,170,170))]
        gui.menu(headers, options, gui.WIN_HEIGHT // 3)
        # gui.win.putchars('XTRICATE OUTLAST: A zombie apocalypse roguelike', (gui.WIN_WIDTH // 2) - 23, gui.WIN_HEIGHT // 3, pygame.Color(255,0,0))
        # gui.win.putchars('By Alasdair McLean', (gui.WIN_WIDTH // 2) - 7, (gui.WIN_HEIGHT // 3) + 1, pygame.Color(255,255,255))
        # gui.win.putchars('1) Start New Game', (gui.WIN_WIDTH // 2) - 6, (gui.WIN_HEIGHT // 3) + 3, pygame.Color(150,150,150))
        gui.win.update()
        gui.win.blittowindow()
        choice = handle_keys()
        if choice == 'a':
            gui.win.setscreencolors(None, None, True)
            ait.game_state = 'normal'
            game = Game()
        

def mainloop():
    while 1:
        handle_keys()
        victory_check()

def victory_check():
    global victory
    if len(gen.all_enemies) == 0 and victory == False:
        gui.message('It is quiet.', pygame.Color(255,255,0))
    victory = True

MainMenu()

