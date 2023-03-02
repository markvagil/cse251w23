import multiprocessing as mp
import time 

output = []

def callback_func(result):
    global ouput
    print(f'callback_func: {result}')
    output.append(result)

def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    #print(f'{total=}')
    return total
    
if __name__ == "__main__":
    pool = mp.Pool(4)
    results = [pool.apply_async(sum_all_values, args=(x,), callback=callback_func) for x in range(10000, 10000 + 10)]
    pool.close()
    
    # do something else

    # collect all of the results into a list
    #output = [p.get() for p in results]
    pool.join()
    print(f'the output is {output}')