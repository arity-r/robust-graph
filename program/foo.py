#!/usr/bin/python
from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt

from init_test import initializeTestGraph, initializeTestGraph2
from calculate_r import calculateR
from rewire import rewire

def main():
	G = initializeTestGraph()
	nx.draw(G, with_labels=True)
	plt.savefig('foo.png')
	plt.close()
	print("initial R:", calculateR(G))

	swapped_pairs = rewire(G)
	print("swapped", swapped_pairs)

	nx.draw(G, with_labels=True)
	plt.savefig('bar.png')
	plt.close()
	print("swapped R:", calculateR(G))

if __name__ == '__main__':
	main()
