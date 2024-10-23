#!/usr/bin/env bash

cat run-log.txt | awk 'NF == 4' | grep ""$1  | sort -t '_' -k 3n | cut -f 1 -d' ' | tr -d 's'

