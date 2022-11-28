https://docs.qq.com/doc/DYk16WE1aSk1iZmdl

解析script下的txt脚本

```python
def get_re_match(pattern, item, group=1):
    match = re.search(pattern, item)
    if match:
        return match.group(1)
    
def get_key_value(key, item_str):
    value = get_re_match(f'{key} *= *(.*?),', item)
    return value

with open(r'D:\Software\steam\steamapps\common\ProjectZomboid\media\scripts\items.txt') as f:
    text = f.read()
text = re.sub('\n', ' ', text)
text = re.sub('\t', ' ', text)
# 删除所有注释
# re.sub(r'/\*.*?\*/', '', text)
```

匹配所有items

```python
items = re.findall(r'item [a-zA-Z]+ +\{.*?\}', text)
item = items[0]
item
```

获取名字和key value

```python
item_name = get_re_match(r'item (\w+)', item)
weight = get_key_value('Weight', item)
```

