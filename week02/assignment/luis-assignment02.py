'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between (end)10,000,000,000 and (start)10,000,110,003.
2. The program should be able to use a variable amount of threads.
3. Each thread should look over an approximately equal number of numbers.
   This means that you need to divise an algorithm that can divide up the
   110,003 numbers "fairly" based on a variable number of threads. 
   
Psuedocode: 
1. Create variable for the start number (10_000_000_000)
2. Create variable for range of numbers to examine (110_003)
3. Create variable for number of threads (start with 1 to get your program running, n - starting number/ n 
   then increase to 5, then 10).
4. Determine an algorithm to partition the 110,003 numbers based on 
    the number of threads. Each thread should have approx. the same amount
    of numbers to examine. For example, if the number of threads is
    5, then the first 4 threads will examine 22,003 numbers, and the
    last thread will examine 22,003 numbers. Determine the start and
    end values of each partition.

x = 0
list = []
for n 
t = threading.Thread(func = ...., args = (x,x + partition))
x+= partition 

5. Use these start and end values as arguments to a function.
6. Use a thread to call this function.
7. Create a function that loops from a start and end value, and checks
   if the value is prime using the isPrime function. Use the globals
   to keep track of the total numbers examined and the number of primes
   found. 

Questions:
1. Time to run using 1 thread = Total time = 48.85 sec
2. Time to run using 5 threads =
3. Time to run using 10 threads =
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   >
   >
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   >
'''

from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found
prime_count = 0

# Global count of the numbers examined
numbers_processed = 0

# global start number
start_number = 10000000000


# global end number

end_number = 10000110003


# global number of threads
NUMBER_THREADS = 5


def is_prime(n: int):
    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test

    Parameters
    ----------
    ``n`` : int
        Number to determine if prime

    Returns
    -------
    bool
        True if ``n`` is prime.
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


"""def partition(number:int):
    interval = 110000
    parts = interval / number
    return parts + 3 """


# this function will count the number of primes in an interval and validate them using the is_prime function
def count_prime(start, end):
    # I am calling the global variable to count the number of primes in the intervals
    global prime_count

    # call the global variable numbers proccess
    global numbers_processed

    # use a list comprenhension (I had to look it up as the TA recommended I use it)
    list_of_primes = [number for number in range(
        start, end, 1) if is_prime(number)]
    prime_count += len(list_of_primes)

    # It will add to the total numbers of numbes proccess
    numbers_processed += end - start

    return


if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()

    # TODO write code here

    range_of_numbers = end_number - start_number

    intervals = range_of_numbers // NUMBER_THREADS

    # this code snippet I ran when thread_number = 1

    def one_thread():
        first_number = start_number
        last_number = start_number + intervals

        # Creating my thread
        t1 = threading.Thread(target=count_prime,
                              args=(first_number, last_number,))

        t1.start()
        t1.join()

    def threads_five():

        # because the range is between 1000000000 and 100100003 the 3 makes it diffcult to evenly devided
        # so Ill just assing the remainder to the last thread
        add_to_last_thread = intervals + (range_of_numbers % NUMBER_THREADS)

        # first set for thatonly the thread 1 will run through and consecuently with the other threads
        first_number = start_number
        last_number = start_number + intervals

        first_number2 = last_number
        last_number2 = last_number + intervals

        first_number3 = last_number2
        last_number3 = last_number2 + intervals

        first_number4 = last_number3
        last_number4 = last_number3 + intervals

        first_number5 = last_number4
        last_number5 = last_number4 + add_to_last_thread

        # Creating the first thread
        t1 = threading.Thread(target=count_prime,
                              args=(first_number, last_number,))
        t2 = threading.Thread(target=count_prime, args=(
            first_number2, last_number2,))
        t3 = threading.Thread(target=count_prime, args=(
            first_number3, last_number3,))
        t4 = threading.Thread(target=count_prime, args=(
            first_number4, last_number4,))
        t5 = threading.Thread(target=count_prime, args=(
            first_number5, last_number5,))

        my_threads = [t1, t2, t3, t4, t5]
        [thread.start() for thread in my_threads]
        [thread.join() for thread in my_threads]

        return

    # one_thread()
    threads_five()

    # Use the below code to check and print your results
    """assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"
    """
    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')
