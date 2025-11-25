import multiprocessing as mp
import time
import concurrent.futures

def simulate_work(task_id, duration):
    """Simulate some work that takes 'duration' seconds."""
    print(f"Task {task_id} started")
    time.sleep(duration)
    result = f"Result from task {task_id}"
    print(f"Task {task_id} completed")
    return result

def main():
    # Simulate multiple asynchronous operations
    tasks = [
        (1, 2.0),  # task_id, duration
        (2, 1.5),
        (3, 3.0),
        (4, 0.5)
    ]

    print("Starting asynchronous tasks...")

    # Use ThreadPoolExecutor to simulate asynchronous operations
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        # Submit all tasks
        futures = {executor.submit(simulate_work, task_id, duration): (task_id, duration) for task_id, duration in tasks}

        print("All tasks submitted. Now waiting for any to complete (MPI_Waitany simulation)...")

        # Wait for any future to complete (equivalent to MPI_Waitany)
        completed_results = []
        while futures:
            # Wait for the next completed future
            completed_future = next(concurrent.futures.as_completed(futures.keys()))
            task_info = futures.pop(completed_future)
            result = completed_future.result()
            completed_results.append((task_info[0], result))
            print(f"Received result from task {task_info[0]}: {result}")

    print("All tasks completed.")
    print("Final results:", completed_results)

if __name__ == "__main__":
    main()

# Explanation of Task 2 (MPI_Waitany):
# This program demonstrates the concept of MPI_Waitany, which waits for any one asynchronous operation to complete.
# In MPI, MPI_Waitany waits for any request in a list to complete and returns the index of the completed request.
# Here, we simulate asynchronous operations using Python's concurrent.futures.ThreadPoolExecutor.
# Multiple tasks are submitted asynchronously, and then we use next(as_completed()) to wait for and process the next completed task.
# This allows the program to handle completed operations as they finish, rather than waiting for all.
# The output shows the order in which tasks complete, demonstrating how MPI_Waitany can be used for dynamic load balancing or responsive handling of asynchronous operations.