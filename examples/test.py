from __future__ import print_function
import sys, networkx as nx

# robust measurement by schneider et.al.
from robust_graph import s, R
# log level: what kind of information are to be printed
# other options: VERBOSE, DEBUG, INFO, WARNING, ERROR
# e.g. WARNING: print warning and error information
from robust_graph import LOG_LEVEL_QUIET as LOG_LEVEL
# 4 optimizers based on 4 different algorithms
from robust_graph import Schneider, WuHolme, Sun, IchinoseSatotani
# measures certain index through optimization process
from robust_graph import TimeTracker
# function to load united states airline network
# and make powerlaw-degree-distribution network
from robust_graph import load_us, scale_free_network

# initialize graph object and algorithm object
G1 = scale_free_network()
R1 = R(G1, n=10) # calculate 10 times to get more accurate result

# use of optimizer
print('----- optimizer test -----')
print('original R =', R1)
for opt_cls in [Schneider, WuHolme, IchinoseSatotani]:
    # still there are more options
    # see robust_graph/optimize document
    optimizer = opt_cls(G1, log_level=LOG_LEVEL, max_trials=10)
    G2 = optimizer.optimize(steps=100)
    R2 = R(G2, n=10)
    print('optimized by', opt_cls.__name__, 'R =', R2)

# use of tracker
print('----- time tracker test -----')
# measurements used in timetracker
cols = [('R', lambda G: R(G, n=10)),                      # R robustness
        ('r', nx.degree_pearson_correlation_coefficient), # r degree correlation
       ]
# WuHolme is not iterative algorithm
for opt_cls in [Schneider, IchinoseSatotani]:
    # options are given after columns(measurements)
    tracker = TimeTracker(opt_cls, G1, cols=cols,
                          log_level=LOG_LEVEL, max_trials=5)
    tracker.track(steps=2)
    print('tracked by', opt_cls.__name__, 'algorithm...')
    print(tracker.dumps())
    # tracker.dump('test.csv') # also, tracker can dump to file

