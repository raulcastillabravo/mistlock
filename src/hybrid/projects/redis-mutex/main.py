import threading
import time
import random
from mutex import RedisMutex


def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"
    lock_acquired = False

    try:
        if not mutex.lock(resource, wait_sec=15.0, retry_sec=0.5):
            print(f"[Thread {thread_id}] X Unable to lock")
            return
        
        lock_acquired = True
        time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
        with open(filename, 'a') as f:
            f.write(f"Thread {thread_id} wrote this line\n")
        print(f"[Thread {thread_id}] ✓ Done")
    finally:
        if lock_acquired:
            mutex.unlock(resource)
        mutex.close()

def main():
    threads = []
    
    for i in range(5):
        thread = threading.Thread(target=write_to_file, args=[i + 1])
        threads.append(thread)
        thread.start() 
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
