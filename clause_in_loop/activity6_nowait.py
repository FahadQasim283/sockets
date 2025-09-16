# activity6_nowait.py
# Activity 6: NOWAIT – second loop can start without waiting for the first to finish.

from concurrent.futures import ThreadPoolExecutor, as_completed

def run(N=10, max_workers=4):
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
        # Submit second loop immediately (no barrier)
        futures += [ex.submit(second_loop, i) for i in range(N)]
        for _ in as_completed(futures):
            pass

    print("Array after both loops:", array, "\n")
    return array

if __name__ == "__main__":
    run()
