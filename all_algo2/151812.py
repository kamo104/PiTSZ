import random
import threading
import sys
import time

stop_event = threading.Event()

def read_instance_file(instance_path):
    with open(instance_path, 'r') as file:
        n = int(file.readline().strip())
        
        tasks_times = []
        for _ in range(n):
            line = file.readline().strip().split()
            line = list(map(int, line))
            tasks_times_on_each_machine = line[0:5]
            temp = [tasks_times_on_each_machine, line[5], line[6]]
            tasks_times.append(temp)
    return n, tasks_times

def get_delay(scheduled_tasks, tasks_times, machine_number):
    c_value = 0
    previous_end_time = 0

    for current_task in scheduled_tasks:
        current_task_time = tasks_times[current_task - 1][0][machine_number]
        current_task_start_time = tasks_times[current_task - 1][1]
        
        previous_end_time = max(previous_end_time, current_task_start_time)
        end_time = previous_end_time + current_task_time
        previous_end_time = end_time
        
        expected_end_time = tasks_times[current_task - 1][2]
        
        if end_time > expected_end_time:
            c_value += 1
            
    return c_value

def schedule_tasks(n, tasks_times, result):
    best_sequence = list(range(1, n + 1))
    min_delay = float('inf')

    while not stop_event.is_set():
        sequence = list(range(1, n + 1))
        random.shuffle(sequence)
        
        scheduled_tasks_per_machine = [[] for _ in range(5)]

        for task_index, machine_number in enumerate(sequence):
            scheduled_tasks_per_machine[machine_number % 5].append(task_index + 1)

        total_delay = 0
        for machine_number in range(5):
            delay = get_delay(scheduled_tasks_per_machine[machine_number], tasks_times, machine_number)
            total_delay += delay

        if total_delay < min_delay:
            min_delay = total_delay
            best_sequence = scheduled_tasks_per_machine
            result["schedule"] = min_delay, best_sequence

    result["schedule"] = min_delay, best_sequence
    return min_delay, best_sequence

def save_results(output_path, min_delay, best_sequence):
    with open(output_path, 'w') as file:
        file.write(f"{min_delay}\n")
        for machine_schedule in best_sequence:
            file.write(' '.join(map(str, machine_schedule)) + '\n')


def run_with_timeout(output_path, n, tasks_times, time_limit):
    result = {}
    thread = threading.Thread(target=schedule_tasks, args=(n, tasks_times, result))
    thread.start()
    
    thread.join(time_limit)
    
    if thread.is_alive():
        stop_event.set()
        thread.join()
        
        min_delay, best_sequence = result['schedule']
        save_results(output_path, min_delay, best_sequence)
    else:
        min_delay, best_sequence = result['schedule']
        save_results(output_path, min_delay, best_sequence)

def main():
    start_time = time.time()

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    time_limit = int(sys.argv[3])
    time_limit = time_limit * 0.8
    n, tasks_times = read_instance_file(input_path)
    run_with_timeout(output_path, n, tasks_times, time_limit)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Time elapsed: {execution_time:.6f}")
    
   
if __name__ == "__main__":
    main()
