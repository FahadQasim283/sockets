# graded_task2_reduction_sum.py
# Graded Task 2: Parallel sum of an array using a reduction-style pattern.

from concurrent.futures import ThreadPoolExecutor, as_completed
from schedule_utils import make_chunks_static, make_chunks_dynamic, make_chunks_guided

def reduction_sum(array, chunk=16, schedule="static", max_workers=4):
    """
    Parallel sum of a 1-D array:
      - Each task computes a local partial sum (private accumulator).
      - The main thread reduces (adds) all partials into the final result.
    """
    n = len(array)
    if n == 0:
        return 0

    def sum_partial(indices):
        s = 0
        for i in indices:
            s += array[i]
        # Print once per partial for visibility
        print(f"Partial {indices[0]}..{indices[-1]} -> {s}")
        return s

    # Partition work
    if schedule == "static":
        buckets = make_chunks_static(n, chunk, max_workers)
        work = [bucket for bucket in buckets if bucket]
    elif schedule == "dynamic":
        work = make_chunks_dynamic(n, chunk)
    elif schedule == "guided":
        work = make_chunks_guided(n, max(1, chunk))
    else:
        raise ValueError("Unknown schedule")

    # Parallel partial sums + reduction
    total = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(sum_partial, bucket) for bucket in work]
        for f in as_completed(futures):
            total += f.result()

    return total

def demo():
    # Example usage for your report
    data = list(range(1, 51))  # 1..50 => expected sum = 1275
    print("Input length:", len(data))
    ans1 = reduction_sum(data, chunk=8, schedule="static",  max_workers=4)
    print("Total (static): ", ans1)
    ans2 = reduction_sum(data, chunk=8, schedule="dynamic", max_workers=4)
    print("Total (dynamic):", ans2)
    ans3 = reduction_sum(data, chunk=8, schedule="guided",  max_workers=4)
    print("Total (guided): ", ans3)

if __name__ == "__main__":
    demo()
