"""
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

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- When a philosopher is not eating, it will think for 3 to 5 seconds.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""

import time
import random
import threading

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
TIME = 60

max_meals = MAX_MEALS


class Waiter(threading.Thread):

    def __init__(self):

        # create the 5 forks and give them the ID's
        self.forks = [threading.Lock() for i in range(PHILOSOPHERS)]

    def take_forks(self, philosopher_id):

        # left fork is the philosophers id
        left_fork = philosopher_id

        # right fork is the id to the right. The % operator will cycle its way back to 0 once it gets to the last philosopher
        right_fork = (philosopher_id + 1) % 5

        # acquire both left and right forks
        self.forks[left_fork].acquire()
        self.forks[right_fork].acquire()

    def release_forks(self, philosopher_id):
        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % 5

        # release both left and right forks
        self.forks[left_fork].release()
        self.forks[right_fork].release()


class Philosopher(threading.Thread):

    def __init__(self, philosopher_id, waiter: Waiter, start_time):
        super().__init__()
        self.meal_count = 0
        self.philosopher_id = philosopher_id
        self.waiter = waiter
        self.start_time = start_time

    def run(self):
        while (time.time() - self.start_time < TIME):

            print(f"{self.philosopher_id}: is THINKING")

            # choose between 1, 2, or 3 seconds of eating time
            time.sleep(random.choice([1, 2, 3]))

            # get the forks from the waiter
            self.waiter.take_forks(self.philosopher_id)

            print(f"{self.philosopher_id}: is EATING")

            # release the forks
            self.waiter.release_forks(self.philosopher_id)

            self.meal_count += 1

            if self.meal_count == 5:
                break


def main():

    start_time = time.time()

    waiter = Waiter()

    philosophers = []

    for i in range(PHILOSOPHERS):
        philosophers.append(Philosopher(i, waiter, start_time))

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()

    for philosopher in philosophers:
        print(
            f"Philosopher{philosopher.philosopher_id} ate {philosopher.meal_count} meals")


if __name__ == '__main__':
    main()
