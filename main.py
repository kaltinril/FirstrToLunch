# This program is written without optimizations for easier understanding.
# Loops are used instead of mapping, list comprehension, or lambda
# Loops should be "fast enough" for us for this example
import sys
import pygame
from pygame.locals import * # Things like QUIT
import math

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


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def draw_board(screen, objects, object_images, rotate_angle):

    for o in objects:
        if o[0] == 'A':
            screen.blit(pygame.transform.rotate(object_images[12], rotate_angle), (o[1], o[2]))
        elif o[0] == 'a':
            screen.blit(pygame.transform.rotate(object_images[0], -rotate_angle), (o[1], o[2]))
        elif o[0] == '!':
            screen.blit(object_images[1], (o[1], o[2]))
        elif o[0] == '@':
            screen.blit(object_images[2], (o[1], o[2]))
        elif o[0] == '#':
            screen.blit(object_images[3], (o[1], o[2]))
        elif o[0] == '$':
            screen.blit(object_images[4], (o[1], o[2]))
        elif o[0] == '%':
            screen.blit(object_images[5], (o[1], o[2]))
        elif o[0] == '1':
            screen.blit(object_images[7], (o[1], o[2]))
        elif o[0] == '2':
            screen.blit(object_images[8], (o[1], o[2]))
        elif o[0] == '3':
            screen.blit(object_images[9], (o[1], o[2]))
        elif o[0] == '4':
            screen.blit(object_images[10], (o[1], o[2]))
        elif o[0] == '5':
            screen.blit(object_images[11], (o[1], o[2]))
        elif o[0] == 'E':
            screen.blit(object_images[13], (o[1], o[2]))
        elif o[0] == 'S':
            #sin = math
            #scaled = pygame.transform.scale(object_images[14], (32*(rotate_angle / 360), 720))
            screen.blit(object_images[14], (o[1], o[2]))

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

    cloudy = pygame.image.load('images/cloudy.png')
    cloudy = pygame.transform.scale(cloudy, (96, 96))  # 32, 25

    vines = pygame.image.load('images/vines.png')
    vines = pygame.transform.scale(vines, (96, 96))  # 32, 25

    rings = pygame.image.load('images/rings.png')
    rings = pygame.transform.scale(rings, (196, 196))  # 32, 25

    goo = pygame.image.load('images/goo.png')
    goo = pygame.transform.scale(goo, (196, 196))  # 32, 25

    bluered = pygame.image.load('images/bluered.png')
    bluered = pygame.transform.scale(bluered, (196, 196))  # 32, 25

    station = pygame.image.load('images/sat.png')
    station = pygame.transform.scale(station, (32, 32))  # 32, 25

    img_one = pygame.image.load('images/one.png')
    img_one = pygame.transform.scale(img_one, (32, 32))
    img_two = pygame.image.load('images/two.png')
    img_two = pygame.transform.scale(img_two, (32, 32))
    img_three = pygame.image.load('images/three.png')
    img_three = pygame.transform.scale(img_three, (32, 32))
    img_four = pygame.image.load('images/four.png')
    img_four = pygame.transform.scale(img_four, (32, 32))
    img_five = pygame.image.load('images/five.png')
    img_five = pygame.transform.scale(img_five, (32, 32))

    asteroid1 = pygame.image.load('images/asteroid1.png')
    asteroid1 = pygame.transform.scale(asteroid1, (32, 32))

    earth = pygame.image.load('images/earth.png')
    earth = pygame.transform.scale(earth, (128, 128))
    start = pygame.image.load('images/start.png')
    start = pygame.transform.scale(start, (32, 32))

    object_images = [orange, cloudy, vines, rings, goo, bluered, station,
                     img_one, img_two, img_three, img_four, img_five,
                     asteroid1,
                     earth, start]

    command_list = load_command_file("commands.txt")

    game_map, objects = load_map_file("gameboard.txt")

    # game loop
    fps = 60.0
    fps_clock = pygame.time.Clock()
    time_elapsed_since_last_action = 0
    rotate_angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen and draw background
        gamescreen.fill(BLACK)
        gamescreen.blit(background, (0, 0))

        # Draw grid
        for x in range(0, int(SCREEN_WIDTH / 32)):
            pygame.draw.line(gamescreen, BLACK, (x * 32, 0), (x * 32, SCREEN_HEIGHT))

        for y in range(0, int(SCREEN_HEIGHT / 32)):
            pygame.draw.line(gamescreen, BLACK, (0, y * 32), (SCREEN_WIDTH, y * 32))

        # Force to 60 FPS
        dt = fps_clock.tick(fps)
        # time_elapsed_since_last_action += dt
        # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
        # if time_elapsed_since_last_action > 250:
        #    snake.action()  # move the snake here
        #     time_elapsed_since_last_action = 0  # reset it to 0 so you can count again

        # draw planets and obstacles
        positions = ''
        rotate_angle = rotate_angle + ((dt / 1000) * 50)
        if rotate_angle > 360:
            rotate_angle = rotate_angle - 360
        draw_board(gamescreen, objects, object_images, rotate_angle)


        # draw players
        # update players positions
        # wait 1 second

        pygame.display.update()

if __name__ == "__main__":
    main()
