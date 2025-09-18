import concurrent.futures
import os
import math

def compute(i, n):
    thread_id = os.getpid() % 10000
    return thread_id * n + i

def static_schedule(n, num_workers=4):
    """Split iterations equally among workers."""
    chunk = math.ceil(n / num_workers)
    result = [0] * n
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        for w in range(num_workers):
            start = w * chunk
            end = min(start + chunk, n)
            for i, val in zip(range(start, end),
                              executor.map(lambda j: compute(j, n), range(start, end))):
                result[i] = val
    return result

def dynamic_schedule(n):
    """Tasks assigned dynamically to available workers."""
    result = [0] * n
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(compute, i, n): i for i in range(n)}
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]
            result[i] = future.result()
    return result

def guided_schedule(n, num_workers=4):
    """Decreasing chunk sizes like guided scheduling in OpenMP."""
    result = [0] * n
    remaining = n
    start = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        while remaining > 0:
            chunk = max(1, remaining // 2)  # halve each time
            end = min(start + chunk, n)
            for i, val in zip(range(start, end),
                              executor.map(lambda j: compute(j, n), range(start, end))):
                result[i] = val
            start = end
            remaining = n - start
    return result

if __name__ == "__main__":
    n = 20

    print("Static scheduling result:")
    print(static_schedule(n))

    print("\nDynamic scheduling result:")
    print(dynamic_schedule(n))

    print("\nGuided scheduling result:")
    print(guided_schedule(n))
