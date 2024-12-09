import sys


def calculate_delay(jobs, schedules):
    U = 0

    for worker, schedule in enumerate(schedules):
        time = 0
        for task_id in schedule:
            task = jobs[task_id-1]
            p = task[worker]
            r = task[5]
            d = task[6]

            time = max(time, r) + p
            
            if time > d:
                U += 1

    return U


def list_scheduling(jobs, rule):
    tasks = sorted(enumerate(jobs), key=rule)
    schedules = [[] for _ in range(5)]
    finish_times = [0]*5

    MAX_ATTEMPTS = 3
    attempts = {task_id: 0 for task_id, _ in tasks}
    while tasks:
        task_id, task = tasks.pop(0)
        best_machine = min(range(5), key=lambda m: max(finish_times[m], task[5]) + task[m])
        start_time = max(finish_times[best_machine], task[5])
        finish_time = start_time + task[best_machine]

        if finish_time > task[6]:
            if attempts[task_id] < MAX_ATTEMPTS:
                tasks.append((task_id, task))
                attempts[task_id] += 1
                continue

        schedules[best_machine].append(task_id + 1)
        finish_times[best_machine] = finish_time

    return schedules


def find_best_rule(jobs):
    
    rules = {
        "EDD": lambda task: task[1][-1],  # Najwcześniejszy deadline
        "SPT": lambda task: min(task[1][:-2]),  # Najkrótszy czas realizacji
        "LPT": lambda task: -max(task[1][:-2]),  # Najdłuższy czas realizacji
        "EST": lambda task: task[1][-2],  # Najwcześniejszy czas gotowości
        "LST": lambda task: task[1][-1] - task[1][-2], # Najkrótszy czas między początkiem a końcem
    }

    min_delay = float("inf")
    best_schedule = None
    best_rule = None

    for rule_name, rule in rules.items():
        schedules = list_scheduling(jobs, rule)
        delay = calculate_delay(jobs, schedules)

        if delay < min_delay:
            min_delay = delay
            best_schedule = schedules
            best_rule = rule_name

    return min_delay, best_schedule, best_rule


def read_instance(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        
        jobs = []
        for _ in range(n):
            job = list(map(int, f.readline().strip().split()))
            jobs.append(job)

    return n, jobs


def save(filename, U, schedules):
    with open(filename, "w") as f:
        f.write(str(U)+"\n")
        for schedule in schedules:
            f.write(" ".join(map(str, schedule))+"\n")


def main():
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    time_limit = int(sys.argv[3])

    _, jobs = read_instance(filename) 

    delay, schedules, rule = find_best_rule(jobs)
    
    save(output_filename, delay, schedules)
    
    # print(rule, delay)


if __name__ == "__main__":
    main()