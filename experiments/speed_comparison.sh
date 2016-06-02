#!/bin/bash
PID=""
for i in {1..5}
do
    python -u experiment2.py tabu$i.us.csv > progress$i.log.csv &
    PID="$PID $!"
done
wait $PID

PID=""
for i in {6..10}
do
    python -u experiment2.py tabu$i.us.csv > progress$i.log.csv &
    PID="$PID $!"
done
wait $PID

CSVIN=""
for i in {1..10}
do
    CSVIN="$CSVIN tabu$i.us.csv"
done
CSVOUT="tabu.us.csv"
python csvmerge.py $CSVIN $CSVOUT
