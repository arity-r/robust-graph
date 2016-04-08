from networkx import double_edge_swap
from robust_graph import R
from common import run

def greedy_update(G1):
    trials = 10**3
    while trials:
        trials -= 1
        G2 = G1.copy()
        double_edge_swap(G2)
        if R(G2) > R(G1):
            return G2
    return G1

run(greedy_update, 'greedy')
