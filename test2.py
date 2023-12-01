import queue
import threading

# Create a shared queue
shared_queue = queue.Queue()

# Function to be executed by multiple threads
def worker_thread():
    while True:
        item = shared_queue.get()  # Retrieve an item from the queue
        # Process the item...
        print(f"Processed: {item}")
        shared_queue.task_done()  # Mark the item as processed

# Create and start multiple threads
num_threads = 4
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker_thread)
    thread.start()
    threads.append(thread)

# Add data to the shared queue
for i in range(10):
    shared_queue.put(i)  # Put items into the queue

# Wait for all threads to finish
for thread in threads:
    thread.join()

# All items have been processed