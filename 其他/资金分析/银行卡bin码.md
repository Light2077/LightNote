http://www.chakahao.com/bin/list/list_1.html

```python
"""
银行卡bin码匹配
"""
import pandas as pd


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

    def match(self, card, return_prefix=False):
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
        # 返回名称，匹配的前缀
        if return_prefix:
            return name, prefix
        return name

def get_tree(card_bin_data_path):
    df = pd.read_excel(card_bin_data_path, dtype=str)
    tree = Trie()
    for i, row in df.iterrows():
        bank = row.银行
        card_bin = row.卡BIN
        tree.insert(card_bin, bank)
    return tree

card_bin_data_path = 'E:\\Github\LightNote\\其他\\资金分析\\2020最新银联卡BIN表.xlsx'
card_bin_tree = get_tree(card_bin_data_path)


if __name__ == "__main__":
    # 卡号匹配
    cards = ['622848xxxx', '6228xxx', '6221880xx']
    for card in cards:
        name, prefix = card_bin_tree.match(card)
        print(card, prefix, name)
```

