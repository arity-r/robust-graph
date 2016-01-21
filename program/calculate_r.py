from __future__ import division
import networkx as nx
import random

def calculateR(G):
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
	G = G.copy()
	N = len(G)
	S_q = []
	for _ in range(N-1):
		maxdeg = max(nx.degree(G).values())
		maxnodes = [n for n in G.nodes() if G.degree(n) == maxdeg]
		removed_node = random.choice(maxnodes)
		G.remove_node(removed_node)
		largest_connected = max(nx.connected_components(G), key=len)
		S_q.append(len(largest_connected) / N)
	return sum(S_q) / N

