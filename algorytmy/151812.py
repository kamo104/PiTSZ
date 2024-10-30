import threading
import sys
import time
from collections import deque

stop_event = threading.Event()

def read_instance_file(instance_path):
    with open(instance_path, 'r') as file:
        n = int(file.readline().strip())
        
        tasks_times = []
        for _ in range(n):
            start_time, end_time = map(int, file.readline().strip().split())
            tasks_times.append((start_time, end_time))
        
        distance_matrix = []
        for _ in range(n):
            row = list(map(int, file.readline().strip().split()))
            distance_matrix.append(row)
    
    return n, tasks_times, distance_matrix

def topological_sort(tasks, setup_times):
    print(tasks, setup_times)
    queue = deque()
    queue.append(0)
    sorted_order = []
    visited = [False] * len(tasks)


    while queue:
        if stop_event.is_set():
            break
        
        node = queue.popleft()
        
        # current_time += tasks[node - 1]
        # print(setup_times[node])
        
        visited[node] = True
        sorted_order.append(node + 1)
        
        summed_list = [a + b[0] for a, b in zip(setup_times[node], tasks)]
        
        filtered_indices = [i for i in range(len(summed_list)) if not visited[i]]
        if(len(filtered_indices) > 0):
            min = filtered_indices[0]
            for i in range(len(summed_list)):
                if(not visited[i] and summed_list[i] <= summed_list[min] ): # and tasks[i][1] <= tasks[min][1]
                    min = i
                    
            queue.append(min)
    return sorted_order

def greedy_scheduling(tasks, setup_times, result, stop_event):
    # sorted_tasks = sorted(tasks, key=lambda task: task[1])
    # sorted_tasks = [x[0] for x in sorted_tasks]
    sorted_tasks = topological_sort(tasks, setup_times)
    # print(sorted_tasks)
    result['schedule'] = sorted_tasks
    
    return 0, sorted_tasks


def get_tasks_end_times(scheduled_tasks, tasks_times, distance_matrix):
    # print(scheduled_tasks)
    # print(tasks_times)
    # print(distance_matrix)
    
    end_times = [] 
    scheduled_tasks = list(scheduled_tasks)

    first_task = scheduled_tasks[0]
    end_times.append(tasks_times[first_task - 1][0])
    # print(first_task)
    # print(tasks_times)
    # print(end_times)
    # print(scheduled_tasks)
    for i in range(1, len(scheduled_tasks)):
        previous_task = scheduled_tasks[i - 1]
        current_task = scheduled_tasks[i]

        previous_end_time = end_times[i - 1]
        transition_time = distance_matrix[previous_task - 1][current_task - 1]
        # print(f"transition from {previous_task} to {current_task} takes: {transition_time}")
        actual_start_time = previous_end_time + transition_time  
        end_time = actual_start_time + tasks_times[current_task - 1][0]
        # print(f"startTime {actual_start_time} endTime: {end_time}")

        end_times.append(end_time)

    # print(end_times)
    return end_times
    
def calculate_delay_criterion(n, scheduled_tasks, tasks_times, end_times):
    # print(n, tasks_times, end_times, scheduled_tasks)
    delay_criterion = 0
    for i in range(len(scheduled_tasks)):
        task_index = scheduled_tasks[i] - 1
        job_duration = tasks_times[task_index][0]
        part_of_criterion = min(job_duration, max(0, end_times[i] - tasks_times[task_index][1]))
        # print(i, part_of_criterion, job_duration, end_times[task_index], tasks_times[task_index][1])
        delay_criterion += part_of_criterion 
    return delay_criterion
        
def create_result_file(filename, delay_criterion, scheduled_tasks):
    with open(filename, 'w') as file:
        file.write(str(delay_criterion))
        file.write("\n")
        file.write(' '.join(map(str, scheduled_tasks)))

def run_with_timeout(tasks_times, distance_matrix, time_limit):
    result = {}
    thread = threading.Thread(target=greedy_scheduling, args=(tasks_times, distance_matrix, result, stop_event))
    thread.start()

    thread.join(time_limit)

    if thread.is_alive():
        stop_event.set()
        thread.join()
        scheduled_tasks = result['schedule']
        print(scheduled_tasks)
        
        end_times = get_tasks_end_times(scheduled_tasks, tasks_times, distance_matrix)
        delay_criterion = calculate_delay_criterion(n, scheduled_tasks, tasks_times, end_times)
        create_result_file(result_file, delay_criterion, scheduled_tasks)
    else:
        # print(f"Wynik: {result}")
        scheduled_tasks = result['schedule']
        end_times = get_tasks_end_times(scheduled_tasks, tasks_times, distance_matrix)
        delay_criterion = calculate_delay_criterion(n, scheduled_tasks, tasks_times, end_times)
        create_result_file(result_file, delay_criterion, scheduled_tasks)

start_time = time.time()

instance_file = sys.argv[1]
result_file = sys.argv[2]
time_limit = int(sys.argv[3])

n, tasks_times, distance_matrix = read_instance_file(instance_file)

run_with_timeout(tasks_times, distance_matrix, time_limit)

end_time = time.time()
execution_time = end_time - start_time

print(f"Time elapsed: {execution_time:.6f}")