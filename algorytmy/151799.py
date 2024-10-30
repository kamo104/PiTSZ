import time
import random
import sys



# Ustawienie ziarna dla powtarzalnych rozwiązań
random.seed(151799)



# Funkcja wczytująca instrancję
def read_instance(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        
        tasks = []
        for _ in range(n):
            p, d = map(int, f.readline().strip().split())
            tasks.append((p, d))
        
        setup_times = []
        for _ in range(n):
            row = list(map(int, f.readline().strip().split()))
            setup_times.append(row)

    return n, tasks, setup_times



# Funkcja obliczająca opóźnienie harmonogramu
def calculate_delay(n, tasks, setup_times, J_order, max_Y = float('inf')):
    current_time = 0
    Y = 0
    
    for i in range(n):
        task_index = J_order[i]
        p, d = tasks[task_index]

        if i > 0:
            prev_task_index = J_order[i-1]
            current_time += setup_times[prev_task_index][task_index]

        current_time += p
        if current_time > d:
            Y += min(p, max(0, current_time - d))

        if Y > max_Y:
            return max_Y

    return Y



# Algorytm zachłanny generujący wstępne rozwiązanie
def greedy_solution_min_delay(n, tasks, setup_times):
    remaining_tasks = list(range(n)) 
    current_solution = []
    current_time = 0
    last_task = None

    while remaining_tasks:
        best_task = None
        best_delay = float('inf')

        for task_idx in remaining_tasks:
            p, d = tasks[task_idx]
            if last_task is not None:
                switch_time = setup_times[last_task][task_idx]
            else:
                switch_time = 0 

            completion_time = current_time + switch_time + p
            delay = max(0, completion_time - d)
            
            if delay < best_delay:                    
                best_delay = delay
                best_task = task_idx

                if delay == 0:
                    break

        current_solution.append(best_task)
        remaining_tasks.remove(best_task)

        if last_task is not None:
            current_time += setup_times[last_task][best_task] 
        
        current_time += tasks[best_task][0]
        last_task = best_task

    return current_solution



# Funkcja generująca sąsiedztwo przez zamianę dwóch zadań
def generate_neighbors(n, solution, size):
    neighbors = []
    for _ in range(size):
        neighbor = solution.copy()
        to_swap = random.sample(range(n), 2)
        neighbor[to_swap[0]], neighbor[to_swap[1]] = neighbor[to_swap[1]], neighbor[to_swap[0]]
        neighbors.append(neighbor)
    return neighbors



# Algorytm tabu search
def tabu_search(n, tasks, setup_times, max_tabu_size, time_limit):
    best_solution = greedy_solution_min_delay(n, tasks, setup_times)
    best_delay = calculate_delay(n, tasks, setup_times, best_solution)

    tabu_list = []
    start_time = time.time()
    time_limit = time_limit - 0.3
    
    while time.time() - start_time < time_limit:
        neighbors = generate_neighbors(n, best_solution, 500)
        best_neighbor = None
        best_neighbor_delay = float('inf')
        
        for neighbor in neighbors:
            if neighbor not in tabu_list:
                delay = calculate_delay(n, tasks, setup_times, neighbor, best_delay)
                if delay < best_neighbor_delay:
                    best_neighbor = neighbor
                    best_neighbor_delay = delay

        if best_neighbor_delay < best_delay:
            best_solution = best_neighbor
            best_delay = best_neighbor_delay

        tabu_list.append(best_neighbor)
        if len(tabu_list) > max_tabu_size:
            tabu_list.pop(0)

    best_solution = [x+1 for x in best_solution]
    return best_solution, best_delay



def save(filename, Y, order):
    with open(filename, "w") as f:
        f.write(str(Y)+"\n")
        f.write(" ".join(map(str, order))+"\n")



def main():
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    time_limit = int(sys.argv[3])

    n, tasks, setup_times = read_instance(filename)
    
    # time_limit = n / 10.0

    max_tabu_size = 100 

    best_solution, best_delay = tabu_search(n, tasks, setup_times, max_tabu_size, time_limit)

    save(output_filename, best_delay, best_solution)
    


if __name__ == "__main__":
    main()