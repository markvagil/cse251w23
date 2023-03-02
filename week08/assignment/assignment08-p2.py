'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   > My strategy would be to prepend the position of each thread starting from the end position to a list,
   > and return that list to the calling function all the way until the main thread so you would receive a
   > full solution path list containing every single position to get there.
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   > Using threads is a breadth-first search because you are exploring every single possible path from each branch at the same time
   > versus a depth-first where you explore a path all the way to the dead end and going along each branch from that deepest point.
   > The better search in my opinion is depth-first search algorithm because it travelled less space and took less time compared to 
   > the breadth-first search algorithm. But there are trade-offs to both algorithms and neither is perfect, and it also heavily depends
   > on what kind of maze you are solving.
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

    # Globalize the global variables.
    global stop
    global thread_count

    # If we can move to the position we were given, then move to it.
    if maze.can_move_here(current_position[0], current_position[1]):
        maze.move(current_position[0], current_position[1], current_color)

    # If the global stop variable is true, then return.
    if stop == True:
        return

    # Check if the position we moved to is the end position.
    if maze.at_end(current_position[0], current_position[1]):
        stop = True  # Set the global stop variable to true.
        return

    # Get the possible moves from our current position.
    p_moves = maze.get_possible_moves(current_position[0], current_position[1])

    # If possible moves is not empty.
    if len(p_moves) > 0:
        # Get the very first possible move from the list, store it, and remove it from the list.
        current_thread_move = p_moves[0]
        p_moves.pop(0)

        # Create a list that will hold each thread created.
        threads_list = []

        # If we can move to the very first possible move, then create a new thread, append it to the threads list, and start it.
        if maze.can_move_here(current_thread_move[0], current_thread_move[1]):
            new_thread = threading.Thread(
                target=solve_find_end, args=(maze, current_thread_move, current_color, thread_count_lock,))
            threads_list.append(new_thread)
            new_thread.start()

        # For every other possible move left in the moves list.
        for new_position in p_moves:
            # Check if we can move to the possible move position.
            if maze.can_move_here(new_position[0], new_position[1]):
                # Update the global thread count using the threading lock.
                thread_count_lock.acquire()
                thread_count += 1
                thread_count_lock.release()

                # Create a new thread for this move with a new color, start it, and add it to the threads list.
                new_thread = threading.Thread(
                    target=solve_find_end, args=(maze, new_position, get_color(), thread_count_lock,))
                threads_list.append(new_thread)
                new_thread.start()

        # Join all of the threads in the threads list.
        for thread in threads_list:
            thread.join()
    else:
        # If no possible moves, then return.
        return


def find_end(filename, delay):

    global thread_count
    global stop
    stop = False
    # Resetting to 1 because we are starting a main thread in this function.
    thread_count = 1

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    # Threading lock for accessing/modifying the thread count.
    thread_count_lock = threading.Lock()

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
