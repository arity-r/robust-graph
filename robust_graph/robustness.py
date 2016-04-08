from __future__ import division
import networkx as nx
import random

def R(G, n=1):
    """
    Notes
    -----
    This function computes Eq.[1] in Ref.[1]

    References
    ----------
    .. [1]Schneider, C. M., Moreira, A. A., Andrade, J. S., Havlin, S., & Herrmann, H. J. (2011).
    Mitigation of malicious attacks on networks.
    Proceedings of the National Academy of Sciences, 108(10), 3838-3841.
    .. [2] Herrmann, H. J., Schneider, C. M., Moreira, A. A., Andrade Jr, J. S., & Havlin, S. (2011).
    Onion-like network topology enhances robustness against malicious attacks.
    Journal of Statistical Mechanics: Theory and Experiment, 2011(01), P01027.
    """
    N = len(G)
    return sum(sum(map(s, [G]*n), []))/(N*n)

def s(G):
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
