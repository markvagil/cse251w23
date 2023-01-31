import threading
import time
import random

def test_with_barrier(synchronizer: threading.Barrier):
    
    print(f'{threading.current_thread().name}: BEFORE SLEEP\n', end="")
    time.sleep(random.uniform(0.5, 2.5))
    print(f'{threading.current_thread().name}: AFTER SLEEP\n', end="")
     
    synchronizer.wait()
    now = time.time()
    
    print(f'{threading.current_thread().name}: The current time is {now}\n', end="")

if __name__ == '__main__':
    
    synchronizer = threading.Barrier(4)
    t1 = threading.Thread(target=test_with_barrier, args=(synchronizer,))
    t2 = threading.Thread(target=test_with_barrier, args=(synchronizer,))
    t3 = threading.Thread(target=test_with_barrier, args=(synchronizer,))
    t4 = threading.Thread(target=test_with_barrier, args=(synchronizer,))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    """ t1.join()
    t2.join()
    t3.join()
    t3.join() """