import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import time

def compute_partial_sum(chunk_data):
    """
    Compute partial sum for a chunk of array.
    This simulates the private accumulator in reduction clause.
    
    Args:
        chunk_data: tuple of (chunk_id, array_chunk)
    
    Returns:
        tuple: (chunk_id, partial_sum)
    """
    chunk_id, array_chunk = chunk_data
    partial_sum = sum(array_chunk)
    return chunk_id, partial_sum


def parallel_reduction_sum(array, num_workers=4):
    """
    Parallel sum using reduction pattern.
    
    Pattern mimics OpenMP reduction clause:
    #pragma omp parallel for reduction(+:sum)
    
    Steps:
    1. Distribute array chunks to workers (scatter)
    2. Each worker computes local partial sum (private variables)
    3. Master thread reduces all partials into final sum (reduction operation)
    
    Args:
        array: Input array to sum
        num_workers: Number of parallel workers
    
    Returns:
        Total sum of array
    """
    n = len(array)
    chunk_size = (n + num_workers - 1) // num_workers  # Ceiling division
    
    # Create chunks with IDs
    chunks = []
    for i in range(num_workers):
        start = i * chunk_size
        end = min(start + chunk_size, n)
        if start < n:
            chunks.append((i, array[start:end]))
    
    print(f"Array divided into {len(chunks)} chunks")
    for chunk_id, chunk in chunks:
        print(f"  Worker {chunk_id}: {len(chunk)} elements -> range [{chunk[0]}..{chunk[-1]}]")
    print()
    
    # Parallel computation of partial sums
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(compute_partial_sum, chunks))
    
    # Display partial results
    print("Partial sums computed:")
    for chunk_id, partial in sorted(results):
        print(f"  Worker {chunk_id}: Partial sum = {partial}")
    print()
    
    # Reduction: Combine all partial sums
    print("Reduction operation:")
    partial_values = [partial for _, partial in sorted(results)]
    print(f"  {' + '.join(map(str, partial_values))} = ", end="")
    total_sum = sum(partial for _, partial in results)
    print(total_sum)
    
    return total_sum


def main():
    """Main function demonstrating reduction clause for array sum."""
    
    print("=" * 70)
    print("PARALLEL ARRAY SUM USING REDUCTION CLAUSE")
    print("=" * 70)
    print()
    
    # Configuration
    array_size = 100
    num_workers = 4
    array = list(range(1, array_size + 1))  # [1, 2, 3, ..., 100]
    expected_sum = sum(array)
    
    print(f"Array: [1, 2, 3, ..., {array_size}]")
    print(f"Array size: {array_size}")
    print(f"Number of workers: {num_workers}")
    print(f"Expected sum: {expected_sum}")
    print()
    
    # Parallel reduction sum
    print("REDUCTION OPERATION:")
    print("-" * 70)
    start_time = time.time()
    computed_sum = parallel_reduction_sum(array, num_workers)
    end_time = time.time()
    
    print("-" * 70)
    print()
    
    # Results
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(f"Computed Sum: {computed_sum}")
    print(f"Expected Sum: {expected_sum}")
    print(f"Verification: {'✓ PASSED' if computed_sum == expected_sum else '✗ FAILED'}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()


# ============================================================================
# Explanation: Reduction Clause in Parallel Programming
# ============================================================================
#
# REDUCTION CLAUSE:
# A reduction is a common parallel pattern where multiple threads/processes
# compute partial results that are then combined using an associative operator.
#
# In OpenMP (C/C++), this is expressed as:
#   #pragma omp parallel for reduction(+:sum)
#   for(i=0; i<n; i++)
#       sum += array[i];
#
# HOW IT WORKS:
# 1. Each worker gets a PRIVATE copy of the reduction variable (sum)
# 2. Each worker computes on its assigned portion of data
# 3. At the end, all private copies are combined using the reduction operator (+)
#
# REDUCTION OPERATORS:
# - Addition (+): sum, total
# - Multiplication (*): product
# - Logical AND (&&): all_true
# - Logical OR (||): any_true
# - Min/Max: finding extremes
#
# ADVANTAGES:
# - Avoids race conditions (each worker has private variable)
# - Automatic synchronization at reduction point
# - Clean, declarative syntax
# - Efficient parallel aggregation
#
# THIS IMPLEMENTATION:
# - Divides array into chunks
# - Each worker computes partial sum (private accumulator)
# - Master thread reduces all partials (implicit barrier + reduction)
# - Demonstrates scatter-compute-reduce pattern
