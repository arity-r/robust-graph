from __future__ import division
import networkx as nx
import random

def R(G, n=1):
    """
    Computes network robustness in :cite:`Schneider2011`.

    :param networkx.Graph G: The graph
    :param int n: The number of iteration, increase to accurate result.
    """
    return sum(map(_R, [G]*n)) / n

def s(G, n=1):
    """
    Computes network robustness in :cite:`Schneider2011`.

    :param networkx.Graph G: The graph
    :param int n: The number of iteration, increase to accurate result.
    """
    return map(lambda s: sum(s) / n, zip(*map(_s, [G]*n)))

def _R(G):
    # Helper function for R.
    return sum(_s(G)) / len(G)

def _s(G):
    # Helper function for R and s.
    G = G.copy()
    N = len(G)
    S_q = []
    all_apart = False
    for _ in range(N-1):
        deglist = list(G.degree().items())
        random.shuffle(deglist) # update: shuffle first
        node, deg = max(deglist, key=lambda t: t[1])
        G.remove_node(node)
        if deg > 0:
            largest = max(map(len, nx.connected_components(G)))
            S_q.append(largest)
        else:
            largest = 1
            S_q.extend([1]*(N-len(S_q)-1))
            break # no further element other than 1 quit
    return map(lambda s: s / N, S_q)
