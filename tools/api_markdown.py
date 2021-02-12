"""
美化 GET POST PUT DELETE在markdown中的格式

使其带有字体颜色和字体背景色
"""
import re
import os


# HTML格式
TEXT = "<span style='color:{};background:{};font-size:16px;font-weight:bold'>{}</span>"


# 根据不同的API设定不同的字体颜色和背景颜色
API = {
    'GET': ("green", "lightgreen"),
    'POST': ("orange", "lightyellow"),
    'PUT': ("blue", "lightblue"),
    'DELETE': ("red", "pink"),
}

# 为了避免重复替换 匹配的时候左右多匹配一对 "><"
# 因为如果是带格式的字符串，左右必有一对 "><"
# 之后判断一下，如果是带格式的，就不必替换了
pat = re.compile(r'>?(GET|POST|PUT|DELETE)<?')


def api_beautify(match):
    api = match.group()  # GET / POST / PUT / DELETE
    if api[0] == '>':
        return api
    color, bgcolor = API[api]
    return TEXT.format(color, bgcolor, api)


for file in os.listdir():
    if file.split('.')[-1] != 'md':
        continue

    with open(file, 'r+', encoding='utf-8') as f:
        text = pat.sub(api_beautify, f.read())
        f.seek(0)
        f.write(text)
    print('修改%s成功!' % file)


# s = ">GET< AA POST"
# print(pat.sub(api_beautify, s))