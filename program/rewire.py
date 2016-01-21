from __future__ import division
import random
import networkx as nx

def rewire(G):
	deg_diff = dict(zip(G.edges_iter(), [abs(G.degree(e[0])-G.degree(e[1])) for e in G.edges_iter()]))

	# choose first edge from degree difference
	prob_total = 0
	rvalue = random.uniform(0, sum(deg_diff.values()))
	for key, value in deg_diff.items():
		prob_total += value
		if rvalue < prob_total:
			u,v = key
			break

	edge_prob = {}
	for e in G.edges_iter():
		for x,y in (e, reversed(e)): # try two pairs
			# omit same vertex
			if x in (u,v) or y in (u,v): continue
			# omit parallel edge
			if x in G[u] or y in G[v]: continue

			# swap anyway
			#G.remove_edges_from([(u,v),(x,y)])
			#G.add_edges_from([(u,x),(v,y)])
			G.remove_edge(u, v); G.remove_edge(x, y)
			G.add_edge(u, x); G.add_edge(v, y)
			# then check connectivity
			can_swap = nx.has_path(G, u, v)
			# undo swapping
			#G.remove_edges_from([(u,x),(v,y)])
			#G.add_edges_from([(u,v),(x,y)])
			G.add_edge(u, v); G.add_edge(x, y)
			G.remove_edge(u, x); G.remove_edge(v, y)
			# calculate score
			if can_swap:
				score = abs(G.degree(u)-G.degree(x)) + abs(G.degree(v)-G.degree(y))
				edge_prob[(x,y)] = 1 / score if score else 1

	if len(edge_prob.keys()) == 0: return None

	prob_total = 0
	rvalue = random.uniform(0, sum(edge_prob.values()))
	for key, value in edge_prob.items():
		prob_total += value
		if rvalue < prob_total:
			x, y = key
			#G.remove_edges_from([(u,v),(x,y)])
			#G.add_edges_from([(u,x),(v,y)])
			G.remove_edge(u, v); G.remove_edge(x, y)
			G.add_edge(u, x); G.add_edge(v, y)
			return ((u, v),(x, y))
