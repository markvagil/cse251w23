"""
Course: CSE 251
Lesson Week: 05
File: team05.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Team Activity

Instructions:

- See in Canvas

"""

import threading
import queue
import time
import requests
import json

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue


def retrieve_thread(queue):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue

        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and print it out
        pass


def file_reader(url_file, queue):  # TODO add arguments
    """ This thread reads the data file and places the values in the data_queue """

    """# Get the response from the API after making the URL request.
    response = requests.get(url)
    
    if response.status_code == 200:
        # If the call is successful then store the data from the response.
        return data_list.append(response.json())
    else:
        print('Error in requesting ID')
        return
    """
    f = open(f"team/{url_file}", "r")
    f.read()

    for line in f:
        line.strip()
        queue.put(line)
        print(line)

    queue.put(NO_MORE_VALUES)
    print("done")

    return queue

    # TODO Open the data file "urls.txt" and place items into a queue

    # TODO signal the retrieve threads one more time that there are "no more values"


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    thread_queue = queue.Queue(0)
    threads_list = []

    t1 = threading.Thread(target=file_reader, args=("urls.txt", thread_queue))
    t1.start()
    t1.join()
    print(t1)
    print(thread_queue.qsize())

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs

    # for i in range(RETRIEVE_THREADS):
    #     new_thread = threading.Thread(target=retrieve_thread, args=(t1))
    #     threads_list.append(new_thread)

    # for thread in threads_list:
    #     thread.start()

    # for thread in threads_list:
    #     thread.join()

    # TODO Get them going

    # TODO Wait for them to finish

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()
