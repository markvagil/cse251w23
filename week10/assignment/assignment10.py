'''
Purpose: Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        ***************************************************
        ** DO NOT search for a solution on the Internet, **
        ** your goal is not to copy a solution, but to   **
        ** work out this problem.                        **
        ***************************************************

- When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be an issue picking up the two forks since the waiter is in control of 
  the forks. When a philosopher is finished eating, it will inform the waiter that they
  are finished.  If the waiter indicates to a philosopher that they can not eat, the 
  philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout. This can be useful to not
  block when trying to acquire a lock.
- Philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- Philosophers need to think (digest?) for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks (minimum of 5 philosophers).
- Use threads for this problem.
- Provide a way to "prove" that each philosophers will not starve. This can be counting
  how many times each philosophers eat and display a summary at the end. Or, keeping track
  how long each philosopher is eating and thinking.
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat. Hint, they are
  sitting in a circle.
'''

import time
import threading
import random

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5


# Waiter class, controls the eating of the philosophers.
class Waiter():
    def __init__(self):
        # Initialize a list of forks (locks).
        self.forks = [threading.Lock() for _ in range(PHILOSOPHERS)]

    # Can_eat() checks if a philosopher can pick up both forks and eat.
    def can_eat(self, philosopher_id):
        if self.forks[philosopher_id].locked() == False and self.forks[(philosopher_id + 1) % 5].locked() == False:
            # Return true if both forks are not locked.
            return True
        else:
            return False

    def take_forks(self, philosopher_id):
        # From philosopher perspective, acquire right fork.
        self.forks[philosopher_id].acquire()
        # From philosopher perspective, acquire left fork.
        self.forks[(philosopher_id + 1) % 5].acquire()

    def release_forks(self, philosopher_id):
        # Release both forks for this philosopher.
        self.forks[philosopher_id].release()
        self.forks[(philosopher_id + 1) % 5].release()

    '''
    # DEBUGGING FUNCTION
    def get_forks(self, ph_id):
        output = f"PH:{ph_id} -- [F-0: {self.forks[0].locked()}, F-1: {self.forks[1].locked()}, F-2: {self.forks[2].locked()}, F-3: {self.forks[3].locked()}, F-4: {self.forks[4].locked()}]\n"
        print(output)
    '''


# Philosopher threading class.
class Philosopher(threading.Thread):
    def __init__(self, id, waiter):
        # Initiate the threading class, philosopher id, the waiter, number of meals eaten, time spent eating, and time spent thinking.
        super().__init__()
        self.ph_id = id
        self.waiter = waiter
        self.meals_eaten = 0
        self.time_eating = 0
        self.time_thinking = 0

    def run(self):
        keep_going = True

        while keep_going:
            # If we can eat, then eat.
            if self.waiter.can_eat(self.ph_id):
                print(f"Philosopher {self.ph_id} IS EATING")

                # Lock the forks we need so we can eat.
                self.waiter.take_forks(self.ph_id)

                # Increment the number of meals eaten.
                self.meals_eaten += 1

                # Sleep between 1 to 3 seconds to eat.
                eating_time = random.choice([1, 2, 3])
                time.sleep(eating_time)

                # Update the time spent eating.
                self.time_eating += eating_time

                # Unlock the forks we don't need anymore since we are done eating.
                self.waiter.release_forks(self.ph_id)

            # Check if we have consumed our fair share of meals.
            if self.meals_eaten >= MAX_MEALS / PHILOSOPHERS:
                # If we have, then break.
                keep_going = False
                break
            else:
                # Otherwise, do some thinking.
                print(f"Philosopher {self.ph_id} IS THINKING")

                # Sleep between 1 to 3 seconds to think.
                thinking_time = random.choice([1, 2, 3])
                time.sleep(thinking_time)

                # Update the time spent thinking.
                self.time_thinking += 1

    # Function that returns a string of the statistics from this philosopher.
    def get_stats(self):
        return f"Philosopher {self.ph_id} - MEALS EATEN: {self.meals_eaten} - eating: {self.time_eating} sec - thinking: {self.time_thinking} sec"


def main():
    # Start the timer.
    start_time = time.time()

    # Create the waiter.
    waiter = Waiter()

    # Creating a list that will hold the philosophers with a numeric id.
    ph_list = []

    # Create each philosopher thread and add them to the list.
    for i in range(PHILOSOPHERS):
        new_ph = Philosopher(i, waiter)
        ph_list.append(new_ph)

    # Start the philosophers eating and thinking and join them.
    [ph.start() for ph in ph_list]
    [ph.join() for ph in ph_list]

    # Display the total runtime of the program, and how many times each philosopher ate, and how long they were eating and thinking for.
    print(f"\nTotal runtime: {time.time() - start_time}\n")
    [print(ph.get_stats()) for ph in ph_list]


if __name__ == '__main__':
    main()
