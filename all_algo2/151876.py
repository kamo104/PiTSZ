import sys
import time
import random
import copy


random.seed(0xB00B5)

class Data:
    def __init__(self, n: int, p_arr: list[list[int]]):
        # ilość elementów
        self.n = n
        # arrayka z danymi zadań
        self.p_arr = p_arr
    def __str__(self):
        out = str(self.n) + '\n'
        out += ''.join([' '.join(list(map(str, self.p_arr[i]))) + '\n' for i in range(self.n)])
        return out

class Solution:
    def __init__(self, u: int, j_arr: list[list[int]]):
        self.u = u
        self.j_arr = j_arr
    def __str__(self):
        out = str(self.u) + '\n'
        out += ''.join([' '.join(list(map(str, self.j_arr[i]))) + '\n' for i in range(5)])
        return out

def gen_source_data(n):
    tasks = []
    for j in range(1, n + 1):
        p_values = [random.randint(1, 100) for _ in range(5)]
        rj = random.randint(0, 100*n)
        dj = rj + random.randint(10, 100)
        task = [*p_values, rj, dj]
        tasks.append(task)
    return Data(len(tasks), tasks)

def parse_data_to_struct(source: list) -> Data:
    n = int(source.pop(0))
    p_arr = list(map(lambda row: list(map(int, row.split(maxsplit=6))), source))

    return Data(n, p_arr)

def parse_res_to_struct(result: list) -> Solution:
    u = int(result.pop(0))
    h_arr = list(map(lambda row: list(map(int, row.split())), result))
    return Solution(u, h_arr)


def load_from_file(filename):
    with open(filename) as fd:
        out = fd.readlines()
    return out

def save_to_file(data: str, filename):
    with open(filename, mode='w') as fd:
        fd.write(data)


def validate_solution(instance: Data, solution: Solution):
    all_tasks = set(range(1, instance.n + 1))
    scheduled_tasks = set()
    print()
    for seq in solution.j_arr:
        scheduled_tasks.update(seq)

    if all_tasks != scheduled_tasks:
        print(all_tasks, scheduled_tasks, sep='\n')
        return -1

    total_cost = 0
    for worker_index, seq in enumerate(solution.j_arr):
        current_time = 0
        for task_index in seq:
            task = instance.p_arr[task_index - 1]
            p = task[worker_index]
            r = task[-2]
            d = task[-1]

            if current_time < r:
                current_time = r

            current_time += p

            if current_time > d:
                total_cost += 1
    if solution.u != total_cost:
        return total_cost

    return total_cost


def schedule_tasks(data: Data):
    tasks = data.p_arr
    workers = [[] for _ in range(5)]
    worker_time = [0] * 5
    total_late_count = 0

    tasks_sorted = sorted(enumerate(tasks, start=1), key=lambda x: x[1][-1])

    for task_id, task in tasks_sorted:
        p_times = task[:5]
        r = task[-2]
        d = task[-1]

        best_worker = None
        earliest_completion = float('inf')

        for worker_idx, p_time in enumerate(p_times):
            start_time = max(worker_time[worker_idx], r)
            completion_time = start_time + p_time

            if completion_time < earliest_completion:
                earliest_completion = completion_time
                best_worker = worker_idx

        workers[best_worker].append(task_id)
        worker_time[best_worker] = earliest_completion

        if earliest_completion > d:
            total_late_count += 1

    return Solution(total_late_count, workers)


def schedule_tasks_with_local_search(data: Data, time_limit=5):
    tasks = data.p_arr
    def evaluate_solution(workers):
        total_late_count = 0

        for worker_idx, seq in enumerate(workers):
            current_time = 0
            for task_id in seq:
                task = tasks[task_id - 1]
                p_time = task[worker_idx]
                r = task[-2]
                d = task[-1]
                current_time = max(current_time, r) + p_time
                if current_time > d:
                    total_late_count += 1

        return total_late_count

    def generate_initial_solution():
        workers = [[] for _ in range(5)]
        worker_time = [0] * 5
        tasks_sorted = sorted(enumerate(tasks, start=1), key=lambda x: x[1][-1])

        for task_id, task in tasks_sorted:
            p_times = task[:5]
            r = task[-2]

            best_worker = None
            earliest_completion = float('inf')

            for worker_idx, p_time in enumerate(p_times):
                start_time = max(worker_time[worker_idx], r)
                completion_time = start_time + p_time
                if completion_time < earliest_completion:
                    earliest_completion = completion_time
                    best_worker = worker_idx

            workers[best_worker].append(task_id)
            worker_time[best_worker] = earliest_completion

        return workers

    def make_small_change(workers):
        # new_workers = [list(w) for w in workers]
        new_workers = copy.deepcopy(workers)
        worker1, worker2 = random.sample(range(5), 2)
        if not new_workers[worker1] or not new_workers[worker2]:
            return new_workers

        idx1 = random.randint(0, len(new_workers[worker1]) - 1)
        idx2 = random.randint(0, len(new_workers[worker2]) - 1)
        new_workers[worker2][idx2], new_workers[worker1][idx1] = \
            new_workers[worker1][idx1], new_workers[worker2][idx2]

        return new_workers


    best_solution = generate_initial_solution()
    best_cost = evaluate_solution(best_solution)
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < (time_limit-.3) and best_cost > 0:
        new_solution = make_small_change(best_solution)
        new_cost = evaluate_solution(new_solution)

        if new_cost < best_cost:
            best_solution = new_solution
            best_cost = new_cost

    return Solution(best_cost, best_solution)


if __name__ == '__main__':
    start = time.perf_counter()
    args = sys.argv[1:]
    in_file, out_file = args[0], args[1]
    t_limit = float(args[2]) if len(args)==3 else -1

    # print(in_file, out_file, t_limit)
    # print('Starting...')
    data = parse_data_to_struct(load_from_file(in_file))
    sol = schedule_tasks_with_local_search(data, t_limit)
    save_to_file(str(sol), out_file)
    print(sol.u)
    # print(time.perf_counter() - start)
