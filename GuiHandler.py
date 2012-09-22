###Gui handler
import pygame, pygcurse, math, sys, textwrap
from pygame.locals import *

WIN_WIDTH=80
WIN_HEIGHT=50
HBARWID = 14
MSGX = HBARWID + 1
MSG_MAX_WID = WIN_WIDTH - HBARWID

MSG_HEIGHT = 5

MAPWIDTH=80
MAPHEIGHT=45

win = pygcurse.PygcurseWindow(WIN_WIDTH, WIN_HEIGHT, 'Xtricate Presents: Outlast')
win.autoupdate = False
win.autoblit = False

all_msgs = []
cur_msgs = []

class header:
    def __init__(self, text, color):
        self.color = color
        self.text = text

def message(text, color=pygame.Color(255,255,255)):
    all_msgs.append((text, color))
    cur_msgs.append((text, color))

def msg_update():
    global cur_msgs
    y = MAPHEIGHT
    x = MSGX
    for line in cur_msgs:
        #new_msg_lines = textwrap.wrap(line[0], MSG_MAX_WID)
        win.putchars(line[0], x, y, fgcolor=line[1])
        y += 1
    cur_msgs = []

def menu(headers, options, height):
    length = len(options)
    headerl = len(headers)
    if length + height + headerl > WIN_HEIGHT:
        raise ValueError('too many options in menu.')
    y = height + headerl + 2
    letter_index = ord('a')
    for header in headers:
        win.putchars(header.text, 20, height, fgcolor=header.color)
        height += 1
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        win.putchars(text, 20, y)
        y += 1
        letter_index += 1
    return chr(letter_index)

def list(lines):
    y = 0
    for line in lines:
        win.putchars(line, 0, y)
        y += 1




