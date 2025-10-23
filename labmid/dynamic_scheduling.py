import multiprocessing as mp
import time
import random

def make_chunks_dynamic(n, chunk_size):
    """Generate chunks for dynamic scheduling."""
    chunks = []
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append((start, end))
        start = end
    return chunks

def process_chunk(chunk_id, start, end, process_id):
    """Simulate processing a chunk with some work."""
    # Simulate variable work time
    work_time = random.uniform(0.01, 0.1)
    time.sleep(work_time)
    result = sum(range(start, end))
    print(f"Process {process_id} processed chunk {chunk_id}: range({start}, {end}) -> sum = {result}")
    return result

def worker(queue, results, process_id):
    """Worker function that processes chunks from the queue."""
    while True:
        try:
            chunk = queue.get(timeout=1)  # Wait for a chunk
            if chunk is None:  # Sentinel to stop
                break
            chunk_id, start, end = chunk
            result = process_chunk(chunk_id, start, end, process_id)
            results.append(result)
        except:
            break

def main():
    n = 100
    chunk_size = 10
    num_processes = 4

    chunks = make_chunks_dynamic(n, chunk_size)
    print(f"Total chunks: {len(chunks)}")
    for i, (start, end) in enumerate(chunks):
        print(f"Chunk {i}: range({start}, {end})")

    # Create a queue for chunks
    queue = mp.Queue()
    for i, (start, end) in enumerate(chunks):
        queue.put((i, start, end))

    # Add sentinels
    for _ in range(num_processes):
        queue.put(None)

    # Shared list for results
    manager = mp.Manager()
    results = manager.list()

    print(f"\nStarting {num_processes} processes with dynamic scheduling...")

    start_time = time.time()

    processes = []
    for i in range(num_processes):
        p = mp.Process(target=worker, args=(queue, results, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time()

    total_sum = sum(results)
    expected_sum = sum(range(n))

    print(f"\nTotal sum: {total_sum}")
    print(f"Expected sum: {expected_sum}")
    print(f"Match: {total_sum == expected_sum}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()

# Explanation of the question:
# The question asks to write a program to observe the output with dynamic scheduling.
# Dynamic scheduling in parallel computing means that work chunks are assigned to threads/processes as they become available,
# rather than pre-assigning all chunks at the start. This can lead to better load balancing when work per chunk varies.
# In this program, we simulate dynamic scheduling using a queue. Chunks are placed in a queue, and worker processes
# take chunks from the queue as they finish their current work. Each chunk processes a range of numbers and computes their sum.
# The output shows which process handled which chunk, demonstrating how dynamic scheduling distributes work.
# We use random sleep times to simulate variable work per chunk, showing how dynamic scheduling adapts to this.