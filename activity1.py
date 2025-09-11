import multiprocessing as mp

def worker(i):
    print(f"Process {mp.current_process().name} executes loop iteration {i}")

if __name__ == '__main__':
    n = 9
    with mp.Pool(processes=4) as pool:
        pool.map(worker, range(n))
