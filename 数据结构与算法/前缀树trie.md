https://leetcode.cn/problems/implement-trie-prefix-tree/

最基本的前缀树，基于字典实现

```python
class Trie:
    def __init__(self):
        self.children = dict()
        self.is_end = False

    def insert(self, word: str) -> None:
        node = self
        for a in word:
            if a not in node.children:
                node.children[a] = Trie()
            node = node.children[a]
        node.is_end = True

    def search_prefix(self, prefix: str):
        node = self
        for a in prefix:
            if a not in node.children:
                return
            node = node.children[a]
        return node

    def search(self, word: str) -> bool:
        node = self.search_prefix(word)
        return node is not None and node.is_end

    def startswith(self, prefix: str) -> bool:
        return self.search_prefix(prefix) is not None
```



前缀树应用案例：银行卡bin码匹配

```python
"""
银行卡bin码匹配

采用前缀树实现
"""
import pandas as pd
import json


class Trie:
    def __init__(self):
        self.children = dict()
        self.is_end = False
        self.name = ''
        self.prefix = ''

    def insert(self, word: str, name) -> None:
        node = self
        prefix = ''
        for a in word:
            if a not in node.children:
                node.children[a] = Trie()
            node = node.children[a]
            prefix += a
        node.is_end = True
        node.name = name
        node.prefix = prefix

    def search_prefix(self, prefix: str):
        node = self
        for a in prefix:
            if a not in node.children:
                return
            node = node.children[a]
        return node

    def search(self, word: str) -> bool:
        node = self.search_prefix(word)
        return node is not None and node.is_end

    def startswith(self, prefix: str) -> bool:
        return self.search_prefix(prefix) is not None

    def match(self, card):
        name = ''
        prefix = ''
        node = self
        for a in card:
            if a not in node.children:
                break
            node = node.children[a]
            if node.name != '':
                name = node.name
                prefix = node.prefix
        return name, prefix


def get_tree(card_bin_data_path):
    df = pd.read_excel(card_bin_data_path, dtype=str)
    tree = Trie()
    for i, row in df.iterrows():
        bank = row.银行
        card_bin = row.卡BIN
        tree.insert(card_bin, bank)
    return tree


if __name__ == "__main__":
    card_bin_data_path = 'E:\\Github\LightNote\\其他\\资金分析\\2020最新银联卡BIN表.xlsx'
    tree = get_tree(card_bin_data_path)

    # 卡号匹配
    cards = ['622848xxxx', '6228xxx', '6221880xx']
    for card in cards:
        name, prefix = tree.match(card)
        print(card, prefix, name)
```



```python
path = r'E:\Github\LightNote\其他\资金分析\2020最新银联卡BIN表.xlsx'
df = pd.read_excel(path, dtype=str)

# 构建前缀树
tree = Trie()
for i, row in df.iterrows():
    bank = row.银行
    card_bin = row.卡BIN
    tree.insert(card_bin, bank)
    
# 卡号匹配
cards = ['622848xxxx', '6228xxx', '6221880xx']
for card in cards:
    print(tree.match(card))
```

