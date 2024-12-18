import sys
import random
import math
import time

def load_instance(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_tasks = int(lines[0].strip())
    global N
    N = num_tasks
    tasks_info = {}
    
    for idx, line in enumerate(lines[1:], start=1):
        values = list(map(int, line.strip().split()))
        task_duration = values[:5]
        ready_time = values[5]
        deadline = values[6]
        max_duration = max(task_duration)
        
        tasks_info[idx] = {
            'durations': task_duration,
            'ready_time': ready_time,
            'deadline': deadline,
            'max_duration': max_duration
        }
        
    return num_tasks, tasks_info


def annealing_schedule_solver(num_tasks, tasks_info, time_limit):
    num_workers = 5
    initial_schedule = {worker: [] for worker in range(1, num_workers + 1)}

    for task_id in range(1, num_tasks + 1):
        worker_assigned = random.randint(1, num_workers)
        initial_schedule[worker_assigned].append(task_id)

    def compute_lateness(schedule):
        lateness = 0
        worker_times = {worker: 0 for worker in range(1, num_workers + 1)}

        for worker, assigned_tasks in schedule.items():
            for task_id in assigned_tasks:
                task = tasks_info[task_id]
                task_duration = task['durations'][worker - 1]
                ready_time = task['ready_time']
                deadline = task['deadline']

                start_time = max(worker_times[worker], ready_time)
                finish_time = start_time + task_duration

                worker_times[worker] = finish_time

                if finish_time > deadline:
                    lateness += 1

        return lateness

    def modify_schedule(schedule):
        new_schedule = {worker: tasks[:] for worker, tasks in schedule.items()}
        worker1, worker2 = random.sample(range(1, num_workers + 1), 2)

        if new_schedule[worker1] and new_schedule[worker2]:
            task1 = random.choice(new_schedule[worker1])
            task2 = random.choice(new_schedule[worker2])

            new_schedule[worker1].remove(task1)
            new_schedule[worker1].append(task2)

            new_schedule[worker2].remove(task2)
            new_schedule[worker2].append(task1)

        return new_schedule

    temperature = 100.0
    cooling_factor = 0.95
    start_time = time.time()

    current_schedule = initial_schedule
    current_lateness = compute_lateness(current_schedule)

    best_schedule = current_schedule
    best_lateness = current_lateness

    while time.time() - start_time < time_limit:
        modified_schedule = modify_schedule(current_schedule)
        modified_lateness = compute_lateness(modified_schedule)

        if modified_lateness < current_lateness:
            current_schedule = modified_schedule
            current_lateness = modified_lateness
            if modified_lateness < best_lateness:
                best_schedule = modified_schedule
                best_lateness = modified_lateness
        else:
            delta_lateness = modified_lateness - current_lateness
            acceptance_prob = math.exp(-delta_lateness / temperature)

            if random.random() < acceptance_prob:
                current_schedule = modified_schedule
                current_lateness = modified_lateness

        temperature *= cooling_factor

    elapsed_time = time.time() - start_time    
    return best_lateness, best_schedule


def save_solution(total_lateness, schedule, output_file):
    with open(output_file, 'w') as file:
        file.write(f"{total_lateness}\n")
        for worker_id in range(1, 6):
            task_sequence = schedule.get(worker_id, [])
            file.write(f"{' '.join(map(str, task_sequence))}\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    max_time = float(sys.argv[3])

    try:
        num_tasks, tasks_info = load_instance(input_file)
        total_lateness, final_schedule = annealing_schedule_solver(num_tasks, tasks_info, max_time)
        save_solution(total_lateness, final_schedule, output_file)
    except Exception as error:
        sys.exit(1)
