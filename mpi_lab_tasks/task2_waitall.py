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
        futures = [executor.submit(simulate_work, task_id, duration) for task_id, duration in tasks]

        print("All tasks submitted. Now waiting for all to complete (MPI_Waitall simulation)...")

        # Wait for all futures to complete (equivalent to MPI_Waitall)
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    print("All tasks completed.")
    print("Results:", results)

if __name__ == "__main__":
    main()

# Explanation of Task 2 (MPI_Waitall):
# This program demonstrates the concept of MPI_Waitall, which waits for all asynchronous operations to complete.
# In MPI, MPI_Waitall waits for all requests in a list to complete.
# Here, we simulate asynchronous operations using Python's concurrent.futures.ThreadPoolExecutor.
# Multiple tasks are submitted asynchronously, and then we wait for all of them to complete using as_completed() in a loop.
# This ensures that the program doesn't proceed until every single asynchronous operation has finished.
# The output shows the order of completion, which may differ from submission order due to different task durations.