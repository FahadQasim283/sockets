import multiprocessing as mp
import time

def compute_sum(start, end):
    """Function to compute sum of numbers in a range."""
    total = 0
    for i in range(start, end):
        total += i
    return total

def main():
    n = 1000000  # Large number to demonstrate parallelism
    num_processes = mp.cpu_count()  # Use all available CPU cores
    chunk_size = n // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    if n % num_processes != 0:
        ranges[-1] = (ranges[-1][0], n)

    print(f"Computing sum from 0 to {n-1} using {num_processes} processes")

    start_time = time.time()

    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(compute_sum, ranges)

    total_sum = sum(results)
    end_time = time.time()

    print(f"Total sum: {total_sum}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()

# Explanation of the question:
# The question asks to write a simple parallel program that uses a Loop Construct.
# In this program, we use multiprocessing to parallelize a loop that computes the sum of numbers from 0 to n-1.
# The loop is divided into chunks, each processed by a separate process.
# This demonstrates parallel execution using Python's multiprocessing module, which simulates a parallel loop construct.
# The Pool.starmap function is used to apply the compute_sum function to each range in parallel.
# This approach distributes the workload across multiple CPU cores, potentially speeding up the computation for large n.