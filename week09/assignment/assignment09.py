'''
Requirements
1. Create a multiprocessing program that reads in files with defined tasks to perform.
2. The program should use a process pool per task type and use apply_async calls with callback functions.
3. The callback functions will store the results in global lists based on the task to perform.
4. Once all 4034 tasks are done, the code should print out each list and a breakdown of 
   the number of each task performed.
   
Questions:
1. How many processes did you specify for each pool:
   >Finding primes: 2
   >Finding words in a file: 1
   >Changing text to uppercase: 2
   >Finding the sum of numbers: 1
   >Web request to get names of Star Wars people: 34
   
   How do you determine these numbers: 
   > For the CPU bound problems, through lots of trial and error I eventually found that since the primes and
   > the uppercase tasks have separate function calls, it seems like they benefit from having a pool size of 2,
   > and the word finder and sum tasks actually slowed down when the pool size increased. It feels strange but
   > the runtimes don't lie. Having large pool sizes only slowed down run times.
   > For the IO bound problem it is useful to use as many processes as their are API calls which is 34, 
   > and at that pool size I get the best performance.
   
2. Specify whether each of the tasks is IO Bound or CPU Bound?
   >Finding primes: CPU
   >Finding words in a file: CPU
   >Changing text to uppercase: CPU
   >Finding the sum of numbers: CPU
   >Web request to get names of Star Wars people: IO
   
3. What was your overall time, with:
   >one process in each of your five pools: 34.87 seconds
   >with the number of processes you show in question one: 4.3 seconds
'''

import glob
import json
import math
import multiprocessing as mp
import os
import time
from datetime import datetime, timedelta

import numpy as np
import requests

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


# The is_prime function checks if an integer is prime or not.
def is_prime(n: int):
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


# Prime task function, takes in an integer.
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """

    # Calls is_prime to check the primality of the value, and returns a string.
    if is_prime(value):
        return (f'{value} is prime')
    else:
        return (f'{value} is not prime')


# Prime task callback function.
def callback_prime(result):
    # Appending result to the global list.
    global result_primes
    result_primes.append(result)


# Word task function, takes in a word.
def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    # Opens the data.txt file and checks if the word is in the file and returns a string.
    with open('data.txt', 'r') as file:
        content = file.read()
        if word in content:
            return (f'{word} Found')
        else:
            return (f'{word} not found *****')


# Word task callback function.
def callback_words(result):
    # Appending result to the global list.
    global result_words
    result_words.append(result)


# Upper task function, takes in a string.
def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    # Return the formatted string with the uppercase version of the text.
    return (f'{text} ==> uppercase version of {text.upper()}')


# Upper task callback function.
def callback_upper(result):
    # Appending result to the global list.
    global result_upper
    result_upper.append(result)


# Sum task function, takes in a start and end value.
def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    # Sum of the start and end values.
    sum = start_value + end_value
    # Return the formatted string.
    return (f'sum of {start_value:,} to {end_value:,} = {sum:,}')


# Sum task callback function.
def callback_sum(result):
    # Appending result to the global list.
    global result_sums
    result_sums.append(result)


# Name task function, takes in a URL.
def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    # Getting the web request from the star wars server.
    response = requests.get(url)

    # Status request validation
    if response.status_code == 200:
        # Getting the JSON data.
        data = response.json()
        # Return the URL and the character's name.
        return f'{url} has name {data["name"]}'
    else:
        # If there is a bad URL or server response.
        return (f'{url} has an error receiving the information')


# Name task callback function.
def callback_name(result):
    # Appending result to the global list.
    global result_names
    result_names.append(result)


# Load JSON file function to get the data from the task file.
def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    begin_time = time.time()

    # Creating each process pool.
    # I have 20 logical processors on my computer just as a note, my CPU is a intel i9-12900H

    prime_pool = mp.Pool(2)  # Runs fastest with 2 CPUs
    word_pool = mp.Pool(1)  # Runs fastest with 1 CPU
    upper_pool = mp.Pool(2)  # Runs fastest with 2 CPUs
    sum_pool = mp.Pool(1)  # Runs fastest with 1 CPU

    # Since the name task is I/O bound, I increase the pool size to the number of names (API calls).
    name_pool = mp.Pool(34)  # Runs best at 34 CPUs

    # Storing each pool in a list.
    pools_list = [prime_pool, word_pool, upper_pool, sum_pool, name_pool]

    # Count variable, and task files folder variable.
    count = 0
    task_files = glob.glob("tasks/*.task")

    # Iterate through each file in the tasks folder.
    for filename in task_files:
        # Loading the json data from the task file.
        task = load_json_file(filename)
        # Updating the count of tasks.
        count += 1
        # Saving the task type as a variable.
        task_type = task['task']

        # Checking which task type we have and then running it.
        if task_type == TYPE_PRIME:
            # Prime pool task.
            prime_pool.apply_async(task_prime, args=(
                task['value'],), callback=callback_prime)
        elif task_type == TYPE_WORD:
            # Word pool task.
            word_pool.apply_async(task_word, args=(
                task['word'],), callback=callback_words)
        elif task_type == TYPE_UPPER:
            # Uppercase pool task.
            upper_pool.apply_async(task_upper, args=(
                task['text'],), callback=callback_upper)
        elif task_type == TYPE_SUM:
            # Sum pool task.
            sum_pool.apply_async(task_sum, args=(
                task['start'], task['end']), callback=callback_sum)
        elif task_type == TYPE_NAME:
            # Names pool task.
            name_pool.apply_async(task_name, args=(
                task['url'],), callback=callback_name)
        else:
            print(f'Error: unknown task type {task_type}')

    # Starting each pool and blocking until they are done before printing anything.
    for pool in pools_list:
        pool.close()
        pool.join()

    # Printing all results.

    def print_list(lst):
        for item in lst:
            print(item)
        print(' ')

    print('-' * 80)
    print(f'Primes: {len(result_primes)}')
    print_list(result_primes)

    print('-' * 80)
    print(f'Words: {len(result_words)}')
    print_list(result_words)

    print('-' * 80)
    print(f'Uppercase: {len(result_upper)}')
    print_list(result_upper)

    print('-' * 80)
    print(f'Sums: {len(result_sums)}')
    print_list(result_sums)

    print('-' * 80)
    print(f'Names: {len(result_names)}')
    print_list(result_names)

    print(f'Number of Primes tasks: {len(result_primes)}')
    print(f'Number of Words tasks: {len(result_words)}')
    print(f'Number of Uppercase tasks: {len(result_upper)}')
    print(f'Number of Sums tasks: {len(result_sums)}')
    print(f'Number of Names tasks: {len(result_names)}')
    print(f'Finished processes {count} tasks = {time.time() - begin_time}')


if __name__ == '__main__':
    main()
