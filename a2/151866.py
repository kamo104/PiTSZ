import sys

def read_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    tasks = []

    for line in lines[1:]:
        data = list(map(int, line.strip().split()))
        p = data[:5]
        r = data[5]
        d = data[6]
        tasks.append((p, r, d))

    return n, tasks

def dynamic_priority_scheduling_with_deadline(tasks):
    num_workers = 5
    workers = [0] * num_workers
    schedule = [[] for _ in range(num_workers)]
    delayed_tasks = 0
    tasks = list(enumerate(tasks))

    while tasks:
        best_task = None
        best_worker = -1
        best_priority = float('inf')
        earliest_finish = float('inf')

        for task_idx, (p, r, d) in tasks:
            for worker_id in range(num_workers):
                start_time = max(workers[worker_id], r)
                finish_time = start_time + p[worker_id]
                lateness = max(0, finish_time - d)
                priority = lateness
                if priority < best_priority or (priority == best_priority and finish_time < earliest_finish):
                    best_priority = priority
                    best_task = (task_idx, (p, r, d))
                    best_worker = worker_id
                    earliest_finish = finish_time

        if best_task:
            task_idx, (p, r, d) = best_task
            start_time = max(workers[best_worker], r)
            finish_time = start_time + p[best_worker]
            workers[best_worker] = finish_time
            schedule[best_worker].append(task_idx + 1)
            if finish_time > d:
                delayed_tasks += 1

            tasks = [task for task in tasks if task[0] != task_idx]

    return delayed_tasks, schedule

def write_output(output_file, delayed_tasks, schedule):
    with open(output_file, 'w') as file:
        file.write(f"{delayed_tasks}\n")
        for worker_schedule in schedule:
            line = " ".join(map(str, worker_schedule))
            file.write(f"{line}\n")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    n, tasks = read_input(input_file)
    delayed_tasks, schedule = dynamic_priority_scheduling_with_deadline(tasks)
    write_output(output_file, delayed_tasks, schedule)