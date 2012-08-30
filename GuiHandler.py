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

rlgui = pygcurse.PygcurseWindow(WIN_WIDTH, WIN_HEIGHT, 'Xtricate Presents: Outlast')
rlgui.autoupdate = False
rlgui.autoblit = False

all_msgs = []
cur_msgs = []

def message(text, color=pygame.Color(255,255,255)):
    new_msg_lines = textwrap.wrap(text, MSG_MAX_WID)
    for line in new_msg_lines:
        if len(cur_msgs) == MSG_HEIGHT:
            del cur_msgs[0]
        cur_msgs.append((line, color))
        all_msgs.append((line, color))



def msg_display():
    global msgs_updated
    y = MAPHEIGHT
    x = MSGX
    for (line, color) in cur_msgs:
        rlgui.putchars(line, x, y, fgcolor=color)
        y += 1
