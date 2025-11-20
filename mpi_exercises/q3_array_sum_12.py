import multiprocessing as mp

def sum_partial(array_chunk):
    """Compute sum of a chunk of the array."""
    return sum(array_chunk)

def main():
    array = list(range(12))  # Array of size 12: [0, 1, 2, ..., 11]
    num_processes = 4  # Using 4 processes

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

# Explanation of Q3:
# This program computes the sum of an array of size 12 by distributing the elements across 4 processes.
# Each process calculates the partial sum of its assigned chunk.
# The partial sums are then combined to get the total sum.
# With 12 elements and 4 processes, each process gets exactly 3 elements (12 // 4 = 3).
# This demonstrates parallel reduction: distributing computation and combining results.