#!/usr/bin/env bash

for file in "instances"/*; do
  if [ ! -f "$file" ]; then
    continue
  fi

  # echo "Processing file: $file"

  numbers=$(echo "$file" | sed -E 's/.*_([0-9]+)_([0-9]+)\.txt/\1 \2/')
  num1=$(echo $numbers | cut -d ' ' -f 1)
  num2=$(echo $numbers | cut -d ' ' -f 2)

  echo $num1 $num2 $(./build/weryfikator $file "./solutions/out_$num2")
  # echo $num1
  # echo $num2
done
