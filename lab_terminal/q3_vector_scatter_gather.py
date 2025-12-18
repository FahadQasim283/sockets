import multiprocessing as mp
import time

def compute_partial_sum(rank, sub_vector, result_queue):
    """
    Compute sum of a sub-vector.
    
    Args:
        rank: Process rank (node id)
        sub_vector: Sub-vector assigned to this process
        result_queue: Queue to send result back to root
    """
    partial_sum = sum(sub_vector)
    result_queue.put((rank, partial_sum))
    return partial_sum


def scatter_vector(vector, num_processes):
    """
    Break up vector into sub-vectors of equal length and distribute to processes.
    
    Args:
        vector: The long vector to be distributed
        num_processes: Number of processes to distribute to
    
    Returns:
        list: List of sub-vectors for each process
    """
    vector_length = len(vector)
    sub_vector_length = vector_length // num_processes
    
    sub_vectors = []
    for i in range(num_processes):
        start = i * sub_vector_length
        # Last process gets any remaining elements
        end = (i + 1) * sub_vector_length if i < num_processes - 1 else vector_length
        sub_vectors.append(vector[start:end])
    
    return sub_vectors


def gather_and_reduce(result_queue, num_processes):
    """
    Gather partial sums from all processes and reduce (add) at root node.
    
    Args:
        result_queue: Queue containing partial results from processes
        num_processes: Number of processes to gather from
    
    Returns:
        tuple: (total_sum, list of partial results)
    """
    partial_results = []
    
    # Gather phase: Collect all partial sums
    for _ in range(num_processes):
        rank, partial_sum = result_queue.get()
        partial_results.append((rank, partial_sum))
    
    # Sort by rank for organized display
    partial_results.sort()
    
    # Reduce phase: Add all partial sums at root node
    total_sum = sum(partial_sum for _, partial_sum in partial_results)
    
    return total_sum, partial_results


def main():
    """Main function demonstrating scatter-gather with collective operations."""
    
    # Configuration
    vector_size = 100
    num_processes = 4
    
    # Create a long vector
    vector = list(range(1, vector_size + 1))  # [1, 2, 3, ..., 100]
    expected_sum = sum(vector)
    
    print("=" * 70)
    print("VECTOR SUM USING SCATTER-GATHER WITH COLLECTIVE OPERATIONS")
    print("=" * 70)
    print(f"Vector size: {vector_size}")
    print(f"Vector: [1, 2, 3, ..., {vector_size}]")
    print(f"Number of processes: {num_processes}")
    print(f"Expected sum: {expected_sum}")
    print("=" * 70)
    print()
    
    # Step 1: SCATTER - Break vector into sub-vectors
    print("STEP 1: SCATTER - Distribute sub-vectors to processes")
    print("-" * 70)
    sub_vectors = scatter_vector(vector, num_processes)
    for i, sub_vec in enumerate(sub_vectors):
        if len(sub_vec) <= 10:
            print(f"  Process {i}: {sub_vec}")
        else:
            print(f"  Process {i}: [{sub_vec[0]}, {sub_vec[1]}, ..., {sub_vec[-1]}] (length: {len(sub_vec)})")
    print()
    
    # Step 2: COMPUTE - Each process computes partial sum
    print("STEP 2: COMPUTE - Parallel computation of partial sums")
    print("-" * 70)
    
    result_queue = mp.Queue()
    processes = []
    
    start_time = time.time()
    
    # Start all processes with their sub-vectors
    for rank, sub_vector in enumerate(sub_vectors):
        p = mp.Process(target=compute_partial_sum, args=(rank, sub_vector, result_queue))
        p.start()
        processes.append(p)
    
    # Step 3: GATHER and REDUCE - Collect partial sums at root and add them
    print()
    print("STEP 3: GATHER & REDUCE - Collect and sum at root node")
    print("-" * 70)
    
    total_sum, partial_results = gather_and_reduce(result_queue, num_processes)
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Display gathered results
    for rank, partial_sum in partial_results:
        print(f"  Process {rank} -> Partial sum: {partial_sum}")
    
    print(f"\nReduction: {' + '.join(str(ps) for _, ps in partial_results)} = {total_sum}")
    
    # Final results
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(f"Total Sum (computed): {total_sum}")
    print(f"Expected Sum: {expected_sum}")
    print(f"Verification: {'✓ PASSED' if total_sum == expected_sum else '✗ FAILED'}")
    print(f"Execution Time: {execution_time:.6f} seconds")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()


# ============================================================================
# Explanation: Scatter-Gather with Collective Operations
# ============================================================================
#
# This program demonstrates the scatter-gather-reduce pattern commonly used
# in parallel computing and MPI (Message Passing Interface).
#
# THREE MAIN OPERATIONS:
#
# 1. SCATTER (Distribution Phase):
#    - Root node has a long vector
#    - Vector is divided into sub-vectors of equal (or nearly equal) length
#    - Each sub-vector is distributed to a different process
#    - Example: [1,2,3,4,5,6,7,8] with 4 processes
#      Process 0 gets [1,2], Process 1 gets [3,4],
#      Process 2 gets [5,6], Process 3 gets [7,8]
#
# 2. COMPUTE (Parallel Processing Phase):
#    - Each process independently computes the sum of its sub-vector
#    - All processes work in parallel
#    - Example: Process 0 computes 1+2=3, Process 1 computes 3+4=7, etc.
#
# 3. GATHER and REDUCE (Collection and Aggregation Phase):
#    - Root node collects partial sums from all processes (GATHER)
#    - Root node adds all partial sums together (REDUCE)
#    - Example: Root adds 3 + 7 + 11 + 15 = 36
#
# COLLECTIVE OPERATIONS:
# - Scatter: One-to-many distribution
# - Gather: Many-to-one collection
# - Reduce: Combine gathered data using an operation (addition in this case)
#
# This pattern is efficient for processing large datasets in parallel
# across distributed computing systems.
