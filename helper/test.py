"""
图片文件存储在images文件夹下

并把md文件的
"""
import re
import os
import shutil
import argparse
parser = argparse.ArgumentParser()

# 文件路径参数，默认是当前文件夹下
parser.add_argument("path", type=str, default=".", help="要处理的文件夹的路径")
args = parser.parse_args()


if __name__ == "__main__":
    for root, dirs, files in os.walk(args.path):
        # move_markdown_used_imgs(root)

        img_dir = os.path.join(root, 'images')

        # img文件夹查看
        if os.path.isdir(img_dir):
            print(img_dir)
            if len(os.listdir(img_dir)) == 0:
                print(img_dir, len(os.listdir(img_dir)))
                # os.removedirs(img_dir)
            # os.remove(img_dir)