import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_chunks_static(n, chunk_size, num_workers):
    """Create static chunks distributed among workers."""
    indices = list(range(n))
    chunked = [indices[i:i+chunk_size] for i in range(0, n, chunk_size)]
    buckets = [[] for _ in range(num_workers)]
    for i, ch in enumerate(chunked):
        buckets[i % num_workers].extend(ch)
    return buckets

def make_chunks_dynamic(n, chunk_size):
    """Create dynamic chunks."""
    return [list(range(i, min(i+chunk_size, n))) for i in range(0, n, chunk_size)]

def make_chunks_guided(n, min_chunk=1):
    """Create guided chunks with decreasing sizes."""
    remaining = n
    start = 0
    chunks = []
    while remaining > 0:
        size = max(remaining // 2, min_chunk)
        end = min(start + size, n)
        chunks.append(list(range(start, end)))
        consumed = end - start
        start = end
        remaining -= consumed
    return chunks

def process_chunk(indices, worker_id, schedule_type):
    """Process a chunk of indices, simulating work."""
    # Simulate variable work
    work_time = random.uniform(0.01, 0.05)
    time.sleep(work_time)
    result = sum(i**2 for i in indices)
    print(f"[{schedule_type}] Worker {worker_id} processed {len(indices)} items: {indices[:3]}{'...' if len(indices) > 3 else ''} -> partial sum = {result}")
    return result

def run_schedule(n, chunk_size, schedule_type, num_workers=4):
    """Run computation with specified schedule."""
    print(f"\n--- Running {schedule_type.upper()} scheduling ---")
    start_time = time.time()

    if schedule_type == "static":
        buckets = make_chunks_static(n, chunk_size, num_workers)
        work = [bucket for bucket in buckets if bucket]
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_chunk, bucket, i, schedule_type) for i, bucket in enumerate(work)]
            results = [f.result() for f in futures]
    elif schedule_type == "dynamic":
        chunks = make_chunks_dynamic(n, chunk_size)
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_chunk, chunk, i, schedule_type) for i, chunk in enumerate(chunks)]
            results = [f.result() for f in as_completed(futures)]
    elif schedule_type == "guided":
        chunks = make_chunks_guided(n, max(1, chunk_size // 2))
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_chunk, chunk, i, schedule_type) for i, chunk in enumerate(chunks)]
            results = [f.result() for f in as_completed(futures)]
    else:
        raise ValueError("Unknown schedule type")

    total_sum = sum(results)
    end_time = time.time()
    print(f"[{schedule_type.upper()}] Total sum: {total_sum}, Time: {end_time - start_time:.4f}s")
    return total_sum, end_time - start_time

def main():
    n = 50  # Total items
    chunk_size = 5
    num_workers = 4

    print("Experimenting with different scheduling options")
    print(f"n = {n}, chunk_size = {chunk_size}, num_workers = {num_workers}")

    schedules = ["static", "dynamic", "guided"]
    results = {}

    for schedule in schedules:
        total_sum, elapsed = run_schedule(n, chunk_size, schedule, num_workers)
        results[schedule] = (total_sum, elapsed)

    print("\n--- Summary ---")
    expected_sum = sum(i**2 for i in range(n))
    for schedule, (total_sum, elapsed) in results.items():
        print(f"{schedule.upper()}: Sum correct = {total_sum == expected_sum}, Time = {elapsed:.4f}s")

if __name__ == "__main__":
    main()

# Explanation of the question:
# The question asks to write a program and experiment with different scheduling options (static, dynamic, guided) by changing the schedule clause in the code.
# Scheduling in parallel computing determines how work is distributed among threads/processes.
# - Static scheduling: Work is divided into chunks and assigned to threads at the beginning. Good for uniform work.
# - Dynamic scheduling: Chunks are assigned to threads as they become available. Better for variable work times.
# - Guided scheduling: Starts with large chunks that decrease in size, combining benefits of static and dynamic.
# This program simulates these scheduling types using Python's ThreadPoolExecutor.
# It computes the sum of squares for numbers 0 to n-1, divided into chunks.
# Each scheduling type is run, and the output shows which worker processed which chunks, along with timing.
# The program demonstrates how different schedules affect work distribution and performance.