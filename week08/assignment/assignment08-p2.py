'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   >
   >
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   >
   >
'''

import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze, current_position, current_color, thread_count_lock):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    # TODO - add code here

    global stop
    global thread_count

    thread_count_lock.acquire()
    thread_count += 1
    thread_count_lock.release()

    not_at_end = True

    while not_at_end:
        # Move to the position we were given
        # print(f"color {current_color} is moving to {current_position}")
        if maze.can_move_here(current_position[0], current_position[1]):
            maze.move(current_position[0], current_position[1], current_color)

        if stop == True:
            return

        # Check if the position we moved to is the end position.
        if maze.at_end(current_position[0], current_position[1]):
            not_at_end = False  # false because we are at the end
            break
            # we need to stop all other threads

        else:
            # Get the possible moves from our current position.
            p_moves = maze.get_possible_moves(
                current_position[0], current_position[1])

            current_thread_move = ''

            if len(p_moves) == 0:  # If no possible moves
                print(f"Thread {current_color} returned.")
                return

            else:
                # position tuple assigned for this current thread
                current_thread_move = p_moves[0]

                if len(p_moves) > 1:  # If possible moves is greater than 1.
                    p_moves.pop(0)

                    for new_position in p_moves:  # For every possible move.
                        # If we can move to the new position.
                        if maze.can_move_here(new_position[0], new_position[1]):
                            new_thread = threading.Thread(
                                target=solve_find_end, args=(maze, new_position, get_color(), thread_count_lock,))
                            new_thread.start()

                if len(p_moves) == 1:
                    if maze.can_move_here(current_thread_move[0], current_thread_move[1]):
                        current_position = current_thread_move

    # happens after the while loop breaks
    stop = True
    print(f"End position found: {current_position}")


def find_end(filename, delay):

    global thread_count
    global stop
    stop = False
    thread_count = 0

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    thread_count_lock = threading.Lock()
    #              maze      start position      new color      threading lock
    main_thread = threading.Thread(target=solve_find_end, args=(
        maze, maze.get_start_pos(), get_color(), thread_count_lock,))
    main_thread.start()
    main_thread.join()

    print(f'Number of drawing commands = {screen.get_command_count()}')
    print(f'Number of threads created  = {thread_count}')

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


def find_ends():
    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    print('*' * 40)
    print('Part 2')
    for filename, delay in files:
        print()
        print(f'File: {filename}')
        find_end(filename, delay)
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_ends()


if __name__ == "__main__":
    main()
