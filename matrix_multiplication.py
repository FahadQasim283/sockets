import multiprocessing as mp

def compute_row(i, A, B, cols_A, cols_B):
    row = []
    for j in range(cols_B):
        sum_val = 0
        for k in range(cols_A):
            sum_val += A[i][k] * B[k][j]
        row.append(sum_val)
    return row

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

if __name__ == '__main__':
    while True:
        try:
            rows_A = int(input("Enter rows for matrix A: "))
            cols_A = int(input("Enter columns for matrix A: "))
            rows_B = int(input("Enter rows for matrix B: "))
            cols_B = int(input("Enter columns for matrix B: "))
            
            if cols_A != rows_B:
                print("Error: Columns of A must equal rows of B for multiplication.")
                retry = input("Do you want to re-enter? (y/n): ")
                if retry.lower() != 'y':
                    break
                continue
            
            # Input matrix A
            A = []
            print("Enter elements for matrix A:")
            for i in range(rows_A):
                while True:
                    row_input = input(f"Enter row {i+1} ({cols_A} integers separated by space): ")
                    row = list(map(int, row_input.split()))
                    if len(row) == cols_A:
                        A.append(row)
                        break
                    else:
                        print(f"Error: Row must have exactly {cols_A} elements.")
            
            # Input matrix B
            B = []
            print("Enter elements for matrix B:")
            for i in range(rows_B):
                while True:
                    row_input = input(f"Enter row {i+1} ({cols_B} integers separated by space): ")
                    row = list(map(int, row_input.split()))
                    if len(row) == cols_B:
                        B.append(row)
                        break
                    else:
                        print(f"Error: Row must have exactly {cols_B} elements.")
            
            # Compute C
            num_processes = min(4, rows_A)
            with mp.Pool(processes=num_processes) as pool:
                C = pool.starmap(compute_row, [(i, A, B, cols_A, cols_B) for i in range(rows_A)])
            
            # Print matrices
            print("\nMatrix A:")
            print_matrix(A)
            print("\nMatrix B:")
            print_matrix(B)
            print("\nMatrix C (Result of A * B):")
            print_matrix(C)
            break
        
        except ValueError:
            print("Invalid input. Please enter integers only.")
            retry = input("Do you want to try again? (y/n): ")
            if retry.lower() != 'y':
                break
