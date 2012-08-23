### Outlast in pygcurse
import pygame, math, sys
from pygame.locals import *
import pygcurse

playerx = 40
playery = 25

win = pygcurse.PygcurseWindow(80, 50, 'Xtricate Games: Outlast')
win.autoupdate = False
# class Object():

# def __init__(self, x, y, char):
#     self.x = x
#     self.y = y
#     self.char = char
def mainloop():
    global playerx
    global playery
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP: playery -= 1
                if event.key == pygame.K_DOWN: playery += 1
                if event.key == pygame.K_LEFT: playerx -= 1
                if event.key == pygame.K_RIGHT: playerx += 1

            if event.type == QUIT:
                return
            win.putchars('@', x=playerx, y=playery)
            win.update()
            win.setscreencolors(None, None, clear=True)


mainloop()

