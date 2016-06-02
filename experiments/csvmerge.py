from __future__ import print_function, division
import sys

def load_csv(filename):
    try:
        with open(filename) as fp:
            col = fp.readline().strip().split(',')[1:] # header line
            csv = fp.read().splitlines()
        csvdata = list(map(lambda l: l.split(','), csv))
        rowdata = map(lambda r: map(float, r), list(zip(*csvdata))[1:])
    except:
        col = None
        rowdata = None
    return col, rowdata

csvdata = filter(lambda e: e[0],
                 map(load_csv, sys.argv[1:-1]))

cols = list(zip(*csvdata))[0]
for c in cols:
    if c != cols[0]:
        raise Exception('not same csv columns')
col = cols[0]

# len(rowdata) means the number of valid csv files
rowdata = list(zip(*csvdata))[1]
rowdata = map(
    lambda r: map(
        lambda x: sum(x) / len(rowdata), zip(*r)),
        zip(*rowdata))

# convert point into string
rlist = map(lambda r: ','.join(map(str, r)), zip(*rowdata))
tlist = map(str, range(len(rlist)))
# write
with open(sys.argv[-1], 'w') as fp:
    fp.write('t,%s\n'%','.join(col)+\
             '\n'.join(map(','.join, zip(tlist, rlist))))

