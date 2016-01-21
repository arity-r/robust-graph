import networkx as nx
def initializeTestGraph():
	G = nx.Graph()
	G.add_nodes_from([i for i in range(1,7)])
	G.add_edges_from([(1,2),(1,5),(2,3),(2,4),(2,6),(3,6),(4,5),(5,6),])
	return G
def initializeTestGraph2():
	G = nx.Graph()
	G.add_nodes_from([i for i in range(1,7)])
	G.add_edges_from([(1,2),(1,3),(2,4),(2,5),(2,6),(3,6),(4,5),(5,6),])
	return G
