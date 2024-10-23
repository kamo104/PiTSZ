#!/usr/bin/env bash

# arg 1 is the index
# arg 2 is the field to cut 1==time 2==score

cat run-log.txt | awk 'NF == 4' | grep "out/"$1 | sed 's/\.txt$//' | sed "s/out\/$1\.py_in_151908_//" | sort -t ' ' -k3 -n | cut -d ' ' -f 3,4 --complement | cut -d' ' -f $2
