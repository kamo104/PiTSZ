import time
import random
import argparse
import math


def read_input_data(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    tasks = []
    for line in lines[1:]:
        data = list(map(int, line.strip().split()))
        p_values = data[:5]
        r = data[5]
        d = data[6]
        tasks.append((p_values, r, d))
    return n, tasks

def calculate_u(tasks, worker_sequences):
    num_workers = len(worker_sequences)
    worker_end_times = [0] * num_workers
    u_sum = 0
    completed = [0] * len(tasks)
    for worker, sequence in enumerate(worker_sequences):
        for task_id in sequence:  # task_id should be an integer
            #print(task_id)
            task = tasks[task_id - 1]
            p_kj = task[0][worker]
            r_j = task[1]
            d_j = task[2]

            start_time = max(worker_end_times[worker], r_j)
            end_time = start_time + p_kj
            worker_end_times[worker] = end_time
            if end_time > d_j:
                u_sum += 1

            completed[task_id - 1] += 1
            if completed[task_id - 1] > 1:
                return "Error: task already done!"
    for count in completed:
        if count < 1:
            return "Error: task not completed!"

    return u_sum

## Heurystyka: minimalny czas zakończenia
## Sortowanie po pracownikach, którzy mogą najszybciej skończyć zadanie, biorąc pod uwagę gotowość
def greedy(tasks):
    worker_assignments = [[] for _ in range(5)]
    worker_end_times = [0] * 5
    for task_id, task in enumerate(tasks, start=1):
        p_values, r_j, d_j = task
        best_worker = None
        min_end_time = float('inf')

        for worker in range(5):
            start_time = max(worker_end_times[worker], r_j)
            end_time = start_time + p_values[worker]

            if end_time < min_end_time:
                min_end_time = end_time
                best_worker = worker
        worker_assignments[best_worker].append(task_id)
        worker_end_times[best_worker] = min_end_time
    return worker_assignments

## Heurystyka: najwcześniejszy deadline
## Sortowanie rosnąco według deadline'u, a następnie przydzielanie zadań by minimalizować zakończenie
def edd(tasks):
    n_tasks = len(tasks)
    n_workers = 5
    worker_assignments = [[] for _ in range(n_workers)]
    worker_end_times = [0] * n_workers
    unassigned_tasks = set(range(n_tasks))
    sorted_tasks = sorted(unassigned_tasks, key=lambda task_id: tasks[task_id][2])  # tasks[task_id][2] = d_j

    for task_id in sorted_tasks:
        task = tasks[task_id]
        best_worker = None
        best_end_time = float('inf')
        for worker in range(n_workers):
            p_kj = task[0][worker]
            r_j = task[1]
            start_time = max(worker_end_times[worker], r_j)
            end_time = start_time + p_kj

            if end_time < best_end_time:
                best_end_time = end_time
                best_worker = worker
        worker_assignments[best_worker].append(task_id + 1)
        worker_end_times[best_worker] = best_end_time

    return worker_assignments

## Heurystyka: Po sumie ważonej czasu gotowości i opóźnienia: opóźnienie + 0.5 * (czas_rozpoczęcia - rj)
## Sortowanie po minimalnej wartości score
def weighted_penalty(tasks):
    n_tasks = len(tasks)
    n_workers = 5
    worker_assignments = [[] for _ in range(n_workers)]
    worker_end_times = [0] * n_workers
    unassigned_tasks = set(range(n_tasks))

    while unassigned_tasks:
        best_score = float('inf')
        best_worker = None
        best_task = None

        for task_id in unassigned_tasks:
            task = tasks[task_id]
            for worker in range(n_workers):
                p_kj = task[0][worker]
                r_j = task[1]
                d_j = task[2]
                start_time = max(worker_end_times[worker], r_j)
                end_time = start_time + p_kj
                delay = max(0, end_time - d_j)

                score = delay + (start_time - r_j) * 0.5
                if score < best_score:
                    best_score = score
                    best_worker = worker
                    best_task = task_id
        worker_assignments[best_worker].append(best_task + 1)
        worker_end_times[best_worker] = max(worker_end_times[best_worker], tasks[best_task][1]) + tasks[best_task][0][best_worker]
        unassigned_tasks.remove(best_task)

    return worker_assignments

## Lokalne zmiany w sortowaniu na najlepszym podziale zadań
## Iteracyjna modyfikacja przypisań w losowy sposób
def random_modification(tasks, initial_assignments, max_time=4.0, initial_temp=100, cooling_rate=0.99):
    start_time = time.time()
    current_assignments = [list(worker) for worker in initial_assignments]
    best_assignments = [list(worker) for worker in initial_assignments]
    current_u = calculate_u(tasks, current_assignments)
    best_u = current_u
    temp = initial_temp

    while time.time() - start_time < max_time:
        new_assignments = [list(worker) for worker in current_assignments]
        worker1, worker2 = random.sample(range(5), 2)
        if new_assignments[worker1] and new_assignments[worker2]:
            task1 = random.choice(new_assignments[worker1])
            task2 = random.choice(new_assignments[worker2])
            new_assignments[worker1].remove(task1)
            new_assignments[worker2].remove(task2)
            new_assignments[worker1].append(task2)
            new_assignments[worker2].append(task1)

        new_u = calculate_u(tasks, new_assignments)
        if new_u < current_u or random.random() < math.exp((current_u - new_u) / temp):
            current_assignments = new_assignments
            current_u = new_u

            if new_u < best_u:
                best_assignments = new_assignments
                best_u = new_u
        temp *= cooling_rate

    return best_assignments, best_u


def save_results(filename, best_assignments, best_u_sum):
    with open(filename, "w") as file:
        file.write(f"{best_u_sum}\n")
        for worker_tasks in best_assignments:
            file.write(" ".join(map(str, worker_tasks)) + "\n")

start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
parser.add_argument("time")

args = parser.parse_args()
n, tasks = read_input_data(args.input_file)
#print(tasks)

assignments_edd = edd(tasks)
u_edd = calculate_u(tasks, assignments_edd)
#print(assignments_edd)
print(u_edd)

assignments_greedy = greedy(tasks)
u_greedy = calculate_u(tasks, assignments_greedy)
#print(assignments_greedy)
print(u_greedy)

assignments_wp = weighted_penalty(tasks)
u_wp = calculate_u(tasks, assignments_wp)
#print(assignments_wp)
print(u_wp)

if u_wp < u_edd and u_wp < u_greedy:
    assignments = assignments_wp
    u = u_wp
elif u_greedy < u_wp and u_greedy < u_edd:
    assignments = assignments_greedy
    u = u_greedy
else:
    assignments = assignments_edd
    u = u_edd
end_time = time.time() - start_time
assignments, u = random_modification(tasks, assignments, max_time=float(args.time)-end_time-float(args.time)/20)
#print(assignments_wp)
print(u)

save_results(args.output_file,assignments,u)
