import threading
import time
import random
from mutex import RedisMutex, LockAcquisitionError


def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"

    try:
        with mutex.acquire(resource, wait_sec=15.0, retry_sec=0.5):
            time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
            with open(filename, 'a') as f:
                f.write(f"Thread {thread_id} wrote this line\n")
            print(f"[Thread {thread_id}] ✓ Done")
    except LockAcquisitionError:
        print(f"[Thread {thread_id}] X Unable to lock")
    finally:
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
