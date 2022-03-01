"""
构建目录

- [numpy数组初识](基础_numpy数组初识.md)
  - [numpy数组简单创建](基础_numpy数组初识.md#numpy数组简单创建)
  - [numpy数组常用属性](基础_numpy数组初识.md#numpy数组常用属性)
  - [numpy数组轴的概念](基础_numpy数组初识.md#numpy数组轴的概念)
  - [小结](基础_numpy数组初识.md#小结)

需要设定文件读取顺序
"""

import os
import re


def get_titles(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        text = f.read()
    """ 获取markdown文件里的前3级标题 """
    # 因为代码块中的注释也包含了 '#' 
    # 因此需要去除文档中所有的代码块, re.S表示.*也匹配换行符
    text = re.sub('```.*?```', '', text, flags=re.S)

    # 匹配 1, 2, 3级标题
    titles = re.findall('^#{1,3} .*', text, flags=re.M)
    return titles


# 根据标题生成链接
def get_links(file, titles):
    """

    """
    links = ''
    for title in titles:
        # file_path = './demo.md'
        # title = '## 第一小节'
        # link: '  - [第一小节](./demo.md#第一小节)\n'

        level = title.count('#')  # 2
        title_text = title.lstrip('# ')  # 第一小节

        # np.random.randn() -> np-random-randn
        title_text2 = title_text.replace('.', '-')
        title_text2 = title_text2.replace('()', '')

        link = ' ' * 2 * level + f'- [{title_text}](./{file}#{title_text2})\n'
        links += link

    return links


file_paths = {
    "./numpy/" : [
        "基础_numpy数组初识.md",
        "基础_numpy数组创建.md",
        "基础_numpy数组索引.md",
        "基础_numpy数组操作.md",
        "基础_numpy数组运算.md",
    ],
}

def get_content_text():

    for file_dir in file_paths:
        # content_path = os.path.join(file_dir, 'contents.md')
        res = ''
        # with open(content_path, 'w', encoding='utf8') as f:
        for file in file_paths[file_dir]:
            file_path = os.path.join(file_dir, file)
            print(file_path)
            titles = get_titles(file_path)
            links = get_links(file, titles)
            # f.write(links)
            res += links

        # 插入到前言文件的最开头
    
