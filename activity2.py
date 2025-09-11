import multiprocessing as mp

N = 4

def compute_row(i, A, B):
    row = []
    for j in range(N):
        sum_val = 0
        for k in range(N):
            sum_val += A[i][k] * B[k][j]
        row.append(sum_val)
    return row

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

if __name__ == '__main__':
    A = [[i + j for j in range(N)] for i in range(N)]
    B = [[i - j for j in range(N)] for i in range(N)]
    
    print("Matrix A:")
    print_matrix(A)
    print("\nMatrix B:")
    print_matrix(B)
    
    with mp.Pool(processes=4) as pool:
        C = pool.starmap(compute_row, [(i, A, B) for i in range(N)])
    
    print("\nMatrix C (Result of A * B):")
    print_matrix(C)
