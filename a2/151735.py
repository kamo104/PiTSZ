import argparse
import random
import copy
import math
import time

def read_problem_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    tasks = []

    for line in lines[1:n+1]:
        values = list(map(int, line.split()))
        p_kj = values[:5]
        r_j = values[5]
        d_j = values[6]
        tasks.append((p_kj, r_j, d_j))

    return tasks

# Sortowanie
def init_solution(tasks):
    tasks_with_indices = [(i + 1, tasks[i]) for i in range(len(tasks))]
    tasks_with_indices.sort(key=lambda x: x[1][2])

    sequences = [[] for _ in range(5)]
    current_times = [0] * 5
    total_late_jobs = 0

    for task_index, (p_kj, r_j, d_j) in tasks_with_indices:
        best_worker = -1
        best_finish_time = float('inf')
        for i in range(5):
            start_time = max(current_times[i], r_j)
            finish_time = start_time + p_kj[i]
            if finish_time < best_finish_time:
                best_finish_time = finish_time
                best_worker = i

        sequences[best_worker].append(task_index)
        current_times[best_worker] = best_finish_time

        if best_finish_time > d_j:
            total_late_jobs += 1

    return sequences, total_late_jobs

def save_solution_to_file(total_late_jobs, sequences, output_path):
    with open(output_path, 'w') as file:
        file.write(f"{total_late_jobs}\n")
        for seq in sequences:
            file.write(" ".join(map(str, seq)) + "\n")

# Część wyrzarzania
def calculate_late_tasks(solution, tasks):
    total_late = 0
    current_times = [0] * 5

    for i, sequence in enumerate(solution):
        for task_index in sequence:
            p_kj, r_j, d_j = tasks[task_index - 1]
            start_time = max(current_times[i], r_j)
            finish_time = start_time + p_kj[i]
            if finish_time > d_j:
                total_late += 1
            current_times[i] = finish_time

    return total_late

def generate_neighbors(schedule):
    neighbors = []
    for i, sequence in enumerate(schedule):
        for task in sequence:
            for j in range(len(schedule)):
                if i != j:
                    new_schedule = copy.deepcopy(schedule)
                    new_schedule[i].remove(task)
                    new_schedule[j].append(task)
                    neighbors.append(new_schedule)
    return neighbors

def solve(initial_schedule, initial_late_jobs, tasks, current_time, time_limit, init_temperature=100, cooling_rate=0.95, max_iter=1000):
    current_solution = copy.deepcopy(initial_schedule)
    current_cost = initial_late_jobs
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost

    temperature = init_temperature

    for _ in range(max_iter):
            neighbors = generate_neighbors(current_solution)
            if not neighbors:
                break
            new_solution = random.choice(neighbors)
            new_cost = calculate_late_tasks(new_solution, tasks)

            delta = new_cost - current_cost
            acceptance_probability = math.exp(-delta / temperature) if delta > 0 else 1

            if random.random() < acceptance_probability:
                current_solution = new_solution
                current_cost = new_cost

            if current_cost < best_cost:
                best_solution = copy.deepcopy(current_solution)
                best_cost = current_cost

            if best_cost == 0 or (time.time() - current_time > time_limit):
                return best_solution, best_cost

            temperature *= cooling_rate

    return best_solution, best_cost

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_file', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('time', type=float)
    args = parser.parse_args()

    start = time.time()

    tasks = read_problem_file(args.problem_file)
    initial_solution, initial_late_jobs = init_solution(tasks)
    final_sequences, final_late_jobs = solve(initial_solution, initial_late_jobs, tasks, start, args.time)
    save_solution_to_file(final_late_jobs, final_sequences, args.output_file)

if __name__ == '__main__':
    main()
