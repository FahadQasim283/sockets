# activity3_firstprivate.py
# Activity 3: FIRSTPRIVATE – each thread gets an initialized private copy.

from concurrent.futures import ThreadPoolExecutor, as_completed

def run(vlen=16, n=4, max_workers=4):
    print("Activity 3: FIRSTPRIVATE (each thread gets copy of 'indx')")
    a = [-(i+1) for i in range(vlen)]
    indx_init = 4  # master copy before parallel region

    def worker(tid, start_index):
        indx = start_index  # firstprivate copy for this thread
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

if __name__ == "__main__":
    run()
