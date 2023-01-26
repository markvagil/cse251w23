import queue
import threading

MAX_QUEUE_SIZE = 20
max_size = 0

def getter(q: queue.Queue, semMax: threading.Semaphore, semEmpty: threading.Semaphore):
    global max_size
    
    while True:
        
        semEmpty.acquire()       
        if q.qsize() > max_size:
            max_size = q.qsize()
        
        pair = q.get()
        
        if pair == None:
            break
        
        number, power = pair
        
        semMax.release()
        
        
def putter(q: queue.Queue, semMax: threading.Semaphore, semEmpty: threading.Semaphore):
    with open('numbers.txt') as f:
        for line in f:
            
            semMax.acquire()
            parts = line.split(',')
            number = int(parts[0])
            power = int(parts[1])
            q.put((number, power))     
            semEmpty.release() 
    
    q.put(None)      
    semEmpty.release()


def main():
    q = queue.Queue()
    
    semMax = threading.Semaphore(20)
    semEmpty = threading.Semaphore(0)

    putter_thread = threading.Thread(target=putter, args=(q, semMax, semEmpty))
    getter_thread = threading.Thread(target=getter, args=(q, semMax, semEmpty))
    
    putter_thread.start()
    getter_thread.start()
    
    putter_thread.join()
    getter_thread.join()
    
    print(f'MAX QUEUE SIZE WAS = {max_size}')

if __name__ == '__main__':
    main()