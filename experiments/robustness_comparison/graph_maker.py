
import sys, random, pickle
from networkx import barabasi_albert_graph
from networkx.utils.random_sequence import create_degree_sequence
from networkx import configuration_model
from networkx import double_edge_swap

def my_distribution(n, gamma, avrdeg):
    return [random.paretovariate(gamma-1)*
            avrdeg*(gamma-2)/(gamma-1) for _ in range(n)]
def graph(n=100, gamma=2.5, avrdeg=5.8):
    seq = create_degree_sequence(
        n, my_distribution, gamma=gamma, avrdeg=avrdeg)
    return configuration_model(seq)

for i in range(100):
    #G = graph()
    G = barabasi_albert_graph(100, 3)
    double_edge_swap(G, nswap=400, max_tries=1000)
    with open('graph/orig_%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
    print('Graph %02d generated'%i)
