from __future__ import print_function
import sys
import networkx as nx
# R robustness
from robust_graph import R

# log level: use LOG_LEVEL_DEBUG or LOG_LEVEL_VERBOSE
#            to get more information
#            use LOG_LEVEL_ERROR or LOG_LEVEL_WARNING
#            to reduce information
#            use LOG_LEVEL_QUIET to suppress all log
#from robust_graph.optimize import LOG_LEVEL_INFO as LOG_LEVEL
from robust_graph import LOG_LEVEL_VERBOSE as LOG_LEVEL

# opt. algorithms: see /robust_graph/optimize
from robust_graph import Schneider
from robust_graph import Sun
from robust_graph import IchinoseSatotani

# time tracker to track simulation
from robust_graph import TimeTracker

# function to load US airline network
from robust_graph import load_us

# some important constants
n_attacks = 10
n_steps = 30
filename = sys.argv[1]
# load graph
graph = load_us()
#graph = nx.barabasi_albert_graph(20, 3)

# define columns in csv
columns = [
    ('R', lambda G: R(G, n_attacks)),
    ('r', nx.degree_pearson_correlation_coefficient)
]
# use TimeTracker to track R and r
tracker = TimeTracker(Sun, graph, columns,
                      # configurations: see robust_graph.optimize.Sun
                      log_level=LOG_LEVEL,
                      force_update=True,
                      max_trials=1000,
                      Nt=6, Ng=10)
tracker.track(steps=n_steps)

tracker.dump(filename) # in this time, tabu$i.us.csv
