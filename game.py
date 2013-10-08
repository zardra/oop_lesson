import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
from random import randint

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID  = True

class Character(GameElement):
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    IMAGE = "Horns"

    # defining how to move a character
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

class Gem(GameElement):
    
    # how to add gems to a player's inventory
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" 
            % (len(player.inventory)))

    IMAGE = "BlueGem"
    SOLID = False

class Key(GameElement):

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key!")
        print player.inventory

    IMAGE = "Key"
    SOLID = False

class Chest(GameElement):

    def interact(self, player):
        for i in player.inventory:
            if type(i) == Key:
                chest2 = Chest()
                chest2.IMAGE = "ChestOpen"
                GAME_BOARD.register(chest2)
                GAME_BOARD.del_el(self.x, self.y)
                GAME_BOARD.set_el(self.x, self.y, chest2)
                chest2.SOLID = False

    IMAGE = "Chest"
    SOLID = True


####   End class definitions    ####
def initialize():
    """Put game initialization code here"""

    # initialize game with rocks in the following positions
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

    # make the last rock in the list not solid 
    rocks[-1].SOLID = False

 

    # message board
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # initialize game with objects
    gem1 = Gem()
    GAME_BOARD.register(gem1)
    GAME_BOARD.set_el(3, 1, gem1)

    gem2 = Gem()
    gem2.IMAGE = "OrangeGem"
    GAME_BOARD.register(gem2)
    GAME_BOARD.set_el(3, 3, gem2)


    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(5, 5, chest)

   # initialize game with player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    a_key = Key()
    GAME_BOARD.register(a_key)

    rand_x = randint(0, GAME_WIDTH-1)
    rand_y = randint(0, GAME_HEIGHT-1)

    while rand_x == PLAYER.x or rand_y == PLAYER.y:
        rand_x = randint(0, GAME_WIDTH-1)
        rand_y = randint(0, GAME_HEIGHT-1)
    else:
        GAME_BOARD.set_el(rand_x, rand_y, a_key)

def keyboard_handler():
    direction = None

    # interprets keyboard commands
    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    
    # moves a character if allowed
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        GAME_BOARD.erase_msg()

        # looks at next spot on the board
        if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_WIDTH:

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            # interact with player
            if existing_el:
                existing_el.interact(PLAYER)

            # check if the next spot can be moved to
            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

        else:
            GAME_BOARD.draw_msg("Don't go off the board!")




