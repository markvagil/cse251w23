

import multiprocessing as mp
import threading
import time


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def read_thread(file_name, data_queue: mp.Queue, cpu_count):
    """read file and populate queue"""
    with open(file_name) as f:
        for line in f:
            data_queue.put(line.strip())
    print('Done reading all values from file')
    for _ in range(cpu_count):
        data_queue.put(None)


def prime_process(data_queue: mp.Queue, primes):
    print('prime_process starting')
    while True:
        number = data_queue.get()

        # check if reader is done putting items on the queue
        if (number == None):
            break

        #print(f'checking if {number} is prime')
        if (is_prime(int(number))):
            #print(f'YES, {number} is prime')
            #primes.append(number)
            primes.value += 1


def main():
    """ Main function """

    filename = 'data.txt'

    # Start a timer
    begin_time = time.perf_counter()

    # Create shared data structures
    data_queue = mp.Queue()
    #primes = mp.Manager().list()
    primes = mp.Value('i', 0)

    cpu_count = mp.cpu_count() + 4

    # create reading thread
    reading_thread = threading.Thread(
        target=read_thread, args=(filename, data_queue, cpu_count))

    # create prime processes
    processes = []
    for _ in range(cpu_count):
        processes.append(mp.Process(
            target=prime_process, args=(data_queue, primes)))

    # Start them all
    reading_thread.start()
    for p in processes:
        p.start()

    # wait for them to complete
    reading_thread.join()
    for p in processes:
        p.join()

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    
    # Assert the correct amount of primes were found.
    assert primes.value == 321, "You should find exactly 321 prime numbers"


if __name__ == '__main__':
    main()
