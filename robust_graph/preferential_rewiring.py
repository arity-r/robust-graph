from __future__ import division
import random
import networkx as nx

def greedy_rewiring(G, max_trias=1000):
    return preferential_rewiring(G, greedy=True, max_tries=max_trias)

def preferential_rewiring(G, greedy=False, max_tries=1000):
    kdelta = lambda e: abs(G.degree(e[0])-G.degree(e[1]))
    deg_diff = dict(zip(G.edges_iter(), map(kdelta, G.edges_iter())))
    for _ in range(max_tries):
        # choose two links from degree difference
        swap_edges = []
        for __ in range(2):
            prob_total = 0
            rvalue = random.uniform(0, sum(deg_diff.values()))
            for key, value in deg_diff.items():
                prob_total += value
                if rvalue < prob_total:
                    swap_edges.append(key)
                    break
        (u,v),(x,y) = swap_edges
        if greedy:
            if kdelta((u,x))+kdelta((v,y)) > kdelta((u,y))+kdelta((v,x)):
                x,y = y,x
        else:
            if random.uniform(0, 1) < 0.5:
                x,y = y,x

        # check if same vertex
        if x in (u,v) or y in (u,v): continue
        # check if parallel edge
        if x in G[u] or y in G[v]: continue

	# simulate swap
        G.remove_edges_from([(u,v),(x,y)])
        G.add_edges_from([(u,x),(v,y)])
        # then check connectivity
        can_swap = nx.has_path(G, u, v)
        if can_swap:
            return G
        else:
            # undo swapping
            G.add_edges_from([(u,v),(x,y)])
            G.remove_edges_from([(u,x),(v,y)])
    raise Exception('could not rewire in %d tries'%max_tries)

