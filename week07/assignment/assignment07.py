'''
Requirements
1. Create a multiprocessing program that connects the processes using Pipes.
2. Create a process from each of the following custom process classes, 
   Marble_Creator, Bagger, Assembler, and Wrapper.
3. The Marble_Creator process will send a marble to the Bagger process using
   a Pipe.
4. The Bagger process will create a Bag object with the required number of
   marbles. 
5. The Bagger process will send the Bag object to the Assembler using a Pipe.
6. The Assembler process will create a Gift object and send it to the Wrapper
   process using a Pipe.
7. The Wrapper process will write to a file the current time followed by the 
   gift string.
8. The program should not hard-code the number of marbles, the various delays,
   nor the bag count. These should be obtained from the settings.txt file.
   
Questions:
1. Why can you not use the same pipe object for all the processes (i.e., why 
   do you need to create three different pipes)?
   > You need to create 3 different pipe objects because each pipe can only connect two processes together,
   > and since we have 4 different processes, the connections look like:
   > Marble_Creator ==pipe==> Bagger ==pipe==> Assembler ==pipe==> Wrapper
2. Compare and contrast pipes with queues (i.e., how are the similar or different)?
   > Queues are a data structure that can be used by many different processes,
   > whereas a pipe only connects two specific processes together to send and receive data directly by each other.
'''

from datetime import datetime
import json
import multiprocessing as mp
import os
import random
import time

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


# Bag class.
class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


# Gift class.
class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


# Marble creator class.
class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    # Tuple of marble colors.
    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    # Marble class constructor.
    def __init__(self, creator_sender, settings, colors=colors):
        # Instantiate the superclass, and establish the pipe, colors, and settings dictionary.
        mp.Process.__init__(self)
        self.creator = creator_sender
        self.colors = colors
        self.settings = settings

    def run(self):
        # This will loop through "marble count" number of times.
        for _ in range(self.settings[MARBLE_COUNT]):
            # Get a random color from the list.
            color = random.choice(self.colors)
            self.creator.send(color)  # Send the new marble to the bagger.
            # Sleep before creating the next marble.
            time.sleep(self.settings[CREATOR_DELAY])

        # Once no more marbles are left to make, send None as a sentinel and close the pipe connection.
        self.creator.send(None)
        self.creator.close()


# Bagger class.
class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, creator_reciever, assembler_sender, settings):
        # Instantiate the superclass, the receiving pipe from the marble creator,
        # the sending pipe to the assembler, and the settings dictionary.
        mp.Process.__init__(self)
        self.bagger = creator_reciever
        self.sender = assembler_sender
        self.settings = settings

    def run(self):
        # Get the number of marbles to be put in each bag.
        bag_count = self.settings[BAG_COUNT]
        keep_bagging = True  # While loop controller.

        while keep_bagging:
            # Create a new bag.
            new_bag = Bag()

            # While the current bag has less than 7 marbles.
            while new_bag.get_size() < bag_count:
                # Receive the marble from the marble creator from the pipe.
                current_marble = self.bagger.recv()

                if current_marble is None:  # If the marble is none, then break out of the loop.
                    # Set keep_bagging to false so we don't send an unfilled bag to the assembler.
                    keep_bagging = False
                    break
                else:  # Otherwise, add the marble to the current bag.
                    new_bag.add(current_marble)

            if keep_bagging is False:  # Check if we need to stop bagging.
                break

            # Send the newly made bag to the assembler through the pipe.
            self.sender.send(new_bag)
            # Sleep before creating the next bag.
            time.sleep(self.settings[BAGGER_DELAY])

        # Once we are done making new bags, send None as a sentinel and close the pipe connection.
        self.sender.send(None)
        self.sender.close()


# Assembler class.
class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """

    # Tuple for large marble names.
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, assembler_reciever, wrapper_sender, settings, marble_names=marble_names):
        # Instantiate the superclass, and establish the receiver and sender pipes, the list of large
        # marble names, and the settings dictionary.
        mp.Process.__init__(self)
        self.assembler = assembler_reciever
        self.sender = wrapper_sender
        self.names = marble_names
        self.settings = settings

    def run(self):
        new_bag = ""  # Variable that will hold each new bag from the bagger.

        while new_bag is not None:
            # Get a random large marble.
            large_marble = random.choice(self.names)
            # Receive the new bag from the bagger.
            new_bag = self.assembler.recv()

            if new_bag is None:  # Check if the new bag is none and break if it is.
                break

            # Create a new gift object and send it to the wrapper.
            new_gift = Gift(large_marble, new_bag)
            self.sender.send(new_gift)
            # Sleep before assembling a new gift.
            time.sleep(self.settings[ASSEMBLER_DELAY])

        # Once there are no more gifts to make, send None as a sentinel and close the pipe connection.
        self.sender.send(None)
        self.sender.close()


# Wrapper class.
class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, wrapper_reciever, file, settings, gifts_made):
        # Instantiate the superclass, and establish the receiver pipe connection, the file to write to,
        # the settings dictionary, and the gifts_made multiprocessing value to track the number of gifts made.
        mp.Process.__init__(self)
        self.wrapper = wrapper_reciever
        self.file = file
        self.gift_count = gifts_made
        self.settings = settings

    def run(self):
        with open(self.file, 'w') as f:  # Open the file in write mode.
            gifts = ""
            while gifts is not None:  # While gifts received from the assembler are not none.
                gifts = self.wrapper.recv()  # Receive a new gift.

                if gifts is None:  # If the gift is None, then break.
                    break

                # Write the new gift with the time to the file.
                f.write(f'Created - {datetime.now().time()}: {gifts} \n')
                # Increase the gifts made counter by 1.
                self.gift_count.value += 1
                # Sleep before getting a new gift to write.
                time.sleep(self.settings[WRAPPER_DELAY])


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer.
    begin_time = time.perf_counter()

    # Load settings file.
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # Creating 3 pipe objects for the processes to share data between each other.
    creator_sender, creator_reciever = mp.Pipe()
    assembler_sender, assembler_reciever = mp.Pipe()
    wrapper_sender, wrapper_reciever = mp.Pipe()

    # Multiprocessing value object that will be used by the wrapper to track the number of gifts made.
    gifts_made = mp.Value('i', 0)

    # Delete the old boxes.txt file.
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    # Creating the marble_creator, bagger, assembler, and wrapper processes.
    print('Creating processes.')
    creator = Marble_Creator(creator_sender, settings)
    bagger = Bagger(creator_reciever, assembler_sender, settings)
    assembler = Assembler(assembler_reciever, wrapper_sender, settings)
    wrapper = Wrapper(wrapper_reciever, BOXES_FILENAME, settings, gifts_made)

    # Starting all of the above processes.
    print('Starting processes.')
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    # Joining all of the above processes.
    print('Waiting for processes to finish.')
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    # Print the boxes.txt file.
    print()
    display_final_boxes(BOXES_FILENAME)

    # Print the number of gifts created and the time taken.
    print(f"\nNumber of gifts created: {gifts_made.value}")
    print(f"Time taken: {(time.perf_counter() - begin_time):.2f} seconds")


if __name__ == '__main__':
    main()
