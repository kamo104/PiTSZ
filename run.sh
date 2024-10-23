#!/usr/bin/env bash

# Directories
prog_dir="algorytmy1"
instances_dir="my_instances"
output_dir="out"

mkdir -p "$output_dir"

for f1 in "$prog_dir"/*; do
    f1_name=$(basename "$f1")
    if [[ "$f1" == *.py ]]; then
        prefix="python ./$f1"
    else
        prefix="./$f1"
    fi
    for f2 in "$instances_dir"/*; do
        f2_name=$(basename "$f2")
        output_file="$output_dir/out_${f1_name}_${f2_name}"

        # Create the full command string
        command="$prefix $f2 $output_file 5"
        
        # $command
        # real_time=$( (time $command > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')
        
        # # Print only the real time
        # # echo "Command: $command"
        # echo "time: $real_time $output_file"


        # Run command in the background
        {
            real_time=$( (time $command > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')
            echo "time: $real_time $output_file"
        } &

        # Ensure no more than $max_jobs are running at once
        while [[ $(jobs -r -p | wc -l) -ge $(nproc) ]]; do
            wait -n
        done        
    done
done
