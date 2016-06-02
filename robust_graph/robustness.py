from __future__ import division
import networkx as nx
import random

def R(G, n=1):
    """
    Computes network robustness in :cite:`Schneider2011`.

    :param networkx.Graph G: The graph
    :param int n: The number of iteration, increase to accurate result.
    """
    return sum(sum(map(_s, [G]*n), []))/(len(G)*n)

def s(G, n=1):
    """
    Computes network robustness in :cite:`Schneider2011`.

    :param networkx.Graph G: The graph
    :param int n: The number of iteration, increase to accurate result.
    """
    return map(lambda s: sum(s) / n, zip(*map(_s, [G]*n)))

def _s(G):
    """
    Helper function for R and s.
    """
    G = G.copy()
    N = len(G)
    S_q = []
    for _ in range(N-1):
        deglist = list(G.degree().items())
        node, deg = max(deglist, key=lambda t: t[1])
        if deg > 0:
            node = random.choice(
                list(filter(lambda n: n[1]==deg, deglist)))[0]
        G.remove_node(node)
        if deg == 0:
            largest = 1
        else:
            largest = max(map(len, nx.connected_components(G)))
        S_q.append(largest / N)
    return S_q
