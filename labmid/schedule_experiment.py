"""schedule_experiment.py

Demonstrate how different loop scheduling strategies (static, dynamic, guided)
affect the order in which loop iterations are executed. The script prints which
process handled each iteration so you can observe ordering and load distribution.

Usage (examples):
    python schedule_experiment.py --schedule static --n 32 --chunk 4 --procs 4
    python schedule_experiment.py --schedule dynamic --n 32 --chunk 3 --procs 4
    python schedule_experiment.py --schedule guided --n 32 --chunk 2 --procs 4

The script is written to be Windows-friendly (multiprocessing guard).

At the end of the file there's an explanation of the question and notes.
"""

from multiprocessing import Process, Queue, Manager, cpu_count
import argparse
import time
import math
import random


def make_chunks_static(n, chunk, num_workers):
    # Pre-assign chunks round-robin to workers (like OpenMP static with chunk)
    indices = list(range(n))
    chunked = [indices[i:i+chunk] for i in range(0, n, chunk)]
    buckets = [[] for _ in range(num_workers)]
    for i, ch in enumerate(chunked):
        buckets[i % num_workers].extend(ch)
    # convert to list of (chunk_id, start, end)
    out = []
    cid = 0
    for b in buckets:
        if not b:
            cid += 1
            continue
        # group contiguous ranges inside bucket for nicer prints
        i = 0
        while i < len(b):
            j = i + 1
            while j < len(b) and b[j] == b[j-1] + 1:
                j += 1
            out.append((cid, b[i], b[j-1]+1))
            i = j
            cid += 1
    return out


def make_chunks_dynamic(n, chunk):
    # Return list of chunks (chunk_id, start, end) in natural order
    out = []
    cid = 0
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        out.append((cid, start, end))
        cid += 1
    return out


def make_chunks_guided(n, min_chunk):
    # Guided: chunks start larger and decrease over time (simulating OpenMP guided)
    remaining = n
    start = 0
    cid = 0
    out = []
    while start < n:
        # size proportional to remaining / P but at least min_chunk
        size = max(remaining // 2, min_chunk)
        end = min(start + size, n)
        out.append((cid, start, end))
        cid += 1
        consumed = end - start
        start = end
        remaining -= consumed
    return out


def worker_static(worker_id, assigned_ranges, output_list):
    # Static worker: processes its pre-assigned ranges in order
    for cid, start, end in assigned_ranges:
        for i in range(start, end):
            # simulate non-uniform work to show scheduling effects
            time.sleep(random.uniform(0.001, 0.005))
            output_list.append((i, worker_id, cid))


def worker_dynamic(q: Queue, output_list, worker_id):
    # Dynamic worker: fetch next chunk from queue until sentinel
    while True:
        task = q.get()
        if task is None:
            break
        cid, start, end = task
        for i in range(start, end):
            time.sleep(random.uniform(0.001, 0.005))
            output_list.append((i, worker_id, cid))


def run_experiment(schedule: str, n: int, chunk: int, procs: int):
    manager = Manager()
    output = manager.list()

    if schedule == "static":
        assigned = make_chunks_static(n, chunk, procs)
        # distribute assigned chunks per worker for the static implementation
        # assigned is list of (cid,start,end) in the order we created - but
        # we want each worker to have contiguous list of assigned ranges.
        worker_buckets = [[] for _ in range(procs)]
        for idx, item in enumerate(assigned):
            worker_buckets[idx % procs].append(item)

        procs_list = []
        for pid in range(procs):
            p = Process(target=worker_static, args=(pid, worker_buckets[pid], output))
            procs_list.append(p)
            p.start()

        for p in procs_list:
            p.join()

    elif schedule == "dynamic":
        q = Queue()
        chunks = make_chunks_dynamic(n, chunk)
        for t in chunks:
            q.put(t)
        # sentinels
        for _ in range(procs):
            q.put(None)

        procs_list = []
        for pid in range(procs):
            p = Process(target=worker_dynamic, args=(q, output, pid))
            procs_list.append(p)
            p.start()

        for p in procs_list:
            p.join()

    elif schedule == "guided":
        chunks = make_chunks_guided(n, max(1, chunk))
        q = Queue()
        for t in chunks:
            q.put(t)
        for _ in range(procs):
            q.put(None)

        procs_list = []
        for pid in range(procs):
            p = Process(target=worker_dynamic, args=(q, output, pid))
            procs_list.append(p)
            p.start()

        for p in procs_list:
            p.join()

    else:
        raise ValueError("Unknown schedule: %r" % schedule)

    # Convert output (iteration, worker, chunk_id) to list and sort by time of append
    result = list(output)
    # Print execution order by the sequence items were appended
    print(f"\nSchedule: {schedule}  n={n} chunk={chunk} procs={procs}")
    for seq, entry in enumerate(result):
        it, wid, cid = entry
        print(f"{seq:03d}: iteration {it:02d} executed by worker {wid} (chunk {cid})")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", choices=["static", "dynamic", "guided"], default="static")
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--chunk", type=int, default=4)
    parser.add_argument("--procs", type=int, default=min(4, cpu_count()))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Seed random so repeated runs are similar but still show variation
    random.seed(1)
    run_experiment(args.schedule, args.n, args.chunk, args.procs)
