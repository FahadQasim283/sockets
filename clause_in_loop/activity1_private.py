# activity1_private.py
# Activity 1: PRIVATE – each thread has its own local variables.

from concurrent.futures import ThreadPoolExecutor

def run(n=8, max_workers=4):
    print("Activity 1: PRIVATE (each thread has its own 'i' and 'a')")
    def worker(i):
        a = i + 1  # 'a' is private (local)
        print(f"[i={i}] -> a = {a}")
        return a

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        list(ex.map(worker, range(n)))
    print()

if __name__ == "__main__":
    run()
