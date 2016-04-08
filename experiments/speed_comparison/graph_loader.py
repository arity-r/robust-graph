import os.path as path, networkx as nx
from os.path import dirname, abspath

def load_us():
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
    return G

def main():
    G = load_us()
    assert len(G.nodes()) == 332
    assert len(G.edges()) == 2126
    assert max(G.degree().values()) == 139

if __name__ == '__main__':
    main()

