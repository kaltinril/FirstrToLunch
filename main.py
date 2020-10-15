# This program is written without optimizations for easier understanding.
# Loops are used instead of mapping, list comprehension, or lambda
# Loops should be "fast enough" for us for this example
import sys
import pygame
from pygame.locals import * # Things like QUIT
import math
from player import Player

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# Draw a string of text to the game screen
# At the specific location
# With the specific font and color
# All method/functions must be defined before they are used
def draw_text(screen, text, font, location, text_color):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    text_rect.center = location
    screen.blit(text_surface, text_rect)

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
            adj = (40 * math.sin(rotate_angle / 16))
            screen.blit(pygame.transform.rotate(object_images[7], adj), (o[1], o[2]))
        elif o[0] == '2':
            adj = (40 * math.sin(rotate_angle / 16))
            screen.blit(pygame.transform.rotate(object_images[8], adj), (o[1], o[2]))
        elif o[0] == '3':
            adj = (40 * math.sin(rotate_angle / 16))
            screen.blit(pygame.transform.rotate(object_images[9], adj), (o[1], o[2]))
        elif o[0] == '4':
            adj = (40 * math.sin(rotate_angle / 16))
            screen.blit(pygame.transform.rotate(object_images[10], adj), (o[1], o[2]))
        elif o[0] == '5':
            adj = (40 * math.sin(rotate_angle / 16))
            screen.blit(pygame.transform.rotate(object_images[11], adj), (o[1], o[2]))
        elif o[0] == 'E':
            screen.blit(object_images[13], (o[1], o[2]))
        elif o[0] == 'S':
            adj = math.sin(rotate_angle / 4)
            scaled = pygame.transform.scale(object_images[14], (32 + int(adj * 5), 32 + int(adj * 5)))
            screen.blit(scaled, (o[1], o[2]))
        elif o[0] == 'F':
            adj = math.sin(rotate_angle / 4)
            scaled = pygame.transform.scale(object_images[15], (32 - int(adj * 5), 32 - int(adj * 5)))
            screen.blit(scaled, (o[1], o[2]))

    return 0


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def main():
    # initialize everything for drawing
    pygame.init()
    gamescreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Setup game fonts
    font = pygame.font.Font("freesansbold.ttf", 26)

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
    flags = pygame.image.load('images/flags.png')
    flags = pygame.transform.scale(flags, (32, 32))

    rocket = pygame.image.load('images/rocket.png')
    rocket = pygame.transform.scale(rocket, (32, 32))

    object_images = [orange, cloudy, vines, rings, goo, bluered, station,
                     img_one, img_two, img_three, img_four, img_five,
                     asteroid1,
                     earth, start, flags,
                     rocket]

    # Load map
    game_map, objects = load_map_file("gameboard.txt")

    # Get starting location
    start_pos = [0, 0]
    for o in objects:
        if o[0] == 'S':
            start_pos[0] = int(o[1] / 32)
            start_pos[1] = int(o[2] / 32)

    # Load players
    player1_list = load_command_file("player1.txt")
    player2_list = load_command_file("player2.txt")
    player3_list = load_command_file("player3.txt")
    player4_list = load_command_file("player4.txt")
    player5_list = load_command_file("player5.txt")

    p1 = Player('Chris', 10, player1_list)
    p2 = Player('Johnise', 10, player2_list)
    p3 = Player('Steve', 10, player3_list)
    p4 = Player('Marty', 10, player4_list)
    p5 = Player('Cé', 10, player5_list)

    players = [p1, p2, p3, p4, p5]

    for p in players:
        p.set_position(start_pos.copy())

    any_finished = False
    all_finished = False

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
        time_elapsed_since_last_action += dt


        # draw planets and obstacles
        positions = ''
        rotate_angle = rotate_angle + ((dt / 1000) * 50)
        if rotate_angle > 360:
            rotate_angle = rotate_angle - 360
        draw_board(gamescreen, objects, object_images, rotate_angle)


        # draw players
        for i in range(0, 5):
            new_sprite = rot_center(object_images[16], -players[i].facing)
            x = players[i].position[0] * 32
            y = players[i].position[1] * 32
            gamescreen.blit(new_sprite, (x, y))
            text_color = GREEN
            if players[i].is_dead():
                text_color = RED
            elif players[i].no_fuel():
                text_color = WHITE
            elif players[i].no_moves():
                text_color = BLUE

            if y == 0:
                y = y + 32 + 32

            if not all_finished:
                draw_text(gamescreen, players[i].name, font, (x + 16, y - 16), text_color)
            else:
                draw_text(gamescreen, players[i].name + " " + str(players[i].points), font, (x + 16, y - 16), text_color)
        # update players positions

        # wait 1 second before moving
        # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
        if time_elapsed_since_last_action > 250:
            for i in range(0, 5):
                players[i].move(game_map, any_finished)
                # players[i].debug_print()
            time_elapsed_since_last_action = 0  # reset it to 0 so you can count again

        # Check if anyone finished this round
        total_complete = 0
        for p in players:
            if p.finished:
                any_finished = True

            if p.finished or p.complete or p.dead or p.no_fuel() or p.no_moves():
                total_complete = total_complete + 1

        if total_complete == len(players) and not all_finished:
            all_finished = True

            print("")
            print("Game over!!!!")
            print("")

            # See who used the least fuel
            least_id = 0
            least_value = 100000
            i = 0
            for i in range(0, 5):
                if players[i].total_fuel_used < least_value:
                    least_value = players[i].total_fuel_used
                    least_id = i
            players[least_id].points = players[least_id].points + 10
            print(players[least_id].name, "Got 10 points for least fuel used overall!")

            # Check for players with more than 10 fuel left that finished
            for i in range(0, 5):
                if players[i].finished:
                    if players[i].fuel > 10:
                        players[i].points = players[i].points - 5
                        print(players[i].name, "lost 5 points for finishing with more than 10 fuel")

            # print out points:
            print("")
            print("====Final Point totals====")
            print("")
            for i in range(0, 5):
                print(players[i].name, "got", players[i].points, "and had", players[i].fuel, "left over")





        pygame.display.update()

if __name__ == "__main__":
    main()
