import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"

class Character(GameElement):
    IMAGE = "Horns"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None
####   End class definitions    ####
def initialize():
    """Put game initialization code here"""

    rock_positions = [
        (2, 1),
        (1, 2),
        (3, 2),
        (2, 3),
    ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")

def keyboard_handler():
    if KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        next_y = PLAYER.y -1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("You pressed down")
        next_y = PLAYER.y +1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("You pressed left")
        next_x = PLAYER.x -1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)    
    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("You pressed right")
        next_x = PLAYER.x +1
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)

