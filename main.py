# This program is written without optimizations for easier understanding.
# Loops are used instead of mapping, list comprehension, or lambda
# Loops should be "fast enough" for us for this example
import sys
import pygame
from pygame.locals import * # Things like QUIT

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Load file: Load a file and return the commands
def load_command_file(filename):
    # Open the file and read all lines into a list
    command_file = open(filename, "r")
    command_list_input = command_file.readlines()

    # Convert all commands to lowercase, remove leading and trailing white space, and then add to command_list
    command_list = []
    for command in command_list_input:
        command_list.append(command.lower().strip())

    command_file.close()
    return command_list

# Loads a file with locations in it, using characters
# Mapping:
#   SPACE   = empty
#   -       = "wall"
#   E       = Earth image location
#   S       = "Start" image location
#   F       = "Finish" image location
#   f       = finish planet
#   number  = Next waypoint in order
#   special = Planet to display near the matching number on keyboard.  I.E. 1 and !, 2 and @, 3 adn #, 4 and $, etc.
#   A       = Asteroid type 1
#   a       = asteroid type 2
#
def load_map_file(filename):
    # Open the file and read all lines into a list
    map_file = open(filename, "r")
    map_lines_raw = map_file.readlines()

    # Remove leading and trailing white space
    map_lines = []
    for line in map_lines_raw:
        map_lines.append(line.strip())

    # Convert all commands to lowercase, remove leading and trailing white space, and then add to command_list
    cols = len(map_lines[0])
    rows = len(map_lines)
    game_map = [[0 for i in range(rows)] for j in range(cols)]

    for y in range(0, rows):
        for x in range(0, cols):
            game_map[x][y] = map_lines[y][x]

    print("Game size", "Width", cols, "height", rows)

    print(" 3 2", game_map[3][2])
    map_file.close()

    objects = []
    for y in range(0, rows):
        for x in range(0, cols):
            if game_map[x][y] != ' ' and game_map[x][y] != '-':
                # Object, X position on screen, Y position on screen
                object = [game_map[x][y], (x * 32), (y * 32)]
                objects.append(object)


    return game_map, objects


def draw_board(screen, objects, object_images):

    for o in objects:
        if o[0] == 'E' or o[0] == 'A' or o[0] == 'a' or o[0] == '!' or o[0] == '@' or o[0] == '#' or o[0] == '$' or o[0] == '%' or o[0] == 'f' or o[0] == 'F':
            screen.blit(object_images[0], (o[1], o[2]))

    return 0



def main():
    # initialize everything for drawing
    pygame.init()
    gamescreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load game objects
    background = pygame.image.load('background.jpg')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    orange = pygame.image.load('images/orange.png')
    orange = pygame.transform.scale(orange, (32, 25)) # 32, 25

    object_images = []
    object_images.append(orange)

    command_list = load_command_file("commands.txt")

    game_map, objects = load_map_file("gameboard.txt")

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen and draw background
        gamescreen.fill(BLACK)
        gamescreen.blit(background, (0, 0))

        # draw planets and obstacles
        positions = ''
        draw_board(gamescreen, objects, object_images)

        # Draw grid
        for x in range(0, int(SCREEN_WIDTH / 32)):
            pygame.draw.line(gamescreen, WHITE, (x * 32, 0), (x * 32, SCREEN_HEIGHT))

        for y in range(0, int(SCREEN_HEIGHT / 32)):
            pygame.draw.line(gamescreen, WHITE, (0, y * 32), (SCREEN_WIDTH, y * 32))

        # draw players
        # update players positions
        # wait 1 second


        pygame.display.update()

if __name__ == "__main__":
    main()
