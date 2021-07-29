# Maze generator -- Randomized Prim Algorithm

# Imports
import random
import sys

from colorama import Fore
from PIL import Image
from colorama import init
import argparse

parser = argparse.ArgumentParser(description='generates mazes')
parser.add_argument("--name", help="the file name of the resulting image", required=False)
parser.add_argument("--width", help="the width of the maze", default=25)
parser.add_argument("--height", help="the height of the maze", default=25)


# Functions
def print_maze(maze, height, width):
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'u':
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif maze[i][j] == 'c':
                print(Fore.GREEN + str(maze[i][j]), end=" ")
            else:
                print(Fore.RED + str(maze[i][j]), end=" ")

        print('\n')


# Find number of surrounding cells
def surrounding_cells(rand_wall):
    s_cells = 0
    if maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
        s_cells += 1

    return s_cells


wall = 'w'
cell = 'c'
unvisited = 'u'
maze = []


def make_maze(width, height):
    # Main code
    # Init variables

    # Initialize colorama
    init()

    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = cell
    walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
             [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

    # Denote walls in maze
    maze[starting_height - 1][starting_width] = 'w'
    maze[starting_height][starting_width - 1] = 'w'
    maze[starting_height][starting_width + 1] = 'w'
    maze[starting_height + 1][starting_width] = 'w'

    while walls:
        # Pick a random wall
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        # Check if it is a left wall
        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
                # Find the number of surrounding cells
                s_cells = surrounding_cells(rand_wall)

                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Bottom cell
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Leftmost cell
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if rand_wall[0] != 0:
            if maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == 'c':

                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Leftmost cell
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Rightmost cell
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if rand_wall[0] != height - 1:
            if maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == 'c':

                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the right wall
        if rand_wall[1] != width - 1:
            if maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == 'c':

                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'u':
                maze[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, width):
        if maze[1][i] == 'c':
            maze[0][i] = 'c'
            break

    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == 'c':
            maze[height - 1][i] = 'c'
            break

    return maze


def to_bmp(maze):
    img = Image.new('L', (len(maze), len(maze[0])))
    pixels = img.load()
    for i in range(0, len(maze)):
        for e in range(0, len(maze[0])):
            if maze[i][e] == 'w':
                pixels[i, e] = 102
    img = img.resize((len(maze) * 10, len(maze[0]) * 10), 0)
    return img


if __name__ == "__main__":
    args = parser.parse_args()
    bmp = to_bmp(make_maze(int(args.width), int(args.height)))
    bmp.save('C:\\Users\\gabri\\dev\\Discord\\pism-discorp-bot\\mazes\\%s.png' % args.name)
