import numpy as np
import argparse
import time

def load_data(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())

    processing_times = []
    deadlines = []
    for i in range(1, n + 1):
        p, d = map(int, lines[i].strip().split())
        processing_times.append(p)
        deadlines.append(d)

    setup_times = []
    for i in range(n + 1, len(lines)):
        setup_times.append(list(map(int, lines[i].strip().split())))
    
    setup_times = np.array(setup_times)
    
    return n, processing_times, deadlines, setup_times

def save_results(output_file, sequence, total_delay):
    with open(output_file, 'w') as file:
        file.write(f"{total_delay}\n")
        
        file.write(" ".join(map(lambda task: str(task + 1), sequence)) + '\n')

def calculate_delay(completion_time, deadline, processing_time):
    delay = max(0, completion_time - deadline)
    return min(processing_time, delay)

def greedy_scheduling(n, processing_times, deadlines, setup_times):
    available_tasks = set(range(n))
    sequence = []
    current_time = 0
    current_task = None
    total_delay = 0
    
    while available_tasks:
        min_cost = float('inf')
        next_task = None

        for task in available_tasks:
            if current_task is None:
                cost = 0
            else:
                setup_time = setup_times[current_task][task]
                cost = setup_time

            completion_time = current_time + cost + processing_times[task]
            delay = calculate_delay(completion_time, deadlines[task], processing_times[task])

            total_cost = cost + delay
            
            if total_cost < min_cost:
                min_cost = total_cost
                next_task = task

        if current_task is None:
            current_time += processing_times[next_task]
        else:
            current_time += setup_times[current_task][next_task] + processing_times[next_task]
        
        current_task = next_task
        sequence.append(current_task)
        total_delay += calculate_delay(current_time, deadlines[current_task], processing_times[current_task])
        available_tasks.remove(current_task)

    return sequence, total_delay

def main(input_file, output_file):
    n, processing_times, deadlines, setup_times = load_data(input_file)

    best_sequence, best_delay = greedy_scheduling(n, processing_times, deadlines, setup_times)
    save_results(output_file, best_sequence, best_delay)

if __name__ == "__main__":
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Path to the input file containing tasks data.')
    parser.add_argument('output_file', type=str, help='Path to the output file where the results will be saved.')
    parser.add_argument('time_limit', type=float, help='Time limit according to task in program')
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    time_limit = args.time_limit
    main(input_file, output_file)
    end = time.perf_counter()
    print('Czas wykonania: ', (end - start))
    if (end - start) > time_limit:
        print('Przekroczono limit czasu!')

