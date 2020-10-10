import time
import threading

def work():
    for i in range(10):
        print('working...')
        time.sleep(0.2)
    print('finish work.')
if __name__ == '__main__':
    work_thread = threading.Thread(target=work)
    work_thread.start()
    
    time.sleep(1)
    print('主线程执行完毕！')
