import matplotlib.pyplot as plt
import networkx as nx

graph = {
    "A": {"B": 5, "C": 1},
    "B": {"A": 5, "C": 2, "D": 1},
    "C": {"A": 1, "B": 2, "D": 4, "E": 8},
    "D": {"B": 1, "C": 4, "E": 3, "F": 6},
    "E": {"C": 8, "D": 3},
    "F": {"D": 6},
}

G = nx.Graph()
edge = []
edge_labels = dict()

# 获得边和边标签
for start in graph:
    for end in graph[start]:
        G.add_edge(start, end)
        edge.append((start, end))
        edge_labels[(start, end)] = graph[start][end]

pos = nx.spring_layout(G, seed=1)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700,node_color="c")
# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_color="w")

# edges
nx.draw_networkx_edges(G, pos, edgelist=edge, width=2)

# edge_labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)

plt.axis("off")

plt.savefig("../img/快速上手.png")
plt.show()