#!/bin/bash

for i in {1..10}
do
    python experiment2.ba.py make_graph exp2.graph$i.pkl
done

for algorithm in sun ichinose ichinose_greedy
do
    PID=""
    for i in {1..5}
    do
        # simulate (algorithm name) (input graph) (output csv)
        python -u experiment2.ba.py simulate $algorithm\
               exp2.graph$i.pkl $algorithm$i.ba.csv\
               > $algorithm$i.log.csv &
        PID="$PID $!"
    done
    wait $PID

    PID=""
    for i in {6..10}
    do
        # simulate (algorithm name) (input graph) (output csv)
        python -u experiment2.ba.py simulate $algorithm\
               exp2.graph$i.pkl $algorithm$i.ba.csv\
               > $algorithm$i.log.csv &
        PID="$PID $!"
    done
    wait $PID

    CSVIN=""
    for i in {1..10}
    do
        CSVIN="$CSVIN $algorithm$i.ba.csv"
    done
    CSVOUT="$algorithm.ba.csv"
    python csvmerge.py $CSVIN $CSVOUT
done
