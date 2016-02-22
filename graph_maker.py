
import sys, random, pickle
from networkx.utils.random_sequence import create_degree_sequence
from netutil import configuration_model

def my_distribution(n, gamma, avrdeg):
    return [random.paretovariate(gamma-1)*
            avrdeg*(gamma-2)/(gamma-1) for _ in range(n)]
def graph(n=2000, gamma=2.5, avrdeg=4.75):
    seq = create_degree_sequence(
        n, my_distribution, gamma=gamma, avrdeg=avrdeg)
    return configuration_model(dict(zip(range(len(seq)), seq)))

for i in range(10):
    G = graph()
    with open('graph/graph%02d.pkl'%i, 'wb') as fp:
        pickle.dump(G, fp)
