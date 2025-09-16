# activity4_lastprivate.py
# Activity 4: LASTPRIVATE – capture the value from the sequentially last iteration.

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

def run(n=8, max_workers=4):
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

    a_after = results[n-1]  # value from the last (sequential) iteration
    print(f"Value of a after parallel for: a = {a_after}\n")

if __name__ == "__main__":
    run()
