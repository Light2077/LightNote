"""
图片文件存储在images文件夹下

并把md文件的
"""
import re
import os
import shutil
import glob
import argparse
parser = argparse.ArgumentParser()

# 文件路径参数，默认是当前文件夹下
parser.add_argument("path", type=str, default=".", help="要处理的文件夹的路径")
args = parser.parse_args()


pattern = re.compile(r'\!\[.*?\]\((.*?)\)')
# 获取当前目录下所有markdownh中用到的图片路径
def move_markdown_used_imgs(dir_path):
    markdown_paths = glob.glob(os.path.join(dir_path, '*.md'))
    used_img_paths = set()
    for markdown_path in markdown_paths:
        with open(markdown_path, 'r', encoding='utf8') as f:
            text = f.read()
            text2 = re.sub(r'`.*?`', '',  text, flags=re.S)  # 去除代码块
            img_paths = pattern.findall(text2)

            for img_path in img_paths:
                img_dir, img_name = os.path.split(os.path.normpath(img_path))
                if img_dir == "images":
                    continue

                # 若图片不存在则不进行操作
                if not os.path.isfile(os.path.join(dir_path, img_path)):
                    continue
                    # print(markdown_path, ":", os.path.join(dir_path, img_path))

                # 新的图片的路径
                new_img_path = os.path.join("images", img_name).replace('\\', '/')

                if not os.path.isdir(os.path.join(dir_path, "images")):
                    os.makedirs(os.path.join(dir_path, "images"))
                # 移动图片到新位置
                print(markdown_path, "move", img_path, "to", new_img_path)
                # print("move", os.path.join(dir_path, img_path), "to", os.path.join(dir_path, new_img_path))
                shutil.move(os.path.join(dir_path, img_path), os.path.join(dir_path, new_img_path))
                
                # 替换markdown内的图片路径
                text = text.replace(img_path, new_img_path)
                # re.sub(img_path, new_img_path, text)

            img_paths = set([os.path.normpath(os.path.join(dir_path, img_path)) for img_path in img_paths])
            # imgs = re.findall(r'img/(.*?)\)', text)
            used_img_paths.update(img_paths)

        # 更新markdown
        with open(markdown_path, 'w', encoding='utf8') as f:
            f.write(text)

    # # 删除旧图片
    # if used_img_paths:
    #     print("----------------------删除旧图片----------------------")

    # for img_path in used_img_paths:
    #     print("remove", img_path)
    #     # os.remove(img_path)



if __name__ == "__main__":
    for root, dirs, files in os.walk(args.path):
        # move_markdown_used_imgs(root)

        img_dir = os.path.join(root, 'img')
        if os.path.isdir(img_dir):
            if len(os.listdir(img_dir)) > 0:
                new_img_dir = os.path.join(root, "images")
                if not os.path.isdir(new_img_dir):
                    os.makedirs(new_img_dir)

                for name in os.listdir(img_dir):
                    src = os.path.join(img_dir, name)
                    dst = os.path.join(new_img_dir, name)
                    shutil.move(src, dst)
                    print(src, dst)
            
            os.removedirs(img_dir)

