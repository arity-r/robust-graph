from __future__ import division
import sys, time, random
import networkx as nx

def onion_structure(deg, a=3):
    G = nx.Graph()
    stubs = sum(map(lambda i: [i[0]]*i[1], enumerate(deg)), [])
    mindeg = min(deg)
    layer = sum(map(lambda i: [i[1]-mindeg]*i[1], enumerate(deg)), [])
    stubs = list(zip(stubs, layer))

    trials = len(deg)
    prev_size = len(stubs)
    while trials > 0 and len(stubs) > 0:
        if prev_size == len(stubs):
            trials -= 1
        else: trials = len(deg)
        prev_size = len(stubs)
        # 0 --> vertex, 1 --> layer index
        (i, si), (j, sj) = random.sample(stubs, 2)
        # same vertex
        if i == j: continue
        # parallel edge
        if j in G.nodes() and i in G[j] or\
           i in G.nodes() and j in G[i]: continue
        if random.uniform(0, 1) < 1 / (1+a*abs(si-sj)):
            G.add_edge(i, j)
            stubs.remove((i, si))
            stubs.remove((j, sj))
    while len(stubs) > 0:
        (i, si), (j, sj) = random.sample(stubs, 2)
        u, v = random.choice(G.edges())
        # check if same vertex
        if i in (u,v) or j in (u,v): continue
        # check if parallel edge
        if i in G[u] or j in G[v]: continue
        # simulate swap
        G.remove_edge(u,v)
        G.add_edges_from([(u,i),(v,j)])
        # then check connectivity
        can_swap = nx.has_path(G, u, v)
        if can_swap:
            stubs.remove((i, si))
            stubs.remove((j, sj))
        else:
            # undo
            G.add_edge(u,v)
            G.remove_edges_from([(u,i),(v,j)])
    return G

def configuration_model(deg):
    return onion_structure(deg, a=0)
