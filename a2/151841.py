import time

start_time = time.time()

import sys
import random
import math
import copy

def read_instance(instance_filename):
    with open(instance_filename, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    tasks = []
    for idx, line in enumerate(lines[1:], start=1):
        values = list(map(int, line.strip().split()))
        pkj = values[:5]
        rj = values[5]
        dj = values[6]
        tasks.append({
            'id': idx - 1,
            'pkj': pkj,
            'rj': rj,
            'dj': dj
        })
    return n, tasks

def calculate_delay(tasks, schedule):
    total_delay = 0
    num_workers = 5
    worker_available_time = [0] * num_workers
    task_list = tasks
    for worker in range(num_workers):
        for task_id in schedule[worker]:
            task = task_list[task_id]
            pkj = task['pkj'][worker]
            rj = task['rj']
            dj = task['dj']
            start_time = max(worker_available_time[worker], rj)
            finish_time = start_time + pkj
            worker_available_time[worker] = finish_time
            if finish_time > dj:
                total_delay += 1
    return total_delay

def generate_initial_schedule(tasks):
    num_workers = 5
    comparers = [
        lambda task: task['dj'],
        lambda task: -max(task['pkj']),
        lambda task: task['dj'] - task['rj'],
        lambda task: task['rj'],
    ]
    min_delay = float("inf")
    best_schedule = None
    for comparer in comparers:
        schedule = [[] for _ in range(num_workers)]
        worker_available_time = [0] * num_workers
        sorted_tasks = sorted(tasks, key=comparer)
        for task in sorted_tasks:
            best_worker = None
            earliest_finish_time = float('inf')
            for worker in range(num_workers):
                pkj = task['pkj'][worker]
                start_time = max(worker_available_time[worker], task['rj'])
                finish_time = start_time + pkj
                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    best_worker = worker
            schedule[best_worker].append(task['id'])
            worker_available_time[best_worker] = earliest_finish_time
        delay = calculate_delay(tasks, schedule)
        if delay < min_delay:
            min_delay = delay
            best_schedule = schedule
    return best_schedule

def calculate_worker_times(schedule, tasks, worker):
    times = []
    current_time = 0
    task_list = tasks
    for task_id in schedule[worker]:
        task = task_list[task_id]
        pkj = task['pkj'][worker]
        rj = task['rj']
        start_time = max(current_time, rj)
        finish_time = start_time + pkj
        times.append((task_id, start_time, finish_time))
        current_time = finish_time
    return times

def calculate_worker_lateness(worker_times_list, tasks):
    total_lateness = 0
    task_list = tasks
    for task_id, start_time, finish_time in worker_times_list:
        dj = task_list[task_id]['dj']
        if finish_time > dj:
            total_lateness += 1
    return total_lateness

def calculate_lateness(schedule, tasks):
    total_lateness = 0
    num_workers = 5
    worker_times = [None] * num_workers
    for worker in range(num_workers):
        worker_times[worker] = calculate_worker_times(schedule, tasks, worker)
        total_lateness += calculate_worker_lateness(worker_times[worker], tasks)
    return total_lateness, worker_times

def perturb_schedule(schedule, num_workers):
    action = random.choice([1, 2])
    if action == 1:
        worker1, worker2 = random.sample(range(num_workers), 2)
        if schedule[worker1] and schedule[worker2]:
            idx1 = random.randrange(len(schedule[worker1]))
            idx2 = random.randrange(len(schedule[worker2]))
            change = (1, worker1, worker2, idx1, idx2)
            return change
    elif action == 2:
        worker = random.randrange(num_workers)
        if len(schedule[worker]) >= 2:
            idx1, idx2 = random.sample(range(len(schedule[worker])), 2)
            change = (2, worker, idx1, idx2)
            return change
    return None

def apply_change(schedule, change):
    if change[0] == 1:
        _, w1, w2, idx1, idx2 = change
        schedule[w1][idx1], schedule[w2][idx2] = schedule[w2][idx2], schedule[w1][idx1]
    elif change[0] == 2:
        _, w, idx1, idx2 = change
        schedule[w][idx1], schedule[w][idx2] = schedule[w][idx2], schedule[w][idx1]

def reverse_change(schedule, change):
    apply_change(schedule, change)

def simulated_annealing_solver(n, tasks, max_time):
    num_workers = 5
    current_schedule = generate_initial_schedule(tasks)
    current_lateness, worker_times = calculate_lateness(current_schedule, tasks)
    best_schedule = copy.deepcopy(current_schedule)
    best_lateness = current_lateness
    T = 750 + n
    cooling_rate = 1 - (5 / (n * n * (n // 100 + 1)))
    while time.time() - start_time < max_time:
        change = perturb_schedule(current_schedule, num_workers)
        if change is None:
            continue
        if change[0] == 1:
            _, worker1, worker2, idx1, idx2 = change
            affected_workers = [worker1, worker2]
        elif change[0] == 2:
            _, worker, idx1, idx2 = change
            affected_workers = [worker]
        else:
            affected_workers = []
        worker_times_before = [worker_times[w][:] for w in affected_workers]
        lateness_before = []
        for i, worker in enumerate(affected_workers):
            lateness_before.append(calculate_worker_lateness(worker_times_before[i], tasks))
        apply_change(current_schedule, change)
        delta_lateness = 0
        for i, worker in enumerate(affected_workers):
            worker_times[worker] = calculate_worker_times(current_schedule, tasks, worker)
            lateness_after = calculate_worker_lateness(worker_times[worker], tasks)
            delta_lateness += lateness_after - lateness_before[i]
        new_lateness = current_lateness + delta_lateness
        delta = new_lateness - current_lateness
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_lateness = new_lateness
            if new_lateness < best_lateness:
                best_schedule = copy.deepcopy(current_schedule)
                best_lateness = new_lateness
        else:
            reverse_change(current_schedule, change)
            for i, worker in enumerate(affected_workers):
                worker_times[worker] = worker_times_before[i]
        T *= cooling_rate
    elapsed_time = time.time() - start_time
    print(f"Simulated Annealing completed after {elapsed_time:.2f} seconds.")
    return best_lateness, best_schedule

def write_solution(total_Uj, schedule, solution_filename):
    with open(solution_filename, 'w') as f:
        f.write(f"{total_Uj}\n")
        for worker_tasks in schedule:
            line = ' '.join(str(task_id + 1) for task_id in worker_tasks)
            f.write(f"{line}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python simulated_annealing_solver.py <instance_file> <solution_file> <max_time>")
        sys.exit(1)
    instance_filename = sys.argv[1]
    solution_filename = sys.argv[2]
    max_time = float(sys.argv[3])
    try:
        n, tasks = read_instance(instance_filename)
        total_Uj, schedule = simulated_annealing_solver(n, tasks, max_time - 0.2)
        write_solution(total_Uj, schedule, solution_filename)
        print(f"Solution saved to {solution_filename}")
        print(f"Total Uj (number of late tasks): {total_Uj}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
