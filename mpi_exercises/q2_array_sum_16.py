import multiprocessing as mp

def sum_partial(array_chunk):
    """Compute sum of a chunk of the array."""
    return sum(array_chunk)

def main():
    array = list(range(16))  # Array of size 16: [0, 1, 2, ..., 15]
    num_processes = 6

    print(f"Array: {array}")
    print(f"Number of processes: {num_processes}")

    # Divide array into chunks
    chunk_size = len(array) // num_processes
    chunks = [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]
    # Adjust last chunk if necessary
    if len(chunks) > num_processes:
        chunks[num_processes - 1].extend(chunks.pop())

    print(f"Chunks: {chunks}")

    with mp.Pool(processes=num_processes) as pool:
        partial_sums = pool.map(sum_partial, chunks)

    total_sum = sum(partial_sums)

    print(f"Partial sums: {partial_sums}")
    print(f"Total sum: {total_sum}")
    print(f"Expected sum: {sum(array)}")
    print(f"Match: {total_sum == sum(array)}")

if __name__ == "__main__":
    main()

# Explanation of Q2:
# This program parallelizes the computation of the sum of an array of size 16 using 6 processes.
# The array elements are distributed across the 6 processes as evenly as possible.
# Each process computes the sum of its assigned chunk.
# The partial sums are then combined (reduced) to get the total sum.
# Since 16 elements and 6 processes, some processes get 2 elements, some get 3 (16 // 6 = 2, remainder 4, so 4 processes get 3, 2 get 2).
# This demonstrates distributing work and combining results in parallel computing.