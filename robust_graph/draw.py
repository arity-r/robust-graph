from __future__ import division
from math import sqrt, log, pi, sin, cos
from random import uniform
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.layout import spring_layout

def onion_layout(G):
    """
    Find node positions for onion-like topology

    :param networkx.Graph G: Graph
    :return: Position dictionary in networkx
    :rtype: dict
    """
    deg = G.degree()
    kd = lambda e: abs(deg[e[0]] - deg[e[1]])
    deglist = list(set(deg.values()))
    layer_idx = lambda n: deglist.index(deg[n])
    nodelist = [[] for _ in range(len(deglist))]
    for n in G.nodes_iter():
        nodelist[layer_idx(n)].append(n)
    for l in nodelist:
        tmp = l[:]
        del l[:]
        l.append(tmp.pop())
        while len(tmp) > 0:
            n = max(tmp,
                    key=lambda n: sum(map(lambda m: m in G[n], l)))
            l.append(n)
            tmp.remove(n)

    init_pos = {}
    for li, l in enumerate(nodelist):
        dist = (1 - ((li+1) / len(nodelist)))**2
        theta0 = uniform(0, 2*pi)
        for ni, n in enumerate(l):
            theta = ni / len(l) * 2*pi + theta0
            init_pos[n] = (dist*cos(theta), dist*sin(theta))

    # edge weight
    mindeg = lambda e: min(map(G.degree, e))
    edge_weight = dict(zip(G.edges_iter(),
                           map(lambda e: 1/sqrt(1+kd(e))*sqrt(mindeg(e)),
                               G.edges_iter())))
    nx.set_edge_attributes(G, 'weight', edge_weight)
    pos = spring_layout(G, pos=init_pos, iterations=1)
    return pos

def save_graph_as_image(G, filename, layout=onion_layout, **kwargs):
    """
    Save given graph as image.
    Node colors represent each degree of its node.
    Edges are shown as solid line if degrees of
    two incident nodes are same, otherwise, dash.

    .. image:: draw_sample.png

    :param networkx.Graph G: Graph
    :param str filename: filename
    :param layout function: function returns position dictionary
    :param kwargs dict: to pass to layout function
    """
    pos = layout(G, **kwargs)
    kd = lambda e: abs(G.degree(e[0]) - G.degree(e[1]))

    # node attribute
    node_color = list(map(G.degree, G.nodes_iter()))
    node_degree = list(set(sorted(node_color)))
    node_color = list(map(node_degree.index, node_color))

    # edge property
    style = ['solid' if kd(e) == 0 else 'dashed' for e in G.edges_iter()]
    width = [0.5 if kd(e) == 0 else 0.5 for e in G.edges_iter()]
    edge_color = ['Black' if kd(e) == 0 else 'Gray' for e in G.edges_iter()]

    plt.cla()
    plt.clf()
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_color, cmap=plt.get_cmap('hsv'))
    nx.draw_networkx_edges(G, pos, style=style, width=width, edge_color=edge_color)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
