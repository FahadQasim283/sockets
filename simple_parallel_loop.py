import multiprocessing as mp

def sum_squares(start, end):
    total = 0
    for i in range(start, end):
        total += i ** 2
    return total

if __name__ == '__main__':
    n = 100
    num_processes = 4
    chunk_size = n // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    if n % num_processes != 0:
        ranges[-1] = (ranges[-1][0], n)
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(sum_squares, ranges)
    
    total_sum = sum(results)
    print(f"Sum of squares from 0 to {n-1} is {total_sum}")
