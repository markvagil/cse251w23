'''
Requirements
1. Write a multithreaded program that calls a local web server. The web server is 
   provided to you. It will return data about the Star Wars movies.
2. You will make 94 calls to the web server, using 94 threads to get the data.
3. Using a new thread each time, obtain a list of the characters, planets, 
   starships, vehicles, and species of the sixth Star Wars movie.
3. Use the provided print_film_details function to print out the data 
   (should look exactly like the "sample_output.txt file).
   
Questions:
1. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
    > This is an IO bound problem.
2. Review dictionaries (see https://isaaccomputerscience.org/concepts/dsa_datastruct_dictionary). How could a dictionary be used on this assignment to improve performance?
    > A dictionary improves performance because accessing items is always O(1) performance since python uses a hash map whereas a list has O(n) performance because python uses linked lists which is worse performance than a dictionary.
'''


from datetime import datetime, timedelta
import time
import requests
import json
import threading
import multiprocessing as mp


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'
CPU_COUNT = mp.cpu_count()

# Global Variables
call_count = 0

# Lists of data we need
characters_data = []
planets_data = []
starships_data = []
vehicles_data = []
species_data = []

# Thread class which creates thread objects that make API requests to the server.


class threads(threading.Thread):
    # Class constructor.
    def __init__(self, url):
        super().__init__()
        self.response = url  # URL.
        self.data = ""  # JSON Data.

    def run(self):
        # Update the call count by 1.
        global call_count
        call_count += 1

        # Get the response from the API after making the URL request.
        self.response = requests.get(self.response)

        if self.response.status_code == 200:
            # If the call is successful then store the data from the response.
            self.data = self.response.json()
        else:
            print('Error in requesting ID')

# Function provided for printing the data in the desired format.


def get_details(url):
    response = requests.get(url)

    if response.status_code == 200:
        # If the call is successful then store the data from the response.
        return response.json()
    else:
        print('Error in requesting ID')


def characters_cb(character):
    global characters_data
    characters_data.append(character)
    global call_count
    call_count += 1


def planets_cb(planet):
    global planets_data
    planets_data.append(planet)
    global call_count
    call_count += 1


def starships_cb(starship):
    global starships_data
    starships_data.append(starship)
    global call_count
    call_count += 1


def vehicles_cb(vehicle):
    global vehicles_data
    vehicles_data.append(vehicle)
    global call_count
    call_count += 1


def species_cb(species):
    global species_data
    species_data.append(species)
    global call_count
    call_count += 1


def print_film_details(film, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''

    def display_names(title, name_list):
        print('')
        print(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))

    print('-' * 40)
    print(f'Title   : {film["title"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)


def main():
    # Start a timer
    begin_time = time.perf_counter()

    # TODO Using your thread class, retrieve TOP_API_URL to get
    # the list of the urls for each of the categories in the form
    # of a dictionary (open your browser and go to http://127.0.0.1:8790
    # to see the json/dictionary). Note that these categories are for
    # all the Star Wars movies.

    # TODO Retrieve details on film 6 by putting a '6' at the end of the films URL.
    # For example, http://127.0.0.1:8790/films/6 gives you all the details of
    # the sixth movie.

    # Iterate over each of the keys in the sixth film details and get the data
    # for each of the categories (might want to create function to do this)

    # TODO Call the display function

    print('Starting to retrieve data from the server')

    # First thread call to the server, getting inital data on lower URLs.
    t1 = threads(TOP_API_URL)
    t1.start()
    t1.join()

    film_number = "6"  # We want info from the 6th film.

    # Our second thread which gets all of the URL data for the 6th film.
    t2 = threads(t1.data["films"] + film_number)
    t2.start()
    t2.join()

    film = t2.data
    pool = mp.Pool(CPU_COUNT)

    for url in film["characters"]:
        pool.apply_async(get_details, args=(url,), callback=characters_cb)

    for url in film["planets"]:
        pool.apply_async(get_details, args=(url,), callback=planets_cb)

    for url in film["starships"]:
        pool.apply_async(get_details, args=(url,), callback=starships_cb)

    for url in film["vehicles"]:
        pool.apply_async(get_details, args=(url,), callback=vehicles_cb)

    for url in film["species"]:
        pool.apply_async(get_details, args=(url,), callback=species_cb)

    pool.close()
    pool.join()

    # Call to the display function to print all of the details in the desired format.
    print_film_details(film, characters_data, planets_data,
                       starships_data, vehicles_data, species_data)

    print(f'\nThere were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')

    # If you do have a slow computer, then put a comment in your code about why you are changing
    # the total_time limit. Note: 90+ seconds means that you are not doing multithreading
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."

    assert call_count == 94, "It should take exactly 94 threads to get all the data"


if __name__ == "__main__":
    main()
