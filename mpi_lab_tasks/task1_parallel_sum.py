import multiprocessing as mp
import time
import math

def compute_partial_sum(start, end, queue):
    """Compute sum from start to end-1 and send via queue (non-blocking send)."""
    partial_sum = sum(range(start, end))
    queue.put(partial_sum)  # Non-blocking put
    return partial_sum

def run_parallel_sum(num_processes, N=1000000):
    """Run parallel sum calculation with given number of processes."""
    chunk_size = N // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    if N % num_processes != 0:
        ranges[-1] = (ranges[-1][0], N)

    queue = mp.Queue()
    processes = []

    start_time = time.time()

    # Start processes (non-blocking)
    for start, end in ranges:
        p = mp.Process(target=compute_partial_sum, args=(start, end, queue))
        p.start()
        processes.append(p)

    # Collect results (simulating gathering)
    total_sum = 0
    for _ in range(num_processes):
        partial_sum = queue.get()  # Blocking get, but processes are non-blocking
        total_sum += partial_sum

    # Wait for all processes to finish
    for p in processes:
        p.join()

    end_time = time.time()
    execution_time = end_time - start_time

    return total_sum, execution_time

def main():
    N = 1000000  # Sum from 0 to 999999
    expected_sum = N * (N - 1) // 2

    nodes = [1, 2, 4, 16]
    base_time = None

    for num_nodes in nodes:
        total_sum, exec_time = run_parallel_sum(num_nodes, N)
        print(f"Output: (On {num_nodes} Node{'s' if num_nodes > 1 else ''})")
        print(f"Total Sum: {total_sum}")
        print(f"Execution Time: {exec_time:.6f} seconds")

        if num_nodes == 1:
            base_time = exec_time
            speedup = 1.0
        else:
            speedup = base_time / exec_time if exec_time > 0 else float('inf')

        if num_nodes > 1:
            print(f"Speedup: {speedup:.2f}")

        print(f"Correct: {total_sum == expected_sum}")
        print("-" * 40)

if __name__ == "__main__":
    main()

# Explanation of Task 1:
# This program simulates a parallel sum calculation using non-blocking process communications.
# Each process computes a partial sum of a range of numbers and sends the result via a queue (non-blocking put).
# The main process collects all partial sums to compute the total.
# Execution time is measured for different numbers of processes (nodes): 1, 2, 4, 16.
# Speedup is calculated as the ratio of single-node time to multi-node time.
# Non-blocking communication is simulated by starting processes asynchronously and using queue.put() which is non-blocking in this context.
# The program demonstrates how parallel processing can speed up computation by distributing work across multiple processes.