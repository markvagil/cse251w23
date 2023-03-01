import multiprocessing as mp
import time

def square_me(number):
    time.sleep(0.01)
    return number * number


if __name__ == "__main__":
    
    numbers = [i for i in range(101)]
    
    with mp.Pool(4) as p:
        p.map(func=square_me, args=numbers)