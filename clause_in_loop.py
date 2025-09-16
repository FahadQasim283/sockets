from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

print("Python OpenMP-like Clauses Demo\n")

# ---------------- Scheduling Helpers ---------------- #
def make_chunks_static(n, chunk, num_workers):
    indices = list(range(n))
    chunked = [indices[i:i+chunk] for i in range(0, n, chunk)]
    buckets = [[] for _ in range(num_workers)]
    for i, ch in enumerate(chunked):
        buckets[i % num_workers].extend(ch)
    return buckets

def make_chunks_dynamic(n, chunk):
    return [list(range(i, min(i+chunk, n))) for i in range(0, n, chunk)]

def make_chunks_guided(n, min_chunk=1):
    remaining = n
    start = 0
    chunks = []
    while remaining > 0:
        size = max(remaining // 2, min_chunk)
        end = min(start + size, n)
        chunks.append(list(range(start, end)))
        consumed = end - start
        start = end
        remaining -= consumed
    return chunks

# ---------------- Activities ---------------- #

# Activity 1: PRIVATE
def activity1_private(n=8, max_workers=4):
    print("Activity 1: PRIVATE (each thread has its own 'i' and 'a')")
    def worker(i):
        a = i + 1
        print(f"[{i}] -> a = {a}")
        return a

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(worker, range(n)))
    print()

# Activity 2: SHARED
def activity2_shared(n=8, max_workers=4):
    print("Activity 2: SHARED (vector 'a' is shared)")
    a = [0]*n
    lock = Lock()

    def worker(i):
        val = a[i] + i
        with lock:
            a[i] = val
        print(f"a[{i}] = {a[i]}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(worker, range(n)))
    print("Final shared a:", a, "\n")

# Activity 3: FIRSTPRIVATE
def activity3_firstprivate(vlen=16, n=4, max_workers=4):
    print("Activity 3: FIRSTPRIVATE (each thread gets copy of 'indx')")
    a = [-(i+1) for i in range(vlen)]
    indx_init = 4

    def worker(tid, start_index):
        indx = start_index  # firstprivate copy
        for i in range(indx, min(indx+n, vlen)):
            a[i] = tid + 1
        print(f"Thread {tid}: wrote a[{indx}:{min(indx+n, vlen)}] = {tid+1}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = []
        for tid in range(max_workers):
            futures.append(ex.submit(worker, tid, indx_init + n*tid))
        for _ in as_completed(futures):
            pass

    print("After the parallel region:")
    for i, val in enumerate(a):
        print(f"a[{i}] = {val}")
    print()

# Activity 4: LASTPRIVATE
def activity4_lastprivate(n=8, max_workers=4):
    print("Activity 4: LASTPRIVATE (value from last iteration visible after loop)")
    results = {}
    lock = Lock()

    def worker(i):
        a = i + 1
        print(f"Thread ? has a value of a = {a} for i = {i}")
        with lock:
            results[i] = a

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(worker, range(n)))

    a_after = results[n-1]
    print(f"Value of a after parallel for: a = {a_after}\n")

# Activity 5: REDUCTION (dot product)
def activity5_reduction_dot(n=40, chunk=5, schedule="static", max_workers=4):
    print(f"Activity 5: REDUCTION (dot product) with schedule={schedule}, chunk={chunk}")
    a = [float(i) for i in range(n)]
    b = [2.0*float(i) for i in range(n)]

    def dot_partial(indices):
        partial = 0.0
        for i in indices:
            partial += a[i] * b[i]
        print(f"Partial from {indices[0]}..{indices[-1]} -> {partial}")
        return partial

    if schedule == "static":
        buckets = make_chunks_static(n, chunk, max_workers)
        work = [bucket for bucket in buckets if bucket]
    elif schedule == "dynamic":
        work = make_chunks_dynamic(n, chunk)
    elif schedule == "guided":
        work = make_chunks_guided(n, max(1, chunk))
    else:
        raise ValueError("Unknown schedule")

    result = 0.0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        if schedule == "static":
            futures = [ex.submit(dot_partial, bucket) for bucket in work]
        else:
            futures = [ex.submit(dot_partial, chunk_ixs) for chunk_ixs in work]
        for f in as_completed(futures):
            result += f.result()

    print(f"Final result = {result}\n")

# Activity 6: NOWAIT
def activity6_nowait(N=10, max_workers=4):
    print("Activity 6: NOWAIT (second loop starts without waiting)")
    array = [0]*N

    def first_loop(i):
        array[i] = i*i
        print(f"First loop: array[{i}] = {array[i]}")

    def second_loop(i):
        array[i] += 5
        print(f"Second loop: array[{i}] = {array[i]}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(first_loop, i) for i in range(N)]
        futures += [ex.submit(second_loop, i) for i in range(N)]
        for _ in as_completed(futures):
            pass

    print("Array after both loops:", array, "\n")

# ---------------- Run All ---------------- #
if __name__ == "__main__":
    activity1_private()
    activity2_shared()
    activity3_firstprivate()
    activity4_lastprivate()
    activity5_reduction_dot(schedule="static")
    activity5_reduction_dot(schedule="dynamic")
    activity5_reduction_dot(schedule="guided")
    activity6_nowait()
