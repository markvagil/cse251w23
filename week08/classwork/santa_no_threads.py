import string
import random
import time

class FlightPath:
    
    def __init__(self, houses):
        self.houses = houses
        self.my_house = 'Q'

    def atEnd(self, house):
        return house == self.my_house
    
    def get_start_house(self):
        return self.houses[0]
    
    def move(self):
        if(len(self.houses) > 0):
            moveTo = self.houses.pop(random.randrange(len(self.houses)))
            time.sleep(0.1)
            return moveTo
        return None

def deliver_presents_recursively(flightPath: FlightPath, house, path):
    
    if flightPath.atEnd(house):
        print('We found my house')
        return
    
    path.append(house)
    
    nextHouse = flightPath.move()
    print(f'Going to visit house "{nextHouse}"')
    
    deliver_presents_recursively(flightPath, nextHouse, path)

if __name__ == '__main__':
    houses = list(string.ascii_lowercase + string.ascii_uppercase)
    #houses = ['A', 'B', 'C', 'D', 'Q', 'E', 'F']
    print(f'{houses}')
    
    path = []
    
    flightPath = FlightPath(houses)
    house = flightPath.get_start_house()
    deliver_presents_recursively(flightPath, house, path)
    
    print(f'The path is {path}')
    
    