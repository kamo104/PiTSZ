#!/usr/bin/env bash

# Directories
prog_dir="solutions3"
instances_dir="my_instances"
output_dir="out"
log_file="run-log.txt"
verifier_bin="algo3/pajton.py"
verifier_args="--program verifier"

mkdir -p "$output_dir"
rm "$log_file"
touch "$log_file"

# Function to run the command and log the results
run_command() {
    local f1_name="$1"
    local instance_file="$2"
    local output_file="$3"
    local prefix="$4"

   
    # time_limit = instance_size/10
    local time_limit=$(echo $instance_file | sed 's/[a-z_\/]*[0-9]*_//' | sed 's/\.txt/\/10/' | bc)
    # Create the full command string
    local command="$prefix $instance_file $output_file $time_limit"
    echo "CO SIE DZIEJE $command"

    # Capture execution time and results
    local time_str=$( (time $command > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')

    minutes=${time_str%%m*}
    seconds=${time_str##*m}
    seconds=${seconds//s/}
    seconds=${seconds//,/.}
    real_time=$(echo "$minutes * 60 + $seconds" | bc -l)
    real_time=${real_time//./,}

    local raported_score=$(head -n1 "$output_file")
    local real_score=$("python" "$verifier_bin" "--program" "verifier" "$instance_file" "$output_file")
    echo "HELP ME python algo2/pajton.py --program verifier $instance_file $output_file"
    echo "SCORE1: $raported_score"
    echo "SCORE2: $real_score"
    
    # Log the output
    echo "$real_time $raported_score $real_score $output_file" | tee -a "$log_file"
}

# Iterate over each program
for f1 in "$prog_dir"/*; do
    f1_name=$(basename "$f1")
    if [[ "$f1" == *.py ]]; then
        prefix="python ./$f1"
    else
        prefix="./$f1"
    fi

    # Iterate over each instance file
    for instance_file in "$instances_dir"/*; do
        instance_filename=$(basename "$instance_file")
        output_file="$output_dir/${f1_name}_${instance_filename}"

        # Run the command in the background
        {
            run_command "$f1_name" "$instance_file" "$output_file" "$prefix"
        } &

        # Ensure no more than $(nproc) jobs are running at once
        while [[ $(jobs -r -p | wc -l) -ge $(nproc) ]]; do
            wait -n
        done        
    done
done

wait
