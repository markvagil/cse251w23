import multiprocessing as mp
import random
import threading
import time

number_threads = 1

# -----------------------------------------------------------------------------
# Python program for implementation of MergeSort
# https://www.geeksforgeeks.org/merge-sort/


def combine_arrays(arr, L, R):
    i = j = k = 0

    # Copy data to temp arrays L[] and R[] by comparing
    # sorted values in one array to the other
    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # It is possible (probable?) that we exited the above
    # loop and there are still items left in the temporary
    # arrays. But, now we know that whatever numbers are left
    # in the temp arrays will be greater than what is left in
    # the main array, so we can just move them over.
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort(arr):

    # base case of the recursion - must have at least 2+ items
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        merge_sort(L)

        # Sorting the second half
        merge_sort(R)

        # combine the sorted L and R arrays back into our main array
        combine_arrays(arr, L, R)


def merge_sort_with_threads(arr):

    # base case of the recursion - must have at least 2+ items
    if len(arr) > 1:

        global number_threads
        number_threads += 1
        
        #print(f'{number_threads=}\n', end="")

        # Finding the mid of the array
        mid = len(arr) // 2
        #print(f'{mid}\n')

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        thread_l = threading.Thread(target=merge_sort_with_threads, args=(L, ))
        thread_r = threading.Thread(target=merge_sort_with_threads, args=(R, ))

        thread_l.start()
        thread_r.start()

        thread_l.join()
        thread_r.join()

        # combine the sorted L and R arrays back into our main array
        combine_arrays(arr, L, R)


def merge_sort_with_processes(arr, count):

    # base case of the recursion - must have at least 2+ items
    if len(arr) > 1:
        # Finding the mid of the array
        mid = len(arr) // 2

        # limit the number of processes to 10 to avoid running out
        # of resources
        if (count.value < 10):
            count.value += 2

            # # Dividing the array elements
            L = mp.Manager().list(arr[:mid])

            # # into 2 halves
            R = mp.Manager().list(arr[mid:])

            p_l = mp.Process(
                target=merge_sort_with_processes, args=(L, count))
            p_r = mp.Process(
                target=merge_sort_with_processes, args=(R, count))

            p_l.start()
            p_r.start()

            p_l.join()
            p_r.join()
            
            # combine the sorted L and R arrays back into our main array
            combine_arrays(arr, L, R)
        else:
            L = arr[:mid]
            R = arr[mid:]
            merge_sort(L)
            merge_sort(R)
            combine_arrays(arr, L, R)


# -----------------------------------------------------------------------------


def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))


# -----------------------------------------------------------------------------
def merge_normal(arr):
    merge_sort(arr)


# -----------------------------------------------------------------------------
def merge_sort_thread(arr):
    merge_sort_with_threads(arr)
    print(f'merge_sort_thread done, used {number_threads} threads')


# -----------------------------------------------------------------------------
def merge_sort_process(arr):
    # Copy array into a shared list
    new_arr = mp.Manager().list(arr)
    count = mp.Value('i', 0)
    merge_sort_with_processes(new_arr, count)

    print(f'merge_sort_process done, used {count.value} processes') # type: ignore
 
    for i in range(len(new_arr)):
        arr[i] = new_arr[i]


# -----------------------------------------------------------------------------
def main():
    merges = [
        (merge_sort, ' Normal Merge Sort '),
        (merge_sort_thread, ' Threaded Merge Sort '),
        #(merge_sort_process, ' Processes Merge Sort '
        
    ]

    for merge_function, desc in merges:
        # Create list of random values to sort
        arr = [random.randint(1, 10_000_000) for _ in range(1_000)]

        print(f'\n{desc:-^90}')
        print(f'Before: {str(arr[:5])[1:-1]} ... {str(arr[-5:])[1:-1]}')
        start_time = time.perf_counter()

        merge_function(arr)

        end_time = time.perf_counter()
        print(f'Sorted: {str(arr[:5])[1:-1]} ... {str(arr[-5:])[1:-1]}')

        print('Array is sorted' if is_sorted(arr) else 'Array is NOT sorted')
        print(f'Time to sort = {end_time - start_time}')


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
