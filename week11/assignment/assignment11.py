"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp


# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = 'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE = 'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))


def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))


def guest_waiting():
    time.sleep(random.uniform(0, 2))


def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))


def cleaner(room_lock, id, start_time, cleanings):
    # Cleaner process function, takes the following parameters:
    # Room lock, cleaner id, program start time, and cleanings multiprocessing value.

    # Stop after running for TIME (60) seconds.
    while time.time() <= start_time + TIME:
        # Make the cleaner wait.
        cleaner_waiting()

        # Acquire the room lock (if possible) and store the return value (boolean) without blocking.
        have_room_lock = room_lock.acquire(block=False)

        # If we acquired the room lock, then clean the room and leave.
        if have_room_lock:
            # Update the number of times the room has been cleaned.
            cleanings.value += 1
            # Print the start cleaning message.
            print(STARTING_CLEANING_MESSAGE)
            # Call the cleaner_cleaning() function to print which cleaner is cleaning.
            cleaner_cleaning(id)
            # Print the stop cleaning message.
            print(STOPPING_CLEANING_MESSAGE)
            # Release the room lock.
            room_lock.release()


def guest(room_lock, party_lock, id, start_time, parties, guests_in_room):
    # Guest process function, takes the following parameters:
    # Room lock, party lock, guest id, program start time, parties multiprocessing value, and guests_in_room multiprocessing value.

    # Stop after running for TIME (60) seconds.
    while time.time() <= start_time + TIME:
        # Make the guest wait.
        guest_waiting()

        # Acquire the room and party locks (if possible) and store the return value (boolean) without blocking.
        have_room_lock = room_lock.acquire(block=False)
        have_party_lock = party_lock.acquire(block=False)

        # If we acquired both locks, then start the party since we are the first guest in the room.
        if have_room_lock and have_party_lock:
            # Update the amount of parties started.
            parties.value += 1
            # Print the start party message.
            print(STARTING_PARTY_MESSAGE)
            # Have the the first guest start partying, and update the value of the number of guests in the room.
            guests_in_room.value += 1
            guest_partying(id)
            guests_in_room.value -= 1

        elif have_room_lock == False and have_party_lock == True:
            # If we acquired only the party lock and not the room lock then it means there is a cleaner in the room,
            # so just release the party lock and wait again because we can't go in the room.
            party_lock.release()

        elif have_room_lock == False and have_party_lock == False:
            # If both locks are already acquired by the guests, then join the party.

            # Update the number of guests in the room and have the guest join the party in the room.
            guests_in_room.value += 1
            guest_partying(id)
            guests_in_room.value -= 1

            # Check if this guest is the last guest to leave the room after the guest is done partying.
            if guests_in_room.value == 0:
                # If the room is empty, then stop the party and release the room and party locks.
                print(STOPPING_PARTY_MESSAGE)
                room_lock.release()
                party_lock.release()


def main():
    # Start time of the running of the program.
    start_time = time.time()

    # Creating a room lock and a party lock.
    room_lock = mp.Lock()
    party_lock = mp.Lock()

    # Create mulitprocessing values to track the number of cleanings, parties, and guests in the room.
    cleanings = mp.Value('i', 0)
    parties = mp.Value('i', 0)
    guests_in_room = mp.Value('i', 0)

    # Creating a list of cleaner processes and guest processes.
    cleaners = [mp.Process(target=cleaner, args=(room_lock, id, start_time, cleanings,))
                for id in range(1, CLEANING_STAFF + 1)]
    guests = [mp.Process(target=guest, args=(
        room_lock, party_lock, id, start_time, parties, guests_in_room)) for id in range(1, HOTEL_GUESTS + 1)]

    # Starting and joining each cleaner and guest process.
    [cleaner.start() for cleaner in cleaners]
    [guest.start() for guest in guests]
    [cleaner.join() for cleaner in cleaners]
    [guest.join() for guest in guests]

    # Getting the integer values for the number of cleanings and parties.
    cleaned_count = cleanings.value
    party_count = parties.value

    # Output the results.
    print(
        f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()
