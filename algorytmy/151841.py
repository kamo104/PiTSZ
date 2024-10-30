import time
import random
import sys

def read_instance(filename) -> tuple:
    try:
        with open(filename, 'r') as f:
            n = int(f.readline().strip())
            tasks = [tuple(map(int, f.readline().strip().split())) for _ in range(n)]
            setup_times = [list(map(int, f.readline().strip().split())) for _ in range(n)]
        return n, tasks, setup_times
    except Exception as e:
        print(f"Błąd podczas wczytywania instancji z pliku {filename}: {e}")
        sys.exit(1)


def write_solution_to_file(filename, Y, order):
    try:
        with open(filename, 'w') as f:
            f.write(f"{Y}\n")
            f.write(" ".join(map(str, order)) + "\n")
    except Exception as e:
        print(f"Błąd podczas zapisywania do pliku {filename}: {e}")
        sys.exit(1)


def hodgson_algorithm(n, tasks, setup_times) -> list[int]:
    job_indices = list(range(n))
    job_indices.sort(key=lambda x: tasks[x][1]) 

    E = []
    p = 0

    for j in job_indices:
        E.append(j)
        if len(E) >= 2:
            prev_job = E[-2]
            S_prev_j = setup_times[prev_job][j]
        else:
            S_prev_j = 0
        p += S_prev_j + tasks[j][0]

        if p > tasks[j][1]:
            longest_task = max(E, key=lambda x: tasks[x][0])
            E.remove(longest_task)
            if E:
                prev_job = E[-1]
                S_prev_longest = setup_times[prev_job][longest_task]
                p -= S_prev_longest + tasks[longest_task][0]
            else:
                p = 0

    scheduled_jobs = sorted(E, key=lambda x: tasks[x][1])
    remaining_jobs = [j for j in job_indices if j not in E]
    scheduled_jobs.extend(remaining_jobs)
    
    return scheduled_jobs


def calculate_delay(n, tasks, setup_times, J_order) -> int:
    max_Y = float('inf')
    current_time = 0
    Y = 0
    
    for i in range(n):
        task_index = J_order[i]
        p, d = tasks[task_index]

        if i > 0:
            prev_task_index = J_order[i - 1]
            current_time += setup_times[prev_task_index][task_index]

        current_time += p
        if current_time > d:
            Y += min(p, max(0, current_time - d))

        if Y > max_Y:
            return max_Y

    return Y


def generate_neighbors(n, solution, size) -> list[list[int]]:
    neighbors = []
    seen_swaps = set()

    for _ in range(size):
        while True:
            i, j = random.sample(range(n), 2)
            swap_pair = (min(i, j), max(i, j))

            if swap_pair not in seen_swaps:
                seen_swaps.add(swap_pair)
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
                break
    
    return neighbors


def calculate_incremental_delay(tasks, setup_times, J_order, i, j) -> int:
    J_order[i], J_order[j] = J_order[j], J_order[i]
    
    current_time = 0
    total_delay = 0
    
    for k in range(len(J_order)):
        task_index = J_order[k]
        p, d = tasks[task_index]

        if k > 0:
            prev_task_index = J_order[k - 1]
            current_time += setup_times[prev_task_index][task_index]

        current_time += p
        delay_contribution = max(0, current_time - d)

        if delay_contribution > 0:
            total_delay += min(p, delay_contribution)

    J_order[i], J_order[j] = J_order[j], J_order[i]

    return total_delay


def generate_swaps(n, size) -> list[tuple[int, int]]:
    return [random.sample(range(n), 2) for _ in range(size)]


def optimized_tabu_search(n, tasks, setup_times, max_tabu_size, start_time, time_limit) -> tuple[list[int], int]:
    best_solution = hodgson_algorithm(n, tasks, setup_times)
    best_delay = calculate_delay(n, tasks, setup_times, best_solution)
    
    tabu_list = set()
    
    while time.time() - start_time < time_limit:
        swaps = generate_swaps(n, 300)
        best_swap = None
        best_neighbor_delay = float('inf')

        for i, j in swaps:
            if (i, j) in tabu_list or (j, i) in tabu_list:
                continue

            neighbor_delay = calculate_incremental_delay(tasks, setup_times, best_solution, i, j)
            
            if neighbor_delay < best_neighbor_delay:
                best_swap = (i, j)
                best_neighbor_delay = neighbor_delay

        if best_swap:
            i, j = best_swap
            best_solution[i], best_solution[j] = best_solution[j], best_solution[i]
            best_delay = best_neighbor_delay

            tabu_list.add((i, j))
            if len(tabu_list) > max_tabu_size:
                tabu_list.pop()

    best_solution = [x + 1 for x in best_solution]
    return best_solution, best_delay


def main():
    if len(sys.argv) != 4:
        print("Użycie: python solver.py plik_wejściowy plik_wyjsciowy max_time")
        sys.exit(1)

    start_time = time.time()

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        max_time = float(sys.argv[3])
    except ValueError:
        print("Błąd: max_time musi być liczbą.")
        sys.exit(1)

    n, tasks, setup_times = read_instance(input_file)
    max_tabu_size = 100 

    best_solution, best_delay = optimized_tabu_search(n, tasks, setup_times, max_tabu_size, start_time, max_time - 0.1)
    write_solution_to_file(output_file, best_delay, best_solution)


if __name__ == "__main__":
    main()
