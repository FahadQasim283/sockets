import concurrent.futures
import os

def compute(i, n):
    # Simulate OpenMP's omp_get_thread_num() using process id
    thread_id = os.getpid() % 10000   # just to distinguish workers
    return thread_id * n + i

def main():
    n = 100
    result = [0] * n

    print("Results with dynamic scheduling:")

    # Use ThreadPoolExecutor or ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks dynamically
        futures = {executor.submit(compute, i, n): i for i in range(n)}

        for future in concurrent.futures.as_completed(futures):
            i = futures[future]
            result[i] = future.result()

    print(result)

if __name__ == "__main__":
    main()
