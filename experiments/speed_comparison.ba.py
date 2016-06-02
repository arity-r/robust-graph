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
# function to print header row of log
from robust_graph import print_log_header

# opt. algorithms: see /robust_graph/optimize
from robust_graph import Schneider
from robust_graph import Sun
from robust_graph import IchinoseSatotani

# time tracker to track simulation
from robust_graph import TimeTracker

# function to load US airline network
from robust_graph import load_us

def make_and_dump_graph(n, m, filename):
    graph = nx.barabasi_albert_graph(n, m, filename)
    nx.write_gpickle(graph, filename)

def simulate_and_dump_result(algorithm, graph_filename, out_filename):
    # parsing valid algorithm
    if algorithm == 'sun':
        opt_class = Sun
        config = dict(log_level=LOG_LEVEL,
                      force_update=True, # update graph even if swap is not done
                      max_trials=1000,   # and continue even if swap is done
                      Nt=6, Ng=10)
        n_steps = 30

    elif algorithm == 'ichinose':
        opt_class = IchinoseSatotani
        config = dict(log_level=LOG_LEVEL,
                      force_update=False) # does not accept if swap is not done
        n_steps = 500

    elif algorithm == 'ichinose_greedy':
        opt_class = IchinoseSatotani
        config = dict(log_level=LOG_LEVEL,
                      greedy=True,        # greedy swapping
                      force_update=False) # same as above
        n_steps = 500

    else: raise ValueError('invalid algorithm: ', algorithm)

    # number of attacks (to calculate R)
    n_attacks = 10
    # load graph
    graph = nx.read_gpickle(graph_filename)
    # define columns in csv
    columns = [
        ('R', lambda G: R(G, n_attacks)),
        ('r', nx.degree_pearson_correlation_coefficient)
    ]
    # use TimeTracker to track R and r
    tracker = TimeTracker(opt_class, graph, columns, **config)
    tracker.track(steps=n_steps)
    tracker.dump(out_filename) # in this time, algorithm$i.ba.csv


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('type command: make_graph or simulate')

    command = sys.argv[1]
    if command == 'make_graph':
        if len(sys.argv) < 3:
            raise ValueError('insufficient arguments: make_graph <out_file>')
        out_file = sys.argv[2]
        make_and_dump_graph(n=500, m=3, filename=out_file)

    elif command == 'simulate':
        if len(sys.argv) < 5:
            raise ValueError(
                'insufficient arguments: simulate <algorithm> <graph_file> <out_file>')
        print_log_header()
        algorithm = sys.argv[2]
        graph_file = sys.argv[3]
        out_file = sys.argv[4]
        simulate_and_dump_result(algorithm, graph_file, out_file)
