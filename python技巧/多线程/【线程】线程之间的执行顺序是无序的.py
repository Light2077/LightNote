import threading
import time

def task():
    # 获取当前线程的线程对象
    thread = threading.current_thread()
    time.sleep(1)
    print(thread)

if __name__ == '__main__':
    for i in range(5):
        sub_thread = threading.Thread(target=task)
        sub_thread.start()
