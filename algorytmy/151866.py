import sys

def read_data(input_file):
    with open(input_file, 'r') as f:
        n = int(f.readline().strip())
        tasks = []
        for _ in range(n):
            pj, dj = map(int, f.readline().strip().split())
            tasks.append((pj, dj))

        switch_times = []
        for _ in range(n):
            switch_times.append(list(map(int, f.readline().strip().split())))

    return n, tasks, switch_times

def write_results(output_file, delays, schedule):
    with open(output_file, 'w') as f:
        f.write(f"{delays}\n")
        f.write(" ".join(map(str, schedule)) + "\n")

def calculate_schedule(input_file, output_file, time_limit):
    n, tasks, switch_times = read_data(input_file)
    current_time = 0
    total_delay = 0
    completed_tasks = set()
    schedule = []

    while len(completed_tasks) < n:
        best_task = None
        minimum_delay = float('inf')

        for j in range(n):
            if j not in completed_tasks:
                pj, dj = tasks[j]

                if schedule:
                    last_task = schedule[-1] - 1
                    switch_time = switch_times[last_task][j]
                else:
                    switch_time = 0

                predicted_completion_time = current_time + switch_time + pj
                delay = min(pj, max(0, predicted_completion_time - dj))

                if delay < minimum_delay:
                    minimum_delay = delay
                    best_task = j

        completed_tasks.add(best_task)
        schedule.append(best_task + 1)

        pj, dj = tasks[best_task]

        if len(schedule) > 1:
            last_task = schedule[-2] - 1
            switch_time = switch_times[last_task][best_task]
        else:
            switch_time = 0

        current_time += switch_time + pj
        total_delay += min(pj, max(0, current_time - dj))

    write_results(output_file, total_delay, schedule)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])
    calculate_schedule(input_file, output_file, time_limit)
