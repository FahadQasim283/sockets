import multiprocessing as mp
from multiprocessing import Pipe
import time

# Fixed message size constraint
FIXED_MESSAGE_SIZE = 16  # 16 octets (bytes)


def pad_message(message):
    """
    Pad or truncate message to exactly 16 characters.
    
    Args:
        message: Input message string
    
    Returns:
        str: Message exactly 16 characters long
    """
    if len(message) > FIXED_MESSAGE_SIZE:
        # Truncate if too long
        return message[:FIXED_MESSAGE_SIZE]
    else:
        # Pad with spaces if too short
        return message.ljust(FIXED_MESSAGE_SIZE)


def sender_process(rank, pipe_send, message):
    """
    Sender process that sends fixed-size messages.
    
    Args:
        rank: Process rank/ID
        pipe_send: Pipe connection for sending
        message: Message to send
    """
    # Ensure message is exactly 16 characters
    fixed_message = pad_message(message)
    message_bytes = fixed_message.encode('utf-8')
    
    print(f"Sender {rank}:")
    print(f"  Original: '{message}' ({len(message)} chars)")
    print(f"  Fixed:    '{fixed_message}' ({len(fixed_message)} chars)")
    print(f"  Bytes:    {len(message_bytes)} octets")
    
    # Send the fixed-size message
    pipe_send.send(message_bytes)
    print(f"  Status:   ✓ Sent\n")


def receiver_process(rank, pipe_recv):
    """
    Receiver process that receives fixed-size messages.
    
    Args:
        rank: Process rank/ID
        pipe_recv: Pipe connection for receiving
    """
    # Receive the fixed-size message
    message_bytes = pipe_recv.recv()
    
    # Decode and validate
    message = message_bytes.decode('utf-8')
    
    print(f"Receiver {rank}:")
    print(f"  Received: '{message}' ({len(message)} chars)")
    print(f"  Bytes:    {len(message_bytes)} octets")
    
    # Validate message size
    if len(message_bytes) == FIXED_MESSAGE_SIZE:
        print(f"  Status:   ✓ Valid (exactly {FIXED_MESSAGE_SIZE} octets)\n")
    else:
        print(f"  Status:   ✗ Invalid (expected {FIXED_MESSAGE_SIZE}, got {len(message_bytes)})\n")


def main():
    """Main function demonstrating fixed-size message passing."""
    
    print("=" * 70)
    print("FIXED-SIZE MESSAGE PASSING (16 OCTETS)")
    print("=" * 70)
    print(f"Constraint: All messages must be exactly {FIXED_MESSAGE_SIZE} characters\n")
    
    # Test messages of various lengths
    test_messages = [
        "Hello",                  # Too short (5 chars)
        "Hello World!",           # Too short (12 chars)
        "Message16chars!",        # Exact (16 chars)
        "This is too long message"  # Too long (24 chars)
    ]
    
    print("TEST CASES:")
    print("-" * 70)
    
    for i, msg in enumerate(test_messages):
        print(f"\nTest Case {i + 1}:")
        print("-" * 70)
        
        # Create pipe for communication
        recv_conn, send_conn = Pipe(duplex=False)
        
        # Create sender and receiver processes
        sender = mp.Process(target=sender_process, args=(i, send_conn, msg))
        receiver = mp.Process(target=receiver_process, args=(i, recv_conn))
        
        # Start processes
        sender.start()
        time.sleep(0.1)  # Small delay for clean output
        receiver.start()
        
        # Wait for completion
        sender.join()
        receiver.join()
        
        # Close connections
        send_conn.close()
        recv_conn.close()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ All messages standardized to {FIXED_MESSAGE_SIZE} octets")
    print(f"✓ Short messages padded with spaces")
    print(f"✓ Long messages truncated")
    print(f"✓ Ensures fixed-size communication protocol")
    print("=" * 70)


if __name__ == "__main__":
    main()


# ============================================================================
# Explanation: Fixed-Size Message Passing
# ============================================================================
#
# PROBLEM:
# In parallel/distributed systems, sometimes we need messages to be a fixed
# size (16 octets/bytes in this case) for:
# - Predictable memory allocation
# - Simplified buffer management
# - Consistent network packet sizes
# - Hardware constraints (some systems require fixed-size messages)
#
# SOLUTION APPROACH:
# 1. If message < 16 chars: Pad with spaces to reach 16 chars
# 2. If message = 16 chars: Send as-is
# 3. If message > 16 chars: Truncate to 16 chars
#
# REAL-WORLD APPLICATIONS:
# - MPI (Message Passing Interface) fixed-size message buffers
# - Network protocols with fixed packet sizes
# - Embedded systems with limited memory
# - RDMA (Remote Direct Memory Access) communication
# - GPU communication buffers
#
# CHARACTERISTICS OF MESSAGE PASSING APIs:
# 1. Send/Receive operations (point-to-point communication)
# 2. Message size specification (fixed or variable)
# 3. Blocking vs Non-blocking operations
# 4. Process identification (rank/ID)
# 5. Data type specification
# 6. Error handling
# 7. Synchronization primitives
# 8. Collective operations (broadcast, gather, scatter, reduce)
#
# PARALLEL PROGRAMMING MODELS:
# 1. Message Passing (MPI) - Explicit communication
# 2. Shared Memory (OpenMP) - Implicit communication via shared variables
# 3. Data Parallel (CUDA, OpenCL) - Same operation on multiple data
# 4. Task Parallel - Different operations executed concurrently
