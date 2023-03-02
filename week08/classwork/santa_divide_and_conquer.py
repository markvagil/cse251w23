import string
import threading

def deliver_presents(houses):
    
    #print(f'{houses}')
    
    # base case
    if (len(houses) == 1):
        #print(f'Deliver present to house "{houses[0]}"')
        return
    mid = len(houses) // 2 #integer division
    L = houses[:mid]
    R = houses[mid:]
    
    print(f'{L=}')
    t1 = threading.Thread(target=deliver_presents, args=(L,))
    t1.start()
    t1.join()
    print(f'{R=}')
    deliver_presents(R)

if __name__ == '__main__':
    #houses = list(string.ascii_lowercase + string.ascii_uppercase)
    houses = ['0', '1', '2', '3', '4', '5']
    deliver_presents(houses)
    