from __future__ import division
import os.path as path
import random
import networkx as nx
from os.path import dirname, abspath
from networkx.utils.random_sequence import create_degree_sequence
from networkx import configuration_model

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
