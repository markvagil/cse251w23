'''
Requirements
1. Create a recursive program that finds the solution path for each of the provided mazes.
'''

import math
from screen import Screen
from maze import Maze
import cv2
import sys

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions

def solve(maze: Maze, current_position, solution_path: list):
    """ Solve the maze. The path object should be a list (x, y) of the positions 
        that solves the maze, from the start position to the end position. """

    # Check if the position we moved to is the end position.
    if maze.at_end(current_position[0], current_position[1]):
        return solution_path  # Return the solution path.

    # Get the possible moves from our current position.
    p_moves = maze.get_possible_moves(current_position[0], current_position[1])

    if len(p_moves) > 0:  # If possible moves is not empty.
        for new_position in p_moves:  # For every possible move.
            # If we can move to the new position.
            if maze.can_move_here(new_position[0], new_position[1]):
                # Move to the new position.
                maze.move(new_position[0], new_position[1], COLOR)

                # Append that new position to the solution path.
                solution_path.append(new_position)

                # Get the return value from that move (recursive call).
                temp = solve(maze, new_position, solution_path)

                # Add the return value to the list, and check if it is greater than 0.
                # If it is, then it means we can return part of a possible solution path.
                if isinstance(temp, list):
                    if len(temp) > 0:
                        return temp

                # If we make it here it means that we didn't get a solution path and hit a dead end
                # which means we need to restore the position we are at and remove it from the path list.
                maze.restore(new_position[0], new_position[1])
                solution_path.remove(new_position)
    else:
        # If no possible moves, then return empty solution path.
        return []


def get_solution_path(filename):
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    start_position = maze.get_start_pos()
    maze.move(start_position[0], start_position[1], COLOR)
    solution_path = solve(maze, start_position, [])

    print(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return solution_path


def find_paths():
    files = ('verysmall.bmp', 'verysmall-loops.bmp',
             'small.bmp', 'small-loops.bmp',
             'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    print('*' * 40)
    print('Part 1')
    for filename in files:
        print()
        print(f'File: {filename}')
        solution_path = get_solution_path(filename)
        print(f'Found path has length          = {len(solution_path)}')
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_paths()


if __name__ == "__main__":
    main()
