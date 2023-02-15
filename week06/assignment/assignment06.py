'''
Requirements
1. Finish the team06 assignment (if necessary).
2. Change your program to process all 300 images using 1 CPU, then 2 CPUs, all the way up to the
   number of CPUs on your computer plus 4.
3. Keep track of the time it takes to process all 300 images per CPU.
4. Plot the time to process vs the number of CPUs.
   
Questions:
1. What is the relationship between the time to process versus the number of CPUs?
   Does there appear to be an asymptote? If so, what do you think the asymptote is?
   > The graph is an exponential decay function so as the number of CPUs increases the time to process drastically decreases.
   > There appears to be a horizontal asymptote to me which is about y = 12 seconds.
2. Is this a CPU bound or IO bound problem? Why?
   > This is a CPU bound problem, there is no input or output to deal with.
   > The computer is strictly processing images and only relies on the CPU.
3. Would threads work on this assignment? Why or why not? (guess if you need to) 
   > I don't think threads would really help on this assignment because this is a CPU bound problem,
   > and threads only improve performance in I/O bound problems.
'''

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4

# TODO Your final video need to have 300 processed frames.  However, while you are
# testing your code, set this much lower
FRAME_COUNT = 300

RED = 0
GREEN = 1
BLUE = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels
    mask = (np_img[:, :, BLUE] < 120) & (
        np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# This process_frames function is the function that is called by the map function and will get the images and pass them to the
# create_new_frame function so the combined image can be created.
def process_frames(image_number):
    image_file = rf'elephant/image{image_number:03d}.png'
    green_file = rf'green/image{image_number:03d}.png'
    process_file = rf'processed/image{image_number:03d}.png'

    create_new_frame(image_file, green_file, process_file)


if __name__ == '__main__':
    all_process_time = timeit.default_timer()

    # Use two lists: one to track the number of CPUs and the other to track
    # the time it takes to process the images given this number of CPUs.
    xaxis_cpus = []
    yaxis_times = []

    # List of integers for the number of each frame we need to process.
    inputs = list(range(1, FRAME_COUNT + 1))

    # For loop that will start 1 cpu, then 2 cpus, and go all the way to CPU_COUNT (which is the number of cpus on the machine plus 4).
    for count in range(1, CPU_COUNT + 1):
        # Starts a timer for this iteration.
        start_time = timeit.default_timer()

        # Starts the processing pool and calls the map function to process each frame.
        with mp.Pool(count) as p:
            p.map(process_frames, inputs)

        # Prints the number of CPU cores used and the time taken to process all images.
        print(f'\n\nProcessed with {count} CPU cores.')
        time_taken = timeit.default_timer() - start_time
        print(
            f'Time To Process all images = {time_taken} seconds')

        # Appending the data to the lists for the graph.
        xaxis_cpus.append(count)
        yaxis_times.append(time_taken)

    print(
        f'Total Time for ALL processing: {timeit.default_timer() - all_process_time} seconds')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')

    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
