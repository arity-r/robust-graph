import matplotlib.pyplot as plt
import numpy as np

with open('result.csv') as fp:
    #                                t                           r                       R
    fp.readline()
    result = np.array(map(lambda l: (int(l.split(',')[0]), float(l.split(',')[1]), float(l.split(',')[2])),
                       fp.read().splitlines()))

with open('result_ref.csv') as fp:
    #                                    Tabu Search                   Greedy Algorithm
    fp.readline()
    result_ref = np.array(map(lambda l: (float(l.split(',')[0]), float(l.split(',')[1])),
                       fp.read().splitlines()))

t = result[:, 0]
r = result[:, 1]
R = result[:, 2]
tabu_search = result_ref[:, 0]
greedy = result_ref[:, 1]

"""
plt.plot(t, tabu_search, 'ro')
plt.plot(t, greedy, 'bo')
plt.plot(t, R, 'go')
plt.legend(['Tabu Search', 'Greedy Algorithm', 'Unnamed Algorithm'], loc='lower right')
plt.xlabel('Number of Steps')
plt.ylabel('$R$')
"""

plt.plot(t, R, 'r-', label='$R$')
plt.xlabel('Number of Swaps')
plt.ylabel('$R$')
h1, l1 = plt.gca().get_legend_handles_labels()
par = plt.twinx()
par.plot(t, r, 'b-', label='$r$')
par.set_ylabel('$r$')

h2, l2 = par.get_legend_handles_labels()
plt.legend(h1+h2, l1+l2, loc='upper left')
plt.show()

