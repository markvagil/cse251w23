'''
Requirements
1. Using two threads, put cars onto a shared queue, with one thread consuming
   the items from the queue and the other producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
   
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   > You don't need to use locks when putting or getting items from a queue because queues are thread safe, there is no race condition.
   >
2. How would you define a semaphore in your own words?
   > A semaphore is like a lock that allows a specific number of threads to access data rather than just one thread at a time.
   > 
3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   > The join function is a blocking function because it waits for the thread to finish before returning it.
   > We want this because if join wasn't a blocking function then we would receive the thread object that would not have fully run,
   > meaning that we could receive a thread that hasn't even done anything if joined and started immediately or if joined after a small amount of time then
   > then the thread might only be half finished.
'''

from datetime import datetime
import time
import threading
import random
# DO NOT import queue

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

#########################
# NO GLOBAL VARIABLES!
#########################


class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, full_lot: threading.Semaphore, empty_lot: threading.Semaphore, car_queue, car_lock, car_count):
        # Call the superclass.
        threading.Thread.__init__(self)

        # Esatblish the semaphores, queue, lock, and the number of cars to make.
        self.sem_full_lot = full_lot
        self.sem_empty_lot = empty_lot
        self.car_queue = car_queue
        self.car_lock = car_lock
        self.car_count = car_count

    def run(self):
        for i in range(self.car_count):
            # Acquire the semaphore.
            self.sem_full_lot.acquire()

            # Create a new car object.
            new_car = Car()

            # Acquire the lock of the queue. (If desired, then uncomment.)
            # self.car_lock.acquire()

            # Put the new car in the queue.
            self.car_queue.put(new_car)

            # Release the lock of the queue and signal to the dealer that there are cars in the queue to be sold.
            # self.car_lock.release() # (If was locked at line 115.)
            self.sem_empty_lot.release()

        # Signal to the dealer that there are no more cars being made by putting a none object in the queue.
        self.sem_full_lot.acquire()
        self.car_queue.put(None)
        self.sem_empty_lot.release()


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self, full_lot: threading.Semaphore, empty_lot: threading.Semaphore, car_queue, car_lock, queue_stats):
        # Call the superclass.
        threading.Thread.__init__(self)

        # Esatblish the semaphores, queue, lock, and queue stats list.
        self.sem_full_lot = full_lot
        self.sem_empty_lot = empty_lot
        self.car_queue = car_queue
        self.car_lock = car_lock
        self.stats = queue_stats

    def run(self):
        while True:
            # Acquire semaphore for the queue.
            self.sem_empty_lot.acquire()

            # Acquire lock for the queue. (If desired, then uncomment.)
            # self.car_lock.acquire()

            # Increment the statistic for the size of the queue in the stats list.
            self.stats[self.car_queue.size()-1] += 1

            # Get the next car from the queue.
            current_car = self.car_queue.get()

            # Release the lock from the queue. (If was locked at line 150.)
            # self.car_lock.release()

            # If the car is none then end the loop, else print the car that was sold.
            if current_car == None:
                break
            else:
                print(
                    f"SOLD {current_car.make} {current_car.model}, {current_car.year}")

            # Release the semaphore of the queue so the manufacturer can start making cars again.
            self.sem_full_lot.release()

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    # Start a timer
    begin_time = time.perf_counter()

    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    # Semaphores for controlling access to the queue.
    full_lot = threading.Semaphore(MAX_QUEUE_SIZE)
    empty_lot = threading.Semaphore(0)

    # Creating the car queue object.
    car_queue = QueueTwoFiftyOne()

    # Creating a lock for the queue.
    car_lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car (i.e., increment the integer at the index using the
    # queue size).
    queue_stats = [0] * MAX_QUEUE_SIZE

    # Instantiating the manufacturer.
    car_maker = Manufacturer(
        full_lot, empty_lot, car_queue, car_lock, CARS_TO_PRODUCE)

    # Instantiating the dealer.
    car_dealer = Dealership(full_lot, empty_lot,
                            car_queue, car_lock, queue_stats)

    # Starting the manufacturer and dealer.
    car_maker.start()
    car_dealer.start()

    # Waiting for the manufacturer and dealer to finish.
    car_maker.join()
    car_dealer.join()

    # Setting the queue stats to be the stats from the dealer.
    queue_stats = car_dealer.stats

    # Outputting the total runtime.
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    # Plot car count vs queue size.
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


# Start of program.
if __name__ == '__main__':
    main()


# Assignment completed by Mark Vagil.
