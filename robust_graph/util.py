from __future__ import division
import os.path as path
import random
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt, log, pi, sin, cos
from random import uniform
from os.path import dirname, abspath
from networkx.utils.random_sequence import create_degree_sequence
from networkx import configuration_model
from networkx.drawing.layout import spring_layout

def powerlaw_sequence(n, gamma, avrdeg):
    """
    Generate power-law degree sequence by pareto distribution.

    :param int   n:      The number of nodes
    :param float gamma:  Exponent of distribution
    :param float avrdeg: Average degree
    :return: Degree distribution
    :rtype: list
    """
    return [random.paretovariate(gamma-1)*
            avrdeg*(gamma-2)/(gamma-1) for _ in range(n)]

def scale_free_network(n=100, gamma=2.5, avrdeg=8):
    """
    Generates a scale free network by configuration model,
    which is shown in :cite:`Wu2011`

    :param int   n:      The number of nodes
    :param float gamma:  Exponent of degree distribution
    :param float avrdeg: Average degree
    :return: Scale-free network
    :rtype: networkx.Graph

    Generates degree sequence from calling
    :func:`~.powerlaw_sequence` and
    :func:`networkx.utils.random_sequence.create_degree_sequence`
    then, build network by configuration model
    (see :func:`networkx.generators.degree_seq.configuration_model`)
    finally, remove self-loop and parallel edge to simplify.

    .. Note:: Actual average degree is smaller than `avrdeg`
    """
    seq = create_degree_sequence(
        n, powerlaw_sequence, gamma=gamma, avrdeg=avrdeg)
    G = configuration_model(seq)
    # multigraph -> graph
    G.remove_edges_from(G.selfloop_edges())
    return nx.Graph(G)

def load_us():
    """
    Load US airline network.

    :return: US Airline network
    :rtype: networkx.Graph
    """
    with open(path.join(dirname(abspath(__file__)), 'USAir97.txt')) as fp:
        contents = fp.read()
    #V, A, E = contents.split('*Vertices')
    V = contents.split('*Vertices')[1].split('*Arcs')[0].splitlines()[1:]
    V = map(lambda c: int(c[0]), map(lambda l: l.split(), V))
    E = contents.split('*Vertices')[1].split('*Arcs')[1].split('*Edges')[1].splitlines()
    E = filter(len, E)
    E = map(lambda c: (int(c[0]), int(c[1])), map(lambda l: l.split(), E))
    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    # is loaded graph actually US Air network?
    assert len(G.nodes()) == 332
    assert len(G.edges()) == 2126
    assert max(G.degree().values()) == 139

    return G

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
