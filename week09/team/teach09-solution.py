"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau
"""

import multiprocessing as mp
import threading

import requests

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

chars = []
planets = []
starships = []
vehicles = []
species = []

# -------------------------------------------------------------------------------


class Request_thread(threading.Thread):

    def __init__(self, url, data, call_count):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.call_count = call_count

    def run(self):
        #print(f'request url={self.url}')
        response = requests.get(self.url)
        self.call_count.value += 1
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.data.append(response.json())


# -------------------------------------------------------------------------------
def print_film_details(film, chars, planets, starships, vehicles, species):

    def display_names(title, names):
        print(f'{title}: {len(names)}')
        names.sort()
        name_str = ''
        for str in names:
            name_str += str + ', '
        print(name_str)

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


def cb_chars(result):
    global chars
    chars.append(result['name'])


def cb_species(result):
    global species
    species.append(result['name'])


def cb_vehicles(result):
    global vehicles
    vehicles.append(result['name'])


def cb_starships(result):
    global starships
    starships.append(result['name'])


def cb_planets(result):
    global planets
    planets.append(result['name'])


def get_url(url, call_count):
    #print(f'{mp.current_process()=}, get_url, url={url}, call_count={call_count.value}')
    response = requests.get(url)
    call_count.value += 1
    return response.json()

# -------------------------------------------------------------------------------


def main():
    call_count = mp.Manager().Value('i', 0)

    pool = mp.Pool(mp.cpu_count())

    # Retrieve Top API urls
    urls = []
    t = Request_thread(TOP_API_URL, urls, call_count)
    t.start()
    t.join()

    # Retrieve film 6 details
    top_urls = urls[0]
    film_url = top_urls['films']

    film6 = []
    t = Request_thread(f'{film_url}6', film6, call_count)
    t.start()
    t.join()
    film_data = film6[0]

    for url in film_data['characters']:
        pool.apply_async(get_url, args=(url, call_count, ), callback=cb_chars)

    for url in film_data['planets']:
        pool.apply_async(get_url, args=(url, call_count, ), callback=cb_planets)

    for url in film_data['starships']:
        pool.apply_async(get_url, args=(url, call_count, ), callback=cb_starships)

    for url in film_data['vehicles']:
        pool.apply_async(get_url, args=(url, call_count, ), callback=cb_vehicles)

    for url in film_data['species']:
        pool.apply_async(get_url, args=(url, call_count, ), callback=cb_species)

    pool.close()
    pool.join()

    # Display results
    print_film_details(film_data, chars, planets,
                       starships, vehicles, species)

    #print('')
    #log.stop_timer('Total Time To complete')
    #print(f'There were {call_count.value} calls to swapi server')


if __name__ == "__main__":
    main()
