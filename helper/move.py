"""
把当前文件夹下的图片文件全部转到img文件夹下
并把md文件的
"""
import re
import os
import shutil
# 如果img文件 创建之
if not os.path.isdir('img'):
    os.mkdir('img')

# 移动图片文件至img文件夹
for file in os.listdir('.'):
    if file.endswith('.png'):
        shutil.move(file, 'img/' + file)

# 匹配![hello](hello.png) 中的 hello.png
pattern = re.compile(r'!\[.*?\]\((.*?)\)')

# 自动检测以.md结尾的文件
for markdown_file in os.listdir('.'):
    if not markdown_file.endswith('.md'):
        continue
    with open(markdown_file, mode='r+', encoding='utf8') as f:
        
        text = f.read()
        for file in pattern.findall(text):
            if file[:4] != 'img/':
                text = re.sub(file, 'img/'+file, text)
        f.seek(0)
        f.write(text)
        f.truncate()