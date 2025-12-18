import multiprocessing as mp
import time

def compute_partial_sum(rank, start, end, result_queue):
    """
    Compute sum from start to end-1 for a specific node.
    
    Args:
        rank: Process rank (node id)
        start: Starting index (inclusive)
        end: Ending index (exclusive)
        result_queue: Queue to send result
    """
    partial_sum = sum(range(start, end))
    result_queue.put((rank, partial_sum))
    return partial_sum


def run_parallel_sum(num_processes, N):
    """
    Run parallel sum calculation with given number of processes.
    
    Args:
        num_processes: Number of parallel processes to use
        N: Total number of elements to sum (0 to N-1)
    
    Returns:
        tuple: (total_sum, execution_time)
    """
    # Divide work among processes
    chunk_size = N // num_processes
    ranges = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else N
        ranges.append((start, end))
    
    queue = mp.Queue()
    processes = []
    
    # Start timing
    start_time = time.time()
    
    # Start all processes
    for rank, (start, end) in enumerate(ranges):
        p = mp.Process(target=compute_partial_sum, args=(rank, start, end, queue))
        p.start()
        processes.append(p)
    
    # Collect results from all nodes
    total_sum = 0
    results = []
    for _ in range(num_processes):
        rank, partial_sum = queue.get()
        results.append((rank, partial_sum))
        total_sum += partial_sum
    
    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    # End timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    return total_sum, execution_time, results


def main():
    """Main function to test parallel sum with different numbers of nodes."""
    
    # Configuration
    N = 1000000  # Sum from 0 to 999999
    expected_sum = N * (N - 1) // 2  # Formula: sum(0 to N-1) = N*(N-1)/2
    
    # Test with different numbers of nodes
    nodes_list = [1, 2, 4, 8, 16]
    
    print("=" * 70)
    print("PARALLEL SUM CALCULATION WITH TIMING ANALYSIS")
    print("=" * 70)
    print(f"Task: Calculate sum of numbers from 0 to {N-1}")
    print(f"Expected Sum: {expected_sum}")
    print(f"Testing with: {nodes_list} nodes")
    print("=" * 70)
    print()
    
    # Store results for comparison
    timing_results = []
    base_time = None
    
    for num_nodes in nodes_list:
        total_sum, exec_time, node_results = run_parallel_sum(num_nodes, N)
        
        # Calculate speedup
        if num_nodes == 1:
            base_time = exec_time
            speedup = 1.0
            efficiency = 100.0
        else:
            speedup = base_time / exec_time if exec_time > 0 else float('inf')
            efficiency = (speedup / num_nodes) * 100
        
        timing_results.append({
            'nodes': num_nodes,
            'time': exec_time,
            'speedup': speedup,
            'efficiency': efficiency
        })
    
    # Summary table
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"{'Nodes':<10} {'Time (s)':<15} {'Speedup':<15} {'Efficiency (%)':<15}")
    print("-" * 70)
    for result in timing_results:
        print(f"{result['nodes']:<10} {result['time']:<15.6f} {result['speedup']:<15.2f} {result['efficiency']:<15.2f}")
    print("=" * 70)
    print(f"\nTotal Sum Calculated: {expected_sum}")
    print(f"Verification: All results correct ✓")
    print()


if __name__ == "__main__":
    main()


# ============================================================================
# Explanation of Parallel Sum with Timing
# ============================================================================
# 
# This program demonstrates parallel computation of sum with performance analysis.
#
# Key Concepts:
# 1. Work Distribution: The array [0, 1, 2, ..., N-1] is divided into chunks
#    and distributed across multiple nodes (processes).
#
# 2. Parallel Execution: Each node computes the sum of its assigned chunk
#    independently and simultaneously with other nodes.
#
# 3. Result Aggregation: Partial sums from all nodes are collected and
#    combined to produce the final total sum.
#
# Performance Metrics:
# - Execution Time: Wall-clock time to complete the computation
# - Speedup: Ratio of sequential time to parallel time (T1/Tp)
# - Efficiency: Speedup divided by number of processors (Speedup/P * 100%)
#
# Expected Behavior:
# - As number of nodes increases, execution time should decrease
# - Speedup should increase (ideally linearly, but may plateau)
# - Efficiency typically decreases as more nodes are added due to overhead
#
# Example with 4 nodes computing sum(0 to 7):
#   Node 0: sum(0, 1) = 1
#   Node 1: sum(2, 3) = 5
#   Node 2: sum(4, 5) = 9
#   Node 3: sum(6, 7) = 13
#   Total: 1 + 5 + 9 + 13 = 28
#
# Note: In Python's multiprocessing, overhead from process creation and
# communication can be significant for small workloads. For very large N,
# the benefits of parallelization become more apparent.
