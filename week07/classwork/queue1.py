import multiprocessing
import queue
import time

def sender(q: multiprocessing.Queue, data):
    for i in range(10):
        q.put(i)
        data[i] = i
    q.put(None)

    time.sleep(3)
    print(f'data={data}')

def receiver(q: multiprocessing.Queue, data):
    while True:
        item = q.get()
        #print(f'{item=}')
        if item == None:
            break
    print(f'data={data}')
    data[0] = 100

def main():

    q = multiprocessing.Queue()
    
    data = multiprocessing.Manager().list([0] * 10)

    p1 = multiprocessing.Process(target=sender, args=(q, data))
    p2 = multiprocessing.Process(target=receiver, args=(q, data))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
    


if __name__ == "__main__":
    main()
