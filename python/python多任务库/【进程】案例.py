import os
import time
import shutil
import multiprocessing


def copy_work(file_name, src_dir, dst_dir):
	# 拼接路径
    src_path = os.path.join(src_dir, file_name)
    dst_path = os.path.join(dst_dir, file_name)
    
    print(src_path, '---->', dst_path)
    start = time.time()
    # 拷贝文件夹时
    shutil.copytree(src_path, dst_path)

    # 拷贝单个文件时
    # with open(src_path, 'rb') as src_file:
    #     with open(dst_path, 'wb') as dst_file:
    #         while True:
    #             data = src_file.read(1024)
    #             if data:
    #                 dst_file.write(data)
    #             else:
    #                 break
    print(src_path, '耗费时间 %.2f' % (time.time() - start))

if __name__ == '__main__':
    src_dir = 'python教学视频'
    dst_dir = 'C:/Users/Light/Desktop/test'

    # 1.判断目标文件夹是否存在，不存在则创建
    try:
        os.mkdir(dst_dir)

    except FileExistsError:
        print('目标文件夹已经存在，未创建')

    # 2读取文件信息

    for file_name in os.listdir(src_dir):
        sub_process = multiprocessing.Process(target=copy_work,
                                              args=(file_name, src_dir, dst_dir))
        sub_process.start()
    

# 单任务耗费时间
# start = time.time()
# for file_name in os.listdir(src_dir):
#     # copy_work(file, src_dir, dst_dir)  # 单任务拷贝
#     copy_work(file_name, src_dir, dst_dir)
# print('time consume %.2f s' % (time.time() - start))