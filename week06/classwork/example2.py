import multiprocessing
import os
import time


def square(n):
    n **= 2
    time.sleep(0.01)
    return n


if __name__ == '__main__':
    inputs = list(range(100))
    
    count = multiprocessing.cpu_count()
    
    print(f'{count=}')
    
    # pool = multiprocessing.Pool(count)
    # outputs = pool.map(square, inputs)
    # pool.close()
    # pool.join()
    outputs = []
    with multiprocessing.Pool(count) as p:
        outputs = p.map(square, inputs)
    
    print(f'{outputs=}')
    print(f'{inputs=}')
    