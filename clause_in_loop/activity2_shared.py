# activity2_shared.py
# Activity 2: SHARED – all threads can read/write the same array (with care).

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

def run(n=8, max_workers=4):
    print("Activity 2: SHARED (vector 'a' is shared)")
    a = [0]*n
    lock = Lock()  # not strictly needed if indices are unique; included for clarity

    def worker(i):
        val = a[i] + i
        with lock:
            a[i] = val
        print(f"a[{i}] = {a[i]}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(worker, range(n)))
    print("Final shared a:", a, "\n")

if __name__ == "__main__":
    run()
