"""
扫描当前文件夹和子文件夹下所有的markdown文件
扫描和markdown文件同级目录下的img文件夹
删除img文件夹中没有被markdown引用的图片
"""
import re
import os

for root, dirs, files in os.walk('.'):
    used_imgs = set()
    for file in files:
        if file[-2:] == 'md':
            print(file)
            with open(os.path.join(root, file), 'r', encoding='utf8') as f:
                text = f.read()
                # imgs = re.findall(r'\!\[.*?\]\((.*?)\)', text)
                imgs = re.findall(r'img/(.*?)\)', text)
                used_imgs.update(set(imgs))
                
    if 'img' in dirs:
        for file in os.listdir(os.path.join(root, 'img')):
            if file.split('.')[-1] not in ['png', 'jpg']:
                continue
            if file not in used_imgs:
                path = os.path.join(root, 'img', file)
                print('remove', path)
                # os.remove(path)