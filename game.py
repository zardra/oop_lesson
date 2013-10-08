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

class SliderRock(Rock):
    SOLID = False

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

    def interact(self, player):
        
        # Check if element in next spot is rock that can move
        next_location_slider = self.next_pos(PLAYER.last_direction)
        next_slider_x = next_location_slider[0]
        next_slider_y = next_location_slider[1]

        # Check if slider rock will go off the board
        if 0 <= next_slider_x < GAME_WIDTH and 0 <= next_slider_y < GAME_HEIGHT:
            # Check if there is a game element in the next spot
            neighbor_el = GAME_BOARD.get_el(next_slider_x, next_slider_y)
            if neighbor_el == None:
                GAME_BOARD.del_el(self.x, self.y)
                GAME_BOARD.set_el(next_slider_x, next_slider_y, self)
            else: 
                self.SOLID = True
        # If slider rock will go off the board, make it solid
        else:
            self.SOLID = True


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

    def move(self, direction):
        # print "Calling the move function"
        next_location = self.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        # print next_x, next_y

        if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT:
            
            #Check for game elements in next location
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            #If there is a game element, call it's interact method
            if existing_el:
                existing_el.interact(self)
    
            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(self.x, self.y)
                GAME_BOARD.set_el(next_x, next_y, self)
                

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
        GAME_BOARD.draw_msg("You just acquired a key! Now open the chest.")
        # print player.inventory

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

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True


####   End class definitions    ####
def initialize():
    """Put game initialization code here"""
    print "I'm in the initialize function"

    f = open("game_map.txt")
    list_of_strings = f.read().split("\n")
    
    for y in range(len(list_of_strings)):
        row = list_of_strings[y]
        for i in range(len(row)):
            if list_of_strings[y][i] == "w":
                wall = Wall()
                GAME_BOARD.register(wall)
                GAME_BOARD.set_el(i, y, wall)
            elif list_of_strings[y][i] == "t":
                tall_tree = TallTree()
                GAME_BOARD.register(tall_tree)
                GAME_BOARD.set_el(i, y, tall_tree)
            elif list_of_strings[y][i] == "r":
                rock = Rock()
                GAME_BOARD.register(rock)
                GAME_BOARD.set_el(i, y, rock)
            elif list_of_strings[y][i] == "s":
                slider_rock = SliderRock()
                GAME_BOARD.register(slider_rock)
                GAME_BOARD.set_el(i, y, slider_rock)
            elif list_of_strings[y][i] == "c":
                chest = Chest()
                GAME_BOARD.register(chest)
                GAME_BOARD.set_el(i, y, chest)

    f.close()

   # initialize game with player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)

    rand_x = randint(1, 7)
    rand_y = randint(0, 7)

    while GAME_BOARD.get_el(rand_x, rand_y):
        rand_x = randint(1, 7)
        rand_y = randint(0, 7)
    else:
        GAME_BOARD.set_el(rand_x, rand_y, PLAYER)

    # Initialize the game with a key and set it in a random location
    a_key = Key()
    GAME_BOARD.register(a_key)

    rand_x = randint(1, 6)
    rand_y = randint(1, 3)

    while GAME_BOARD.get_el(rand_x, rand_y):
        rand_x = randint(1, 6)
        rand_y = randint(1, 3)
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
        PLAYER.last_direction = direction
        PLAYER.move(direction)





