import threading
import queue

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def thread_function(thread_id, q: queue.Queue, barrier: threading.Barrier, start_value, end_value):
    for i in range(start_value, end_value):
        if is_prime(i):
            q.put(i)

    #barrier.wait()  # Wait for all threads to complete the task before printing
    q.put(None) # signal to print function to end

def print_function(q: queue.Queue):
    count = 0
    while True:
        number = q.get()
        if number == None:
            break
        print(f'{number} is prime')
        count += 1
    print(
        f'Total primes found = {count}\n', end="")

def main():

    # 4 is the number of threads to wait
    barrier = threading.Barrier(4)

    q = queue.Queue()

    # Create 4 threads, pass a "thread_id" and a barrier to each thread
    threads = []
    threads.append(threading.Thread(target=thread_function,
                                    args=(1, q, barrier, 1, 3)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(2, q, barrier, 3, 5)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(3, q, barrier, 5, 7)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(4, q, barrier, 7, 9)))
    threads.append(threading.Thread(target=print_function, args=(q,)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
