
import pickle, networkx as nx, matplotlib.pyplot as plt

with open('graph/opt_n_99.pkl', 'rb') as fp:
    G = pickle.load(fp)

node_color = list(map(float, map(G.degree, G.nodes_iter())))
node_degree = list(set(sorted(node_color)))
node_color = list(map(node_degree.index, node_color))
#pos = nx.spring_layout(G, dim=len(node_degree), iterations=100)
pos = nx.spring_layout(G, k=0.11, dim=2, iterations=500)

# node property
nx.draw_networkx_nodes(G, pos, node_size=150, node_color=node_color, cmap=plt.get_cmap('gist_rainbow'))

# edge property
kd = lambda e: abs(G.degree(e[0]) - G.degree(e[1]))
style = ['solid' if kd(e) == 0 else 'dashed' for e in G.edges_iter()]
width = [1 if kd(e) == 0 else 1 for e in G.edges_iter()]
edge_color = ['Black' if kd(e) == 0 else 'Gray' for e in G.edges_iter()]
nx.draw_networkx_edges(G, pos, style=style, width=width, edge_color=edge_color)

plt.axis('off')
plt.show()
