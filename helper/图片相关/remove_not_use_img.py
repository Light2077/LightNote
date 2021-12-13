import os
import re

import glob
import argparse
parser = argparse.ArgumentParser()

# 文件路径参数，默认是当前文件夹下
parser.add_argument("path", type=str, default=".", help="要处理的文件夹的路径")
parser.add_argument("-d", "--image_dir_name", dest="image_dir_name", type=str, 
                    default="images", help="图片文件夹的名称")

parser.add_argument("-r", dest="recursive", type=bool, default=False, help="是否递归子文件夹")
args = parser.parse_args()


# 提取当前目录下images / img文件夹内的所有图片
def get_image_paths(dir_path):
    img_dir = os.path.join(dir_path, args.image_dir_name)
    img_paths = glob.glob(os.path.join(img_dir, '*.png')) + glob.glob(os.path.join(img_dir, '*.jpg'))

    return img_paths
    

# 获取当前目录下所有markdownh中用到的图片路径
def get_markdown_used_image_path(dir_path):
    markdown_paths = glob.glob(os.path.join(dir_path, '*.md'))
    used_img_paths = set()
    for markdown_path in markdown_paths:
        with open(markdown_path, 'r', encoding='utf8') as f:

            text = f.read()
            img_names = re.findall(r'\!\[.*?\]\((.*?)\)', text)
            # imgs = re.findall(r'img/(.*?)\)', text)
            img_names = set([os.path.normpath(os.path.join(dir_path, img_name)) for img_name in img_names])
            used_img_paths.update(set(img_names))
    return used_img_paths


def remove_not_use_images(dir_path):
    img_paths = get_image_paths(dir_path)
    used_img_paths = get_markdown_used_image_path(dir_path)
    for img_path in img_paths:
        if img_path not in used_img_paths:
            print("remove", img_path)
            # os.remove(img_path)

if __name__ == "__main__":
    for root, dirs, files in os.walk(args.path):
        remove_not_use_images(root)
        # print(root)
        if not args.recursive:
            break

# print(args.path)
# print(get_image_paths(args.path))
# remove_not_use_images(args.path)