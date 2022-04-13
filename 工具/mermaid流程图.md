# mermaid

https://mermaid-js.github.io/mermaid-live-editor/edit

原始代码

```
graph TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
```

通过python代码来生成流程图

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
    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content
        self.next_nodes = dict()
        
    def text(self):
        return f'{self.name}[{self.content}]'
```

```python
g = Graph()
nodes = dict(
    a = Node('A', 'Christmas'),
    b = Node('B', 'Go shopping'),
    c = Node('C', 'Let me think'),
    d = Node('D', 'Laptop'),
    e = Node('E', 'iPhone'),
    f = Node('F', 'fa:fa-car Car'),
)

g.add_edges(nodes['a'], nodes['b'], 'Get money')
g.add_edges(nodes['b'], nodes['c'])
g.add_edges(nodes['c'], nodes['d'], 'One')
g.add_edges(nodes['c'], nodes['e'], 'Two')
g.add_edges(nodes['c'], nodes['f'], 'Three')
print(g.result())
```

```
graph TD
A[Christmas] --> |Get money| B[Go shopping]
B --> C[Let me think]
C --> |One| D[Laptop]
C --> |Two| E[iPhone]
C --> |Three| F[fa:fa-car Car]
```

