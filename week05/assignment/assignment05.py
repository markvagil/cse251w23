'''
Requirements
1. Using multiple threads, put cars onto a shared queue, with one or more thread consuming
   the items from the queue and one or more thread producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. Produce a Plot of car count vs queue size (okay to use q.size since this is not a
   condition statement).
5. The number of cars produced by the manufacturer must equal the number of cars bought by the 
   dealership. Use necessary data objects (e.g., lists) to prove this. There is an assert in 
   main that must be used.
   
Questions:
1. How would you define a barrier in your own words?
   > A barrier is like a checkpoint where a specific number of threads have to catch up before they can proceed in their execution.
   >
2. Why is a barrier necessary in this assignment?
   > A barrier is necessary in this assignment because otherwise some manufacturers would put their sentinels before other manufacturers were finished
   > and that would cause errors in the program since not all of the required cars were produced and sold.
'''

from datetime import datetime, timedelta
import time
import threading
import random

import matplotlib.pyplot as plt

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!


# THIS IS THE PLOTS CLASS FROM THE WEEK 4 ASSIGNMENT.
# I MOVED IT HERE SO THAT YOU DIDN'T NEED TO IMPORT IT FROM ANOTHER FILE.
class Plots:
    """ Create plots for reports """

    def __init__(self, title=''):
        self._title = title

    def line(self, xdata, ydata,
             desc='', title='', x_label='', y_label='', show_plot=True, filename=''):
        # fig, ax = plt.subplots()
        plt.plot(xdata, ydata)

        if title == '':
            title = self._title

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        # fig.savefig("test.png")
        if filename != '':
            plt.savefig(filename)

        if show_plot:
            plt.show()

    def bar(self, xdata, ydata,
            desc='', title='', x_label='', y_label='', show_plot=True, filename=''):

        plt.bar(xdata, ydata)

        if title == '':
            title = self._title

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        # fig.savefig("test.png")
        if filename != '':
            plt.savefig(filename)

        if show_plot:
            plt.show()


class Car():
    """ This is the Car class that will be created by the manufacturers """

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

        # Display the car that has was just created in the terminal
        # self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, full_lot: threading.Semaphore, empty_lot: threading.Semaphore, car_queue, car_lock, barrier, sentinel, dealer_count):
        # Call the superclass.
        threading.Thread.__init__(self)

        # Number of cars this manufacturer will produce.
        self.cars_to_produce = random.randint(200, 300)     # Don't change

        # Esatblish the semaphores, queue, lock, barrier, sentinel, and dealer count.
        self.sem_full_lot = full_lot
        self.sem_empty_lot = empty_lot
        self.car_queue = car_queue
        self.car_lock = car_lock
        self.barrier = barrier
        self.sentinel = sentinel
        self.dealer_count = dealer_count

    def run(self):
        for i in range(self.cars_to_produce):

            # Create a new car object.
            new_car = Car()

            # Acquire the semaphore.
            self.sem_full_lot.acquire()

            # Acquire the lock of the queue.
            self.car_lock.acquire()

            # Put the new car in the queue.
            self.car_queue.put(new_car)

            # Release the lock and semaphore and signal to the dealer that there are cars in the queue to be sold.
            self.car_lock.release()
            self.sem_empty_lot.release()

        # Wait until all other manufacturers are finished.
        self.barrier.wait()

        # If this manufacturer is the sentinel, then signal to each dealer that no more cars are being made.
        if self.sentinel:
            for _ in range(self.dealer_count):
                # Signal to the dealer that there are no more cars being made by putting a none object in the queue.
                self.sem_full_lot.acquire()
                self.car_lock.acquire()
                self.car_queue.put(None)
                self.car_lock.release()
                self.sem_empty_lot.release()


class Dealership(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, full_lot: threading.Semaphore, empty_lot: threading.Semaphore, car_queue, car_lock, barrier):
        # Call the superclass.
        threading.Thread.__init__(self)

        # Esatblish the semaphores, queue, lock, barrier, stats, and queue stats.
        self.sem_full_lot = full_lot
        self.sem_empty_lot = empty_lot
        self.car_queue = car_queue
        self.car_lock = car_lock
        self.stats = 0
        self.barrier = barrier
        self.queue_stats = [0] * MAX_QUEUE_SIZE

    def run(self):
        while True:
            # Acquire semaphore for the queue.
            self.sem_empty_lot.acquire()

            # Acquire lock for the queue.
            self.car_lock.acquire()

            # Get the size of the queue.
            queue_size = len(self.car_queue.items)

            # Get the next car from the queue.
            current_car = self.car_queue.get()

            # Release the lock from the queue.
            self.car_lock.release()

            # Release the semaphore of the queue so the manufacturer can start making cars again.
            self.sem_full_lot.release()

            # If the car is none then end the loop, else print the car that was sold and update stats.
            if current_car == None:
                break
            else:
                # Increment the statistic for the number of cars sold for the stats list, and the size of the queue in the queue_stats list.
                self.stats += 1
                self.queue_stats[queue_size-1] += 1

                # print(f"SOLD {current_car.make} {current_car.model}, {current_car.year}")

            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(manufacturer_count, dealer_count):
    """ This function will do a production run with the number of
        manufacturers and dealerships passed in as arguments.
    """

    # Start a timer
    begin_time = time.perf_counter()

    # Semaphores for controlling access to the queue.
    full_lot = threading.Semaphore(MAX_QUEUE_SIZE)
    empty_lot = threading.Semaphore(0)

    # Creating the car queue object.
    car_queue = QueueTwoFiftyOne()

    # Creating a lock for the queue.
    car_lock = threading.Lock()

    # Creating barriers for manufacturer and dealer threads.
    m_barrier = threading.Barrier(manufacturer_count)
    d_barrier = threading.Barrier(dealer_count)

    # Creating lists for collecting stats for manufacturers and dealers.
    dealer_stats = list([0] * dealer_count)
    manufacturer_stats = list([0] * manufacturer_count)

    # List of manufacturers (objects).
    manufacturers = []

    # Creating each manufacturer.
    for i in range(0, manufacturer_count):
        # The first manufacturer will be the sentinel--it is responsible for waking all of the dealers once all roduction has finished.
        if i == 0:
            new_manufacturer = Manufacturer(
                full_lot, empty_lot, car_queue, car_lock, m_barrier, True, dealer_count)
        else:
            # Otherwise just create a regular manufacturer.
            new_manufacturer = Manufacturer(
                full_lot, empty_lot, car_queue, car_lock, m_barrier, False, dealer_count)

        # Add the new manufacturer to the list.
        manufacturers.append(new_manufacturer)

    # List of dealers (objects).
    dealers = []

    # Creating each dealer.
    for i in range(dealer_count):
        new_dealer = Dealership(full_lot, empty_lot,
                                car_queue, car_lock, d_barrier)
        # Add the new dealer to the list.
        dealers.append(new_dealer)

    # Starting each manufacturer thread.
    for m in manufacturers:
        m.start()

    # Starting each dealer thread.
    for d in dealers:
        d.start()

    # Joining all manufacturers and waiting for them to finish.
    for m in manufacturers:
        m.join()

    # Joining all dealers and waiting for the to finish.
    for d in dealers:
        d.join()

    run_time = time.perf_counter() - begin_time

    # Getting the cars made by each manufacturer for the manufacturer stats list.
    for i in range(0, len(manufacturers)):
        manufacturer_stats[i] = manufacturers[i].cars_to_produce

    # Getting the cars sold by each dealer for the dealer stats list.
    for i in range(0, len(dealers)):
        dealer_stats[i] = dealers[i].stats

    # Creating a list for the stats of the queue size during the production run.
    queue_stats = [0] * MAX_QUEUE_SIZE

    # Summing the queue stats for each dealer during production into the main queue_stats list.
    for dealer in dealers:
        for i in range(0, MAX_QUEUE_SIZE):
            queue_stats[i] += dealer.queue_stats[i]

    # Plot car count vs queue size.
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')

    # This function must return the following - only change the variable names, if necessary.
    # manufacturer_stats: is a list of the number of cars produced by each manufacturer,
    #                collect this information after the manufacturers are finished.
    return (run_time, car_queue.get_max_size(), dealer_stats, manufacturer_stats)


def main():
    """ Main function """

    # Use 1, 1 to get your code working like the previous assignment, then
    # try adding in different run amounts. You should be able to run the
    # full 7 run amounts.
    # runs = [(1, 1)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        # The number of cars produces needs to match the cars sold (this should pass)
        assert sum(dealer_stats) == sum(manufacturer_stats)

    # End of program.
    print("\nALL RUNS COMPLETED.\n")


if __name__ == '__main__':
    main()


# Assignment completed by Mark Vagil.
