"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team02.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Playing Card API calls

Instructions:

- Review instructions in Canvas.

"""

from datetime import datetime, timedelta
import threading
import requests
import json
import webbrowser
import climage


class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52

    def reshuffle(self):
        shuffle_thread = Request_thread(
            f'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        shuffle_thread.start()
        shuffle_thread.join()

    def draw_card(self):
        draw_thread = Request_thread(
            f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1')
        draw_thread.start()
        draw_thread.join()

        if draw_thread.response != {}:
            self.remaining = draw_thread.response['remaining']
            output = str(draw_thread.response['remaining']) + ' cards remaining, ' + 'card code: ' + draw_thread.response['cards'][0]['code'] + ', ' + \
                draw_thread.response['cards'][0]['value'] + \
                ' OF ' + draw_thread.response['cards'][0]['suit']
            # webbrowser.open(draw_thread.response['cards'][0]['image'])
            # print(climage.convert(webbrowser.open(draw_thread.response['cards'][0]['image'])))
            return output
        else:
            return 'error'

    def draw_all_cards(self, deck_size):
        draw_thread = Request_thread(
            f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count={deck_size}')
        draw_thread.start()
        draw_thread.join()

        if draw_thread.response != {}:
            self.remaining = draw_thread.response['remaining']
            all_cards = []

            for card in draw_thread.response['cards']:
                all_cards.append(card['value'] + ' OF ' + card['suit'])

            # output = card['value'] + ' OF ' + card['suit']
            # webbrowser.open(draw_thread.response['cards'][0]['image'])
            # print(climage.convert(webbrowser.open(draw_thread.response['cards'][0]['image'])))
            return all_cards
        else:
            return 'error'

    def cards_remaining(self):
        return self.remaining

    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'pzv7xc9ev8t9'

    # Test Code >>>>>
    deck = Deck(deck_id)
    for i in range(52):
        card = deck.draw_endless()
        print(card, flush=True)
    print()
    deck2 = Deck(deck_id)
    cards = deck2.draw_all_cards(52)
    for card in cards:
        print(card)
    # <<<<<<<<<<<<<<<<<<


"""
Stretch Challenge
1. Talk with your team if a Card class needs to be created for your game. What are the pros and cons?
2. Question: Would the class Deck be faster if you retrieved all of the cards for the deck when you reshuffle instead of making an API call for draw every card? 
   If you have the time, implement this feature.
3. Question: Why do you think that it's important to have the Request_thread class? Why not just make the API calls in Deck directly?"""
