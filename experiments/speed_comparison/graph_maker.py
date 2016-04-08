
import sys, random, pickle, networkx as nx
from networkx import barabasi_albert_graph
from networkx.utils.random_sequence import create_degree_sequence
from networkx import configuration_model
from networkx import double_edge_swap

def my_distribution(n, gamma, avrdeg):
    return [random.paretovariate(gamma-1)*
            avrdeg*(gamma-2)/(gamma-1) for _ in range(n)]
def graph(n=100, gamma=2.5, avrdeg=8):
    seq = create_degree_sequence(
        n, my_distribution, gamma=gamma, avrdeg=avrdeg)
    G = configuration_model(seq)
    # multigraph -> graph
    G.remove_edges_from(G.selfloop_edges())
    return nx.Graph(G)

for i in range(10):
    #G = graph()
    G = barabasi_albert_graph(500, 3)
    with open('graph/ba_%d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
    print('Graph %d generated'%i)
