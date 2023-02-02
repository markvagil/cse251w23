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


# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


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

    # Function which creates all threads for each URL from a category.
    def get_all_from_list(key_list):
        thread_list = []  # Stores each thread object.

        # Instance for loop that iterates through each item in the list and creates the thread, and appends it to the list.
        for url in key_list:
            new_thread = threads(url)
            thread_list.append(new_thread)

        return thread_list

    # Creating the list of threads for each category, and starting them.
    characters = get_all_from_list(t2.data["characters"])
    [thread.start() for thread in characters]
    planets = get_all_from_list(t2.data["planets"])
    [thread.start() for thread in planets]
    starships = get_all_from_list(t2.data["starships"])
    [thread.start() for thread in starships]
    vehicles = get_all_from_list(t2.data["vehicles"])
    [thread.start() for thread in vehicles]
    species = get_all_from_list(t2.data["species"])
    [thread.start() for thread in species]

    # Joining all threads from all categories to finish them.
    [thread.join() for thread in characters]
    [thread.join() for thread in planets]
    [thread.join() for thread in starships]
    [thread.join() for thread in vehicles]
    [thread.join() for thread in species]

    # Creating a new list of JSON data from each thread object category.
    characters_data = [thread.data for thread in characters]
    planets_data = [thread.data for thread in planets]
    starships_data = [thread.data for thread in starships]
    vehicles_data = [thread.data for thread in vehicles]
    species_data = [thread.data for thread in species]

    # Call to the display function to print all of the details in the desired format.
    print_film_details(t2.data, characters_data, planets_data,
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


# Assignment completed by Mark Vagil.
