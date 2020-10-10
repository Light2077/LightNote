import time
import multiprocessing

def work():
    for i in range(10):
        print('working...')
        time.sleep(0.2)
    print('finish work.')

if __name__ == '__main__':
    
    work_process = multiprocessing.Process(target=work)
    work_process.start()
    
    time.sleep(1)
    print('主进程执行完毕！')
