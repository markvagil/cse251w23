'''
Requirements:
1. Write a function that takes a number and computes the sum of all numbers between
   one and that number (exclusive). This will be the target of your thread.
2. Create a thread to run this function.
3. Assert that your sums are correct for the given number.

Psuedocode:
1. Create either a global SUM or create a list object in main.
2a. If using a global, then inside of your function, set the global equal to the sum.
2b. If using a list object, set the appropriate index position equal to the sum.
3. In main, create a thread to call the sum function using 10.
4. Using assert, check the expected result (see main)
5. Repeat steps 3 and 4, but use 13.
6. Repeat steps 3 and 4, but use 17.

Things to consider:
a. If using a global, what is the correct syntax for creating a thread with one argument?
   (see https://stackoverflow.com/questions/3221655/python-threading-string-arguments)
b. How do you start a thread? (see this week's reading)
c. How will you wait until the thread is done? (see this week's reading)
d. Do threads (including the main thread) share global variables? (see https://superfastpython.com/thread-share-variables/)
e. If you use a global, how will you ensure that one thread doesn't change the value of
   your global while another thread is using it too? (We haven't learned about locks yet, so you
   won't be able to run your threads simultaneously)
f. How do you modify the value of a global variable (see https://stackoverflow.com/questions/10588317/python-function-global-variables)
g. If using a list object, how to you instantiate it with the correct number of indexes? (see https://stackoverflow.com/questions/8528178/list-of-zeros-in-python)
'''
import threading

# Global sum variable.
sum = 0


# Function for calculating the summation up to an inputted number that is used in our threads.
def threaded_sum(num=int):
    global sum
    for number in range(1, num, 1):
        sum += number



def summing(index, number, results):
    sum = 0
    for i in range(number):
        sum += i
        print(f'{index=}, {i=}, {sum=}\n', end="")
    results[index] = sum


def main():
<<<<<<< Updated upstream

    # If not using a global, use this list to store your results
    results = [0] * 3

    threads = []
    threads.append(threading.Thread(target=summing, args=(0, 10, results)))
    threads.append(threading.Thread(target=summing, args=(1, 13, results)))
    threads.append(threading.Thread(target=summing, args=(2, 17, results)))
    
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()

    # If using a global, place these asserts after the call to your summing function
    # to check that your code is working correctly
    #assert SUM == 45, f'The sum should equal 45 but instead was {SUM}'
    #assert SUM == 78, f'The sum should equal 78 but instead was {SUM}'
    #assert SUM == 136, f'The sum should equal 136 but instead was {SUM}'
    # If using a list object, place these asserts after the call to your summing function
    # to check that your code is working correctly
    assert results[0] == 45, f'The sum should equal 45 but instead was {results[0]}'
    assert results[1] == 78, f'The sum should equal 78 but instead was {results[1]}'
    assert results[2] == 136, f'The sum should equal 136 but instead was {results[2]}'

=======
>>>>>>> Stashed changes

    # Creating our threads directly through the thread class.
    t1 = threading.Thread(target=threaded_sum, args=(10,))
    t2 = threading.Thread(target=threaded_sum, args=(13,))
    t3 = threading.Thread(target=threaded_sum, args=(17,))

    # For each thread, the sum is reset to 0, the thread is started and joined (finished),
    # and we assert the value is correct.
    global sum
    sum = 0
    t1.start()
    t1.join()
    # Summation up to 10, using the first thread.
    assert sum == 45, f'The sum should equal 45 but instead was {sum}'

    sum = 0
    t2.start()
    t2.join()
    # Summation up to 13, using the second thread.
    assert sum == 78, f'The sum should equal 78 but instead was {sum}'

    sum = 0
    t3.start()
    t3.join()
    # Summation up to 17, using the third thread.
    assert sum == 136, f'The sum should equal 136 but instead was {sum}'


# Main function.
if __name__ == '__main__':
    main()
    print("DONE")

# Assignment completed by Mark Vagil.
