#!/usr/bin/env bash
i=0
while [[ $((i+50)) -ne 550 ]]; do
  i=$((i+50))
  ./generator $i instances/in_151908_$i.txt
done
