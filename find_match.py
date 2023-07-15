import hashlib
import threading

from tqdm import tqdm

# Global variable to track the match status
match_found = False

# Lock for synchronizing access to the match status variable
match_lock = threading.Lock()
    
def check_hash(phone_number, target_hash):
    global match_found

    number_hash = hashlib.sha256(str(phone_number).encode()).hexdigest()
    if number_hash == target_hash:
        with match_lock:
            match_found = True
        print(f"\n\nFound a match! Phone number: {phone_number} \n\n")
        exit(0)

def search_phone_numbers(start, end, target_hash):
    global match_found

    for phone_number in tqdm(range(start, end - 1, -1)):
        with match_lock:
            if match_found:
                return
        check_hash(phone_number, target_hash)

# Function to distribute workload across threads
def distribute_workload(start, end, target_hash, num_threads):
    total_range = end - start + 1
    range_per_thread = total_range // num_threads
    threads = []

    for i in range(num_threads):
        thread_start = start + i * range_per_thread
        thread_end = thread_start + range_per_thread - 1
        if i == num_threads - 1:
            thread_end = end

        thread = threading.Thread(target=search_phone_numbers, args=(thread_start, thread_end, target_hash))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    target_hash = "e2d8bba6e47dbe71a56f19804dfbf4deff910004001080ff910004001180ffd9"

    num_threads = 10
    start_number = 9999999999
    end_number = 7000000000

    distribute_workload(start_number, end_number, target_hash, num_threads)
    
    if not match_found: print("No match found.")
