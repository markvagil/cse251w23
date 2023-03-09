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

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
EATING_DELAY = 3
THINKING_DELAY = 1


# TODO - create the waiter (A class would be best here).
class Waiter():
    def __init__(self):
        self.total_meals = 0
        self.forks = [threading.Lock() for _ in range(PHILOSOPHERS)]

    """def can_eat(self, philosopher_id):
        if self.forks[philosopher_id].locked() == False and self.forks[(philosopher_id + 1) % 5].locked() == False:
            # If both forks are not locked
            return True
        else:
            return False"""

    def can_eat(self, philosopher_id):
        if self.forks[philosopher_id].locked() == False and self.forks[(philosopher_id + 1) % 5].locked() == False:
            # If both forks are not locked
            return True
        else:
            return False

    def take_forks(self, philosopher_id):
        print(
            f"PH: {philosopher_id} is taking forks {philosopher_id} and {(philosopher_id + 1) % 5}")
        self.forks[philosopher_id].acquire()
        self.forks[(philosopher_id + 1) % 5].acquire()

    def release_forks(self, philosopher_id):
        print(
            f"PH: {philosopher_id} is releasing forks {philosopher_id} and {(philosopher_id + 1) % 5}")
        self.forks[philosopher_id].release()
        self.forks[(philosopher_id + 1) % 5].release()

    def update_total_meals(self):
        self.total_meals += 1

    def get_total_meals(self):
        return self.total_meals

    def get_forks(self):
        output = f"\n[Fork 0: {self.forks[0].locked()}, Fork 1: {self.forks[1].locked()}, Fork 2: {self.forks[2].locked()}, Fork 3: {self.forks[3].locked()}, Fork 4: {self.forks[4].locked()}]\n"
        print(output)


# TODO - create PHILOSOPHERS philosophers.
class Philosopher(threading.Thread):
    def __init__(self, id, waiter):
        super().__init__()
        self.ph_id = id
        self.waiter = waiter
        self.meals_eaten = 0
        self.time_eating = 0
        self.time_thinking = 0

    def run(self):
        keep_going = True

        while keep_going:
            # Check if we are done
            if self.check_if_done():
                keep_going = False
                break

            # If we can eat, then eat
            if self.waiter.can_eat(self.ph_id):
                print(f"Philosopher {self.ph_id} is eating.")
                self.waiter.take_forks(self.ph_id)
                self.waiter.get_forks()
                self.meals_eaten += 1
                self.time_eating += 1
                time.sleep(EATING_DELAY)
                self.waiter.release_forks(self.ph_id)
                self.waiter.update_total_meals()

            # Check if we are done
            if self.check_if_done():
                keep_going = False
                break

            # Now do some thinking
            # print(f"Philosopher {self.ph_id} is thinking.")
            self.time_thinking += 1
            time.sleep(THINKING_DELAY)

            # Check if we are done
            if self.check_if_done():
                keep_going = False
                break

    def get_stats(self):
        return f"Philosopher {self.ph_id} - MEALS EATEN: {self.meals_eaten} - eating: {self.time_eating} sec - thinking: {self.time_thinking} sec"

    def check_if_done(self):
        if self.waiter.get_total_meals() >= MAX_MEALS:
            return True


def main():
    start_time = time.time()

    waiter = Waiter()

    # Creating a list of philosophers with a numeric id
    ph_list = []

    for i in range(PHILOSOPHERS):
        new_ph = Philosopher(i, waiter)
        ph_list.append(new_ph)

    # TODO - Start them eating and thinking.
    [ph.start() for ph in ph_list]
    [ph.join() for ph in ph_list]

    # TODO - Display how many times each philosopher ate,
    #        how long they spent eating, and how long they spent thinking.
    print(f"\nTotal runtime: {time.time() - start_time}\n")
    [print(ph.get_stats()) for ph in ph_list]


if __name__ == '__main__':
    main()
