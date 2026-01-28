# Parallel Computing with Python

This repository, named "sockets", is a comprehensive collection of Python programs and exercises focused on parallel computing, distributed systems, networking, and high-performance computing concepts. Despite the name, it covers a wide range of topics beyond just socket programming, including multiprocessing, simulated MPI exercises, matrix operations, and parallel algorithms. The code is primarily written in Python and utilizes built-in modules like `multiprocessing`, `socket`, and `threading`, with some files using external libraries like `numpy`.

## Repository Structure

### Root Directory Files

#### Networking and Socket Programming
- **`server.py`**: Implements a multi-threaded TCP server that listens on localhost (127.0.0.1) at port 65432. The server can handle multiple clients concurrently, each in a separate thread. It receives length-prefixed messages from clients, processes them, and responds accordingly:
  - If the message is "hello", it sends a greeting.
  - Otherwise, it echoes the message back.
  This demonstrates basic client-server communication with threading for concurrency.

- **`client.py`**: A multi-threaded TCP client that connects to the server. It sends a list of predefined messages ("hello", "world", "test message") in parallel, each in its own thread. Messages are sent with a 3-digit zero-padded length prefix for proper parsing on the server side. This showcases concurrent client connections and basic protocol design.

#### Parallel Computation Examples
- **`matrix_multiplication.py`**: A program for performing parallel matrix multiplication using Python's `multiprocessing` module. It takes user input for matrix dimensions and elements, then computes the product by distributing row computations across multiple processes (up to 4). This illustrates parallelizing computationally intensive tasks and inter-process communication.

- **`simple_parallel_loop.py`**: Demonstrates parallel summation of squares from 0 to n-1 using a process pool. The range is divided into chunks and distributed across 4 processes. It measures and reports the time taken by each process, highlighting load balancing and parallel reduction.

- **`activity1.py`**: A basic multiprocessing example using a pool to execute a worker function across a range of values (0-8). Each process prints its name and the iteration it's handling, showing process creation and task distribution.

- **`activity2.py`**: Another matrix multiplication example, similar to the dedicated file but hardcoded with 4x4 matrices. It uses `starmap` to parallelize row-wise computation, demonstrating a simpler version of parallel matrix operations.

### Directories

#### **`clause_in_loop/`**
Contains programs exploring parallelism in loops, particularly focusing on handling clauses or conditions within parallel iterations.

#### **`lab_terminal/`**
Houses terminal-based lab exercises, likely for practicing command-line interactions and basic scripting in the context of parallel computing.

#### **`labmid/`**
Includes mid-term lab assignments, covering intermediate topics in the course curriculum.

#### **`mpi_exercises/`**
A set of exercises simulating MPI (Message Passing Interface) functionality using Python's `multiprocessing` module:
- **`q1_matrix_multiplication.py`**: Parallel matrix multiplication where the matrix is divided by rows and distributed across processes. Each process computes a submatrix and sends results back via a queue, mimicking MPI's scatter and gather operations.
- **`q2_array_sum_16.py`**: Parallel array summation of 16 elements across 6 processes. Demonstrates distributing work unevenly (some processes get more elements) and combining partial sums.
- **`q3_array_sum_12.py`**: Similar to q2, but with 12 elements and 4 processes, showing even distribution (3 elements each) and parallel reduction.

#### **`mpi_lab_tasks/`**
Contains lab tasks specifically related to MPI concepts, providing practical exercises for understanding distributed computing paradigms.

#### **`parallelism/`**
A general directory for various parallelism examples and demonstrations, covering different aspects of concurrent and parallel programming.

## Key Concepts Demonstrated

1. **Multiprocessing**: Extensive use of Python's `multiprocessing` module for parallel execution, including process pools, queues, and shared memory concepts.

2. **Threading**: Multi-threaded server and client implementations for handling concurrent connections and requests.

3. **Socket Programming**: TCP client-server architecture with custom protocol design (length-prefixed messages).

4. **Parallel Algorithms**: Matrix multiplication, array summation, and loop parallelization techniques.

5. **Simulated MPI**: Exercises that replicate MPI patterns using multiprocessing, including work distribution and result collection.

6. **Load Balancing**: Division of work across processes, handling uneven distributions.

7. **Inter-Process Communication**: Using queues and shared data structures for communication between processes.

## Requirements

- Python 3.x
- Built-in modules: `multiprocessing`, `socket`, `threading`
- External libraries: `numpy` (for some matrix operations)

## Usage

Most programs can be run directly with `python filename.py`. Some require user input for matrix sizes and elements. For networking examples, run the server first in one terminal, then the client in another.

## Educational Purpose

This repository appears to be part of a computer science or parallel computing course, providing hands-on examples and exercises for learning parallel programming concepts, from basic multiprocessing to advanced distributed computing patterns.
