import sys

input_prefix = './instances/'
output_prefix = './results/'


def read_input(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        tasks = []
        for _ in range(n):
            data = list(map(int, file.readline().strip().split()))
            times = data[:5]
            ready_time = data[5]
            deadline = data[6]
            tasks.append((times, ready_time, deadline))
        return n, tasks


def assign_tasks(tasks):
    assignments = [[] for _ in range(5)]
    completion_times = [0] * 5
    total_late_tasks = 0

    tasks = sorted(enumerate(tasks), key=lambda x: x[1][2])  # Sort by deadline

    for task_id, (times, ready_time, deadline) in tasks:
        best_worker = None
        best_finish_time = float('inf')

        for worker_id in range(5):
            start_time = max(completion_times[worker_id], ready_time)
            finish_time = start_time + times[worker_id]
            if finish_time < best_finish_time:
                best_worker = worker_id
                best_finish_time = finish_time

        assignments[best_worker].append(task_id + 1)
        completion_times[best_worker] = best_finish_time

        if best_finish_time > deadline:
            total_late_tasks += 1

    return total_late_tasks, assignments


def write_output(filename, total_late_tasks, assignments):
    with open(filename, 'w') as file:
        file.write(f"{total_late_tasks}\n")
        for worker_tasks in assignments:
            file.write(" ".join(map(str, worker_tasks)) + "\n")


def run_multiple(index):
    for n in range(50, 501, 50):
        instance_filename = f'{input_prefix}in_{index}_{n}.txt'
        output_filename = f'{output_prefix}out_{index}_{n}.txt'

        print(f'Processing: {instance_filename}...')

        n, tasks = read_input(instance_filename)
        total_late_tasks, assignments = assign_tasks(tasks)
        write_output(output_filename, total_late_tasks, assignments)


def main():
    if len(sys.argv) == 2:
        index = sys.argv[1]
        run_multiple(index)
    elif len(sys.argv) == 3 or len(sys.argv) == 4:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        n, tasks = read_input(input_file)
        total_late_tasks, assignments = assign_tasks(tasks)
        write_output(output_file, total_late_tasks, assignments)
    else:
        print('Wrong number of parameters')


if __name__ == "__main__":
    main()
