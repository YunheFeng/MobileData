#!/bin/sh

date > log
python main.py xuzhou 1 >> log & 
PID1=$!
python main.py yancheng 1 >> log & 
PID2=$!
python main.py taizhou 1 >> log &
PID3=$!
wait $PID1
wait $PID2
wait $PID3

python main.py all_city 0 >> log

date > results/speed_vol.txt
python main.py xuzhou 2 >> results/speed_vol.txt & 
PID1=$!
python main.py yancheng 2 >> results/speed_vol.txt & 
PID2=$!
python main.py taizhou 2 >> results/speed_vol.txt &
PID3=$!
python main.py all_city 2 >> results/speed_vol.txt &
PID4=$!
wait $PID1
wait $PID2
wait $PID3
wait $PID4

date > results/speed_gap.txt
python main.py xuzhou -1 >> results/speed_gap.txt & 
PID1=$!
python main.py yancheng -1 >> results/speed_gap.txt & 
PID2=$!
python main.py taizhou -1 >> results/speed_gap.txt &
PID3=$!
python main.py all_city -1 >> results/speed_gap.txt &
PID4=$!
wait $PID1
wait $PID2
wait $PID3
wait $PID4

