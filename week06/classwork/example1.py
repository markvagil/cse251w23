import multiprocessing

count = 0

class MyProcess(multiprocessing.Process):
    
    def __init__(self, index):
        multiprocessing.Process.__init__(self)
        self.index = index
        
    def run(self):
        global count
        count += 1
        print(f'{self.index=}: {self.pid=}, {count=}')

def func(argument):
    print(f'{argument=}')


def main():
    #print(f'2: __name__={__name__}')

    processes = []
    # for i in range(5):
    #     p = multiprocessing.Process(target=func, args=(i,))
    #     processes.append(p)
    
    for i in range(5):
        p = MyProcess(i)
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()


#print(f'1: __name__={__name__}')
#print(f'{multiprocessing.current_process()}')

if __name__ == '__main__':
    main()

#if __name__ == '__mp_main__':
   # print(f'{multiprocessing.current_process()}: HERE')