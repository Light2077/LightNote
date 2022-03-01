import os
import re
import json
import base64
import shutil

# 写入代码块
def write_lines(f, lines, code_type='', end_enter=True):
    f.write(f'```{code_type}\n')
    f.write(''.join(lines))
    if end_enter:
        f.write('\n')
    f.write('```\n')

def notebook_to_markedown(notebook_path):
    # 给定notebook路径
    # markdown文件输出路径
    # 图片保存路径
    # notebook_path = 'demo.ipynb'

    # './demo/apple.csv' -> './demo', 'apple.csv'
    dirname, file_path = os.path.split(notebook_path)

    # apple.csv' -> 'apple'
    file_name = file_path.split('.')[0]

    markdown_path = os.path.join(dirname, file_name + '.md')
    # markdown_path = os.path.normpath(markdown_path)

    image_dir = os.path.join(dirname, 'images')
    

    with open(notebook_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    cells = data['cells']

    # matplotlib绘图图片数量
    img_num = 1

    with open(markdown_path, 'w', encoding='utf8') as f:
        for cell in cells:
            lines = cell['source']

            if cell["cell_type"] == 'markdown':
                f.write(''.join(lines))
                f.write('\n')


            elif cell["cell_type"] == "code":
                if lines:
                    write_lines(f, lines, code_type='python')

                for output in cell['outputs']:
                    if output['output_type'] == 'stream':
                        write_lines(f, output['text'], end_enter=False)
                        continue

                    output_data = output['data']
                    if 'image/png' in output_data:
                        # 创建图片文件夹
                        if not os.path.isdir(image_dir):
                            os.mkdir(image_dir)
                            
                        img_data = base64.b64decode(output_data['image/png'])
                        # todo: 保存图片

                        # img_path = f'./{image_dir}/'
                        img_path = os.path.join(image_dir, f"{file_name}_plot{img_num}.png")

                        with open(img_path, 'wb') as f2:
                            f2.write(img_data)
                            img_num += 1

                        img_name = os.path.split(img_path)[-1]

                        f.write(f"![](./images/{img_name})\n")

                    elif "text/plain" in output_data:
                        write_lines(f, output_data['text/plain'])
            else:
                print(cell['cell_type'])
        print(notebook_path, 'to', markdown_path)
# notebook_to_markedown('demo.ipynb')


# config_path = './config.py'
# 自动寻找要转换的ipynb文件路径
ipynb_dirs = ['./numpy/notebooks', './pandas/notebooks', './matplotlib/notebooks']
ipynb_paths = []
for dir_path in ipynb_dirs:
    if not os.path.isdir(dir_path):
        continue

    for path in os.listdir(dir_path):
        if path.endswith('ipynb'):
            ipynb_paths.append(dir_path +'/' + path)

# # 生成config文件
# with open(config_path, 'w', encoding='utf8') as f:
#     f.write('c = get_config()\n')
#     f.write('c.NbConvertApp.notebooks = [\n')
#     for path in ipynb_paths:
#         f.write(f'    "{path}",\n')
#     f.write(']\n')

# 将notebook转换为markdown
# os.system("jupyter nbconvert --config config.py --to markdown")
for ipynb_path in ipynb_paths:
    notebook_to_markedown(ipynb_path)


def mysub(x):
    # 传入的是re.Match对象
    x = x.group(1)
    if x.startswith('..'):
        x = x[1:]
        # print(x)
    return f"![]({x})"

# 移动转换好的markdown到上一级文件
for path in ipynb_paths:
    src_path = path[:-5] + 'md'
    file_name = os.path.split(src_path)[-1]
    dst_dir = os.path.dirname(os.path.dirname(src_path))
    dst_path = os.path.join(dst_dir, file_name)

    # 修改markdown里的图片链接
    with open(src_path, 'r+', encoding='utf8') as f:
        text = f.read()
        new_text = re.sub(f'!\[.*?\]\((.*?)\)', mysub, text)

        with open(dst_path, 'w', encoding='utf8') as f:
            f.write(new_text)

    os.remove(src_path)
    # if os.path.isfile(dst_path):
    #     os.remove(dst_path)

    # shutil.move(src_path, dst_path)

# 图片移动过去

for ipynb_dir in ipynb_dirs:
    base_img_dir = os.path.join(os.path.dirname(ipynb_dir), 'images')
    img_dir = os.path.join(ipynb_dir, 'images')

    if not os.path.isdir(img_dir):
        continue

    for path in os.listdir(img_dir):
        src_path = os.path.join(img_dir, path)

        dst_path = os.path.join(base_img_dir, path)
        if os.path.isfile(dst_path):
            os.remove(dst_path)

        shutil.move(src_path, dst_path)

