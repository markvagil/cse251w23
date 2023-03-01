import multiprocessing as mp 

def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    return total

if __name__ == "__main__":
    pool = mp.Pool(4)
    results = pool.map(sum_all_values, range(100000, 100000 + 100))
    #pool.close()
    #pool.join()
    print(results)