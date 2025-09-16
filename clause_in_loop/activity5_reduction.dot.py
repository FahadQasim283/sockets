# activity5_reduction_dot.py
# Activity 5: REDUCTION – dot product with static/dynamic/guided schedules.

from concurrent.futures import ThreadPoolExecutor, as_completed
from schedule_utils import make_chunks_static, make_chunks_dynamic, make_chunks_guided

def run(n=40, chunk=5, schedule="static", max_workers=4):
    print(f"Activity 5: REDUCTION (dot product) schedule={schedule}, chunk={chunk}")
    a = [float(i) for i in range(n)]
    b = [2.0*float(i) for i in range(n)]

    def dot_partial(indices):
        partial = 0.0
        for i in indices:
            partial += a[i] * b[i]
        print(f"Partial {indices[0]}..{indices[-1]} -> {partial}")
        return partial

    if schedule == "static":
        buckets = make_chunks_static(n, chunk, max_workers)
        work = [bucket for bucket in buckets if bucket]
    elif schedule == "dynamic":
        work = make_chunks_dynamic(n, chunk)
    elif schedule == "guided":
        work = make_chunks_guided(n, max(1, chunk))
    else:
        raise ValueError("Unknown schedule")

    result = 0.0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = []
        if schedule == "static":
            futures = [ex.submit(dot_partial, bucket) for bucket in work]
        else:
            futures = [ex.submit(dot_partial, chunk_ixs) for chunk_ixs in work]
        for f in as_completed(futures):
            result += f.result()

    print(f"Final dot product = {result}\n")
    return result

if __name__ == "__main__":
    run()
