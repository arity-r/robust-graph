
import pickle, networkx as nx, matplotlib.pyplot as plt
from math import sqrt, log, pi, sin, cos
from random import uniform

with open('graph/opt_n_1000_01.pkl', 'rb') as fp:
    G = pickle.load(fp)
# degree difference
kd = lambda e: abs(G.degree(e[0]) - G.degree(e[1]))

# node attribute
node_color = list(map(G.degree, G.nodes_iter()))
node_degree = list(set(sorted(node_color)))
node_color = list(map(node_degree.index, node_color))
# initial position
layer_idx = lambda n: node_degree.index(G.degree(n))
node_list = [max(G.nodes_iter(), key=G.degree)]
node_stack = node_list[:]
while len(node_stack) > 0:
    n = node_stack.pop()
    neighbours_list = sorted(G.neighbors(n), key=lambda m: kd((n, m)))
    for n in neighbours_list:
        if not n in node_list and not n in node_stack:
            node_list.append(n)
            node_stack.append(n)

layers = len(node_degree)
node_num_in_layer = [0]*layers
for n in node_list:
    node_num_in_layer[layer_idx(n)] += 1
init_pos = {}
idx_in_layer = [0]*layers
for n in node_list:
    theta = idx_in_layer[layer_idx(n)]/node_num_in_layer[layer_idx(n)] * 2*pi
    dist  = (1 - ((layer_idx(n)+1) / layers))**2
    init_pos[n] = (dist*cos(theta), dist*sin(theta))
    idx_in_layer[layer_idx(n)] += 1

# edge weight
mindeg = lambda e: min(map(G.degree, e))
edge_weight = dict(zip(G.edges_iter(),
                       #map(lambda e: 1/sqrt(1+kd(e))*sqrt(mindeg(e)), G.edges_iter())))
                       map(lambda e: 1/sqrt(1+kd(e))*log(mindeg(e)), G.edges_iter())))
nx.set_edge_attributes(G, 'weight', edge_weight)

pos = nx.spring_layout(G, pos=init_pos, iterations=1)

# node property
nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_color, cmap=plt.get_cmap('hsv'))

# edge property
style = ['solid' if kd(e) == 0 else 'dashed' for e in G.edges_iter()]
width = [0.5 if kd(e) == 0 else 0.5 for e in G.edges_iter()]
edge_color = ['Black' if kd(e) == 0 else 'Gray' for e in G.edges_iter()]
nx.draw_networkx_edges(G, pos, style=style, width=width, edge_color=edge_color)

plt.axis('off')
plt.show()
