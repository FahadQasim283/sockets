# schedule_utils.py
# Helpers to mimic OpenMP scheduling (static, dynamic, guided)

def make_chunks_static(n, chunk, num_workers):
    indices = list(range(n))
    chunked = [indices[i:i+chunk] for i in range(0, n, chunk)]
    buckets = [[] for _ in range(num_workers)]
    for i, ch in enumerate(chunked):
        buckets[i % num_workers].extend(ch)
    return buckets

def make_chunks_dynamic(n, chunk):
    return [list(range(i, min(i+chunk, n))) for i in range(0, n, chunk)]

def make_chunks_guided(n, min_chunk=1):
    remaining = n
    start = 0
    chunks = []
    while remaining > 0:
        size = max(remaining // 2, min_chunk)  # decreasing chunk sizes
        end = min(start + size, n)
        chunks.append(list(range(start, end)))
        consumed = end - start
        start = end
        remaining -= consumed
    return chunks
