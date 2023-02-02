'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between 10,000,000,000 and 10,000,110,003.
2. The program should be able to use a variable amount of threads.
3. Each thread should look over an approximately equal number of numbers.
   This means that you need to devise an algorithm that can divide up the
   110,003 numbers "fairly" based on a variable number of threads. 
   
Psuedocode: 
1. Create variable for the start number (10_000_000_000)
2. Create variable for range of numbers to examine (110_003)
3. Create variable for number of threads (start with 1 to get your program running,
   then increase to 5, then 10).
4. Determine an algorithm to partition the 110,003 numbers based on 
    the number of threads. Each thread should have approx. the same amount
    of numbers to examine. For example, if the number of threads is
    5, then the first 4 threads will examine 22,000 numbers, and the
    last thread will examine 22,003 numbers. Determine the start and
    end values of each partition.
5. Use these start and end values as arguments to a function.
6. Use a thread to call this function.
7. Create a function that loops from a start and end value, and checks
   if the value is prime using the isPrime function. Use the globals
   to keep track of the total numbers examined and the number of primes
   found. 

Questions:
1. Time to run using 1 thread = 7.85 seconds
2. Time to run using 5 threads = 7.93 seconds
3. Time to run using 10 threads = 7.75 seconds
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   > Because threading has no impact on CPU bound problems, there is no performance benefit to using threads for this problem.
   > The GIL only allows one thread to run at a time so only I/O problems benefit from threading. There is no difference between using 1 thread or 100 threads.
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   > This is a CPU bound problem, there is no I/O to worry about in this program.
'''

from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found.
prime_count = 0

# Global count of the numbers examined.
numbers_processed = 0

# Global variables for the start of the range and the end of the range.
start_range = 10_000_000_000
end_range = 10_000_110_003

# Global constant for number of threads.
NUMBER_THREADS = 17


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


def find_primes(start_num, end_num):
    # This function will be run by each thread.
    # Takes a starting number and ending number parameter for the interval of integers to check for primality.

    # Creates a list of prime numbers from the provided interval using a list comprehension.
    primes_list = [num for num in range(
        start_num, end_num, 1) if is_prime(num)]

    # Adding the length of the list (number of primes in the interval) to the global prime count.
    global prime_count
    prime_count += len(primes_list)

    # Adding the interval range of integers to the total number of integers processed in the program.
    global numbers_processed
    numbers_processed += end_num - start_num

    return


if __name__ == '__main__':
    # Start a timer.
    begin_time = time.perf_counter()

    # Find the initial thread interval size.
    prime_range = end_range - start_range
    thread_interval = prime_range // NUMBER_THREADS

    # Find any remainder (partial interval) so that it can be added to the last thread interval.
    last_interval_remainder = (prime_range % NUMBER_THREADS)

    # List that holds each thread object.
    my_threads = []
    # Start of the total prime range, variable is used in the loop algorithm.
    start = start_range
    # End of the first interval for the prime range, which is just the start plus the interval size.
    end = start + thread_interval

    # For loop that will create each thread.
    for i in range(1, NUMBER_THREADS + 1, 1):
        # If we are on the last thread, then add the remainder of the range to the total interval range for the thread.
        if i == NUMBER_THREADS:
            new_thread = threading.Thread(target=find_primes, args=(
                start, end + last_interval_remainder,))
        else:
            # Otherwise, just create the thread with the regular interval size.
            new_thread = threading.Thread(
                target=find_primes, args=(start, end,))

        # Setting the new start to the last end.
        start = end
        # Setting the new end to the current end plus the next range of primes to be found.
        end = end + thread_interval

        # Starting the thread and adding it to the list of all threads.
        new_thread.start()
        my_threads.append(new_thread)

    # Joining all of our threads to finish their processes.
    [thread.join() for thread in my_threads]

    # Use the below code to check and print your results
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')


# Assignment completed by Mark Vagil.
