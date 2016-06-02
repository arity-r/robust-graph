import networkx as nx
from robust_graph import R
from robust_graph import LOG_LEVEL_INFO as LOG_LEVEL
from robust_graph import TimeTracker

# an algorithm
from robust_graph import IchinoseSatotani

# function to load US airline network
from robust_graph import load_us

# some important constants
n_attacks = 10
n_steps = 100
filename = 'Randr.csv'
graph = load_us()

# define columns in csv
columns = [
    # R robustness
    ('R', lambda G: R(G, n_attacks)),
    # r degree correlation
    ('r', nx.degree_pearson_correlation_coefficient)
]

# use TimeTracker to track R and r
tracker = TimeTracker(IchinoseSatotani, graph, columns,
                      log_level=LOG_LEVEL, force_update=False, greedy=True)
tracker.track(steps=n_steps)
tracker.dump(filename)
