播种阶段需要造ARPA吗？造多少？

调整之后的科技知识消耗

```js
evolve.adjustCosts(evolve.actions.tech.mad).Knowledge()
```

获取科技的消耗：如共同毁灭原则的石油消耗

```js
evolve.actions.tech.mad.cost.Oil() 
```



对于包含函数的对象，导出json时获取函数的结果

[你不知道的 JSON.stringify() 的威力](https://segmentfault.com/a/1190000021230185)

```js
a = JSON.stringify(evolve.actions.tech.mad, (key, value) => {
  switch (true) {
    case typeof value === "function":
      if (key in evolve.global.resource) {
        return value();
      }
    default:
      break;
  }
  return value;
})
```

城市

```js
a = JSON.stringify(evolve.actions.city)
```



保存字符串到本地

```js


function exportRaw(name, data) {
            var urlObject = window.URL || window.webkitURL || window;
            var export_blob = new Blob([data]);
            var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a")
            save_link.href = urlObject.createObjectURL(export_blob);
            save_link.download = name;
            fakeClick(save_link);
        }
function fakeClick(obj) {
            var ev = document.createEvent("MouseEvents");
            ev.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            obj.dispatchEvent(ev);
        }

exportRaw('evolve.txt', a);
```

```js
a = JSON.stringify(evolve.actions, (key, value) => {
    switch (true) {
        case typeof value === "function":
            if ('name' in value){ 
                if (value.name === "title") {
                    try {
                        return value();
                    }
                    catch(err) {
                        break;
                    }
                }
            }
        default:
            break;
    }
    return value;
})
```



## 爬虫

```python
import requests
import json
from lxml import etree

with open('tech_htmls.json', 'r', encoding='utf8') as f:
    htmls = json.load(f)

def get_first(tag_xpath):
    if len(tag_xpath) == 1:
        return tag_xpath[0]
    elif len(tag_xpath) == 0:
        return ""
    raise ValueError
    
base_url = "https://pmotschmann.github.io/Evolve/"

techs = dict()
for era in htmls:
    root = etree.HTML(htmls[era])
    tags = root.xpath('//div[@id="mainContent"]/div')
    for tag in tags:
        d = dict()
        # 科技英文名：'housing'
        d['en_name'] = tag.get('id')

        # 科技中文名：'住房'
        d['name'] = tag.xpath('./div/h2/text()')[0]

        # 所属科技组。如：'Housing: 1'
        d['group'] = tag.xpath('./div/span[starts-with(@class, "has-text")]/text()')[0]

        # 科技基本描述，如：解锁基本住房单元，可供一位市民居住
        d['desc'] = get_first(tag.xpath('./div[@class="desc"]/text()'))
        # 科技花费，如：['知识: 10']
        d['cost'] = tag.xpath('./div[@class="stats"]/div[starts-with(@class, "cost")]/div/text()')

        # 科技效果，如：['解锁 小木屋 建筑。']
        d['extra'] = tag.xpath('./div[@class="extra"]/div/text()')

        # 前置研究需求
        tag_reqs_a = tag.xpath('./div[@class="reqs"]/span[contains(text(), "需要前置研究")]/following-sibling::span/a')
        tech_reqs = []
        for a in tag_reqs_a:
            tech_req = dict()
            tech_req['name'] = a.xpath('text()')[0]
            tech_req['url'] = base_url + a.xpath('./@href')[0]
            tech_reqs.append(tech_req)
        d['tech_reqs'] = tech_reqs
        techs[d['name']] = d
with open('techs.json', 'w', encoding='utf8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=2)
```

## 科技树的构建

```python
class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = list()
        
    def result(self):
        res = ["graph TD"]
        visited_node = set()
        for node in self.nodes.values():
            for next_node in node.next_nodes.values():
                node_b = next_node['node']
                msg = ""
                if next_node['msg']:
                    msg = f"|{next_node['msg']}|"
                
                start_node = node.name if node in visited_node else node.text()
                end_node = node_b.name if node_b in visited_node else node_b.text()
                res.append(f"{start_node} --> {msg} {end_node}")
                visited_node.add(node)
                visited_node.add(node_b)
        return "\n".join(res)


    def add_edges(self, node_a, node_b, msg=''):
        self.nodes[node_a.name] = node_a
        self.nodes[node_b.name] = node_b
        node_a.next_nodes[node_b.name] = {'node': node_b, 'msg': msg} 

class Node:
    def __init__(self, name='', content=''):
        self.name = name
        if content:
            self.content = content
        else:
            self.content = name
        self.next_nodes = dict()
        
    def text(self):
        return f'{self.name}[{self.content}]'
            
    
    def __repr__(self):
        return self.name
    
```

查看结果

```python
nodes = dict()
# 创建结点
for name, tech in techs.items():
    nodes[name] = Node(name)



# 创建边
g = Graph()
nodes = dict()
# 创建结点
for name, tech in techs.items():
    nodes[name] = Node(name)
    
layer_limit = 10  # 向上追溯5层
layer = 1  # 当前层数
q = list([techs['能量护盾']])
while q:
    new_q = []
    for tech in q:
        for prev_tech_msg in tech['tech_reqs']:
            prev_tech = techs[prev_tech_msg['name']]
            new_q.append(prev_tech)

            node = nodes[tech['name']]
            prev_node = nodes[prev_tech['name']]
            g.add_edges(prev_node, node)
    q = new_q
    layer += 1
    if layer > layer_limit:
        break
print(g.result())
```

```
graph TD
等离子束[等离子束] -->  能量护盾[能量护盾]
虚拟现实[虚拟现实] -->  等离子束
量子计算[量子计算] -->  虚拟现实
锡烯[锡烯] -->  虚拟现实
人工智能[人工智能] -->  量子计算
人工智能 -->  纳米管[纳米管]
纳米管 -->  量子计算
激光[激光] -->  人工智能
高级机器人技术[高级机器人技术] -->  激光
超铀理论[超铀理论] -->  激光
火箭技术[火箭技术] -->  高级机器人技术
超铀开采[超铀开采] -->  超铀理论
A.R.P.A.[A.R.P.A.] -->  火箭技术
核裂变[核裂变] -->  A.R.P.A.
电子学[电子学] -->  核裂变
铀提取[铀提取] -->  核裂变
```

然后复制到：https://mermaid-js.github.io/mermaid-live-editor/edit

就可以查看可视化结果了。

## 脚本读取

```python
import json
import pandas as pd
with open('脚本备份.txt') as f:
    s = json.load(f)
triggers = s['triggers']
triggers = pd.DataFrame(triggers)
# json.loads(triggers.to_json(orient='records'))[0]  # 还原回json
```

