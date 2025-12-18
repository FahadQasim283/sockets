import multiprocessing as mp
import time

def prefix_sum_node(rank, num_processes, recv_conn, send_conn, result_queue):
    """
    Each node computes prefix sum sequentially.
    
    Args:
        rank: Current process rank (node id)
        num_processes: Total number of processes
        recv_conn: Connection to receive from previous node
        send_conn: Connection to send to next node
        result_queue: Queue to send final result
    """
    # Initialize variables
    a = rank  # Initially a = node id
    b = 0     # Variable to receive value from previous node
    
    print(f"Node {rank}: Initial value a = {a}")
    
    # If not the first node, receive from previous node
    if rank > 0:
        b = recv_conn.recv()
        print(f"Node {rank}: Received b = {b} from Node {rank-1}")
    
    # Calculate prefix sum: sum of all values from 0 to current rank
    prefix_sum = a + b
    print(f"Node {rank}: Calculated prefix_sum = a + b = {a} + {b} = {prefix_sum}")
    
    # If not the last node, send to next node
    if rank < num_processes - 1:
        send_conn.send(prefix_sum)
        print(f"Node {rank}: Sent prefix_sum = {prefix_sum} to Node {rank+1}")
    
    print(f"Node {rank}: Final prefix sum = {prefix_sum}")
    result_queue.put((rank, prefix_sum))


def main():
    """Main function to set up processes and connections for prefix sum."""
    n = 8  # Number of processes (can be changed)
    
    print("=" * 60)
    print(f"Prefix Sum Calculation with {n} processes")
    print("=" * 60)
    print(f"Each node i starts with a = i (node id)")
    print(f"Computing prefix sum: S[i] = sum(a[0] to a[i])")
    print("=" * 60)
    print()
    
    # Create pipes for communication between consecutive nodes
    # Node i receives from node i-1 and sends to node i+1
    pipes = []
    for i in range(n - 1):
        recv_conn, send_conn = mp.Pipe(duplex=False)
        pipes.append((recv_conn, send_conn))
    
    # Create result queue
    result_queue = mp.Queue()
    
    # Start all processes
    processes = []
    for rank in range(n):
        # Determine connections for this node
        recv_conn = pipes[rank - 1][0] if rank > 0 else None
        send_conn = pipes[rank][1] if rank < n - 1 else None
        
        p = mp.Process(target=prefix_sum_node, args=(rank, n, recv_conn, send_conn, result_queue))
        p.start()
        processes.append(p)
    
    # Collect results
    results = []
    for _ in range(n):
        results.append(result_queue.get())
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    # Sort and display results
    results.sort()
    print()
    print("=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    for rank, prefix_sum in results:
        expected = sum(range(rank + 1))
        status = "✓" if prefix_sum == expected else "✗"
        print(f"Node {rank}: Prefix Sum = {prefix_sum}, Expected = {expected} {status}")
    print("=" * 60)
    
    # Verify correctness
    all_correct = all(prefix_sum == sum(range(rank + 1)) for rank, prefix_sum in results)
    print(f"\nVerification: {'PASSED ✓' if all_correct else 'FAILED ✗'}")
    print()


if __name__ == "__main__":
    main()


# Explanation of Prefix Sum Algorithm:
# 
# Prefix sum (also called scan) computes cumulative sums:
# Given: a[0], a[1], a[2], a[3], ...
# Compute: S[0] = a[0]
#          S[1] = a[0] + a[1]
#          S[2] = a[0] + a[1] + a[2]
#          S[3] = a[0] + a[1] + a[2] + a[3]
#          ...
#
# In this program:
# - Each node i starts with a = i (node id)
# - So we compute prefix sum of [0, 1, 2, 3, ...]
# - Expected results: [0, 1, 3, 6, ...]
#
# Algorithm: Parallel Doubling (Upward Sweep)
# - In step d = 1, 2, 4, 8, ...
# - Process i receives from process i-d (if exists)
# - Process i adds received value to its prefix_sum
# - Process i sends its prefix_sum to process i+d (if exists)
#
# Example with 4 processes (n=4):
# Initial: Node 0: a=0, Node 1: a=1, Node 2: a=2, Node 3: a=3
#
# ============================================================================
# Explanation of Prefix Sum Algorithm:
# ============================================================================
# 
# Prefix sum (also called scan or cumulative sum) computes running totals:
# 
# Given: a[0], a[1], a[2], a[3], ...
# Compute: S[0] = a[0]
#          S[1] = a[0] + a[1]
#          S[2] = a[0] + a[1] + a[2]
#          S[3] = a[0] + a[1] + a[2] + a[3]
#          ...
#
# In this program:
# - Each node i starts with a = i (node id)
# - So we compute prefix sum of [0, 1, 2, 3, 4, 5, 6, 7]
# - Expected results: [0, 1, 3, 6, 10, 15, 21, 28]
#
# ============================================================================
# Algorithm: Sequential Prefix Sum with Message Passing
# ============================================================================
# 
# 1. Each node i has:
#    - Variable 'a' initialized to its rank (node id)
#    - Variable 'b' to receive cumulative sum from previous node
#
# 2. Communication pattern:
#    - Node 0: Doesn't receive (first node), computes S[0] = a = 0
#    - Node i (i>0): Receives 'b' from Node i-1, computes S[i] = a + b
#    - Node i (i<n-1): Sends its prefix sum to Node i+1
#
# 3. Example with 4 nodes:
#    Node 0: a=0, b=0 (no receive), S[0]=0+0=0, sends 0 to Node 1
#    Node 1: a=1, receives b=0, S[1]=1+0=1, sends 1 to Node 2  
#    Node 2: a=2, receives b=1, S[2]=2+1=3, sends 3 to Node 3
#    Node 3: a=3, receives b=3, S[3]=3+3=6 (no send, last node)
#
# Time Complexity: O(n) - sequential but demonstrates message passing
# Space Complexity: O(1) per node
# 
# Note: This is a simple linear scan. For better performance with many nodes,
# parallel algorithms like doubling or tree-based scans can be used