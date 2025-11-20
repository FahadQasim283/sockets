import multiprocessing as mp
import numpy as np

def multiply_submatrix(A, B, start_row, end_row, queue):
    """Multiply submatrix from start_row to end_row."""
    C_sub = np.dot(A[start_row:end_row], B)
    queue.put((start_row, end_row, C_sub))

def main():
    # Define matrices
    n = 4  # Small size for demo
    A = np.random.randint(0, 5, (n, n))
    B = np.random.randint(0, 5, (n, n))

    print("Matrix A:")
    print(A)
    print("Matrix B:")
    print(B)

    num_processes = 2  # Simulate 2 processes
    rows_per_process = n // num_processes
    processes = []
    queue = mp.Queue()

    # Start processes
    for i in range(num_processes):
        start_row = i * rows_per_process
        end_row = (i + 1) * rows_per_process if i < num_processes - 1 else n
        p = mp.Process(target=multiply_submatrix, args=(A, B, start_row, end_row, queue))
        p.start()
        processes.append(p)

    # Gather results
    C = np.zeros((n, n))
    for _ in range(num_processes):
        start_row, end_row, C_sub = queue.get()
        C[start_row:end_row] = C_sub

    # Join processes
    for p in processes:
        p.join()

    print("Result Matrix C:")
    print(C)
    print("Verification (A @ B):")
    print(A @ B)
    print("Match:", np.allclose(C, A @ B))

if __name__ == "__main__":
    main()

# Explanation of Q1:
# This program implements parallel matrix multiplication using multiprocessing in Python.
# Each process (simulating an MPI process) computes a submatrix multiplication.
# The matrices are divided by rows: each process gets a portion of rows from matrix A.
# They compute A_sub * B and put the result in a queue.
# The main process gathers all submatrices to form the complete result matrix C.
# This demonstrates distributing work across processes and gathering results on process zero (main process).