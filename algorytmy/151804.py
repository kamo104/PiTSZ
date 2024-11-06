import sys

class Task:
    def __init__(self, id, duration, deadline):
        self.id = id
        self.duration = int(duration)
        self.deadline = int(deadline)

def main():
    if len(sys.argv) < 3:
        print("Error, expected input filename and output filename")
        return
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    in_file = open(input_filename, "r")
    task_count = int(in_file.readline().strip())
    tasks = []
    swap_times = []
    for i in range(task_count):
        line = in_file.readline().strip()
        duration, deadline = line.split()
        tasks.append(Task(i, duration, deadline))
    for i in range(task_count):
        swap_times_for_task = [int(x) for x in in_file.readline().strip().split()]
        swap_times.append(swap_times_for_task)
    in_file.close()
    tasks.sort(key=(lambda a: a.deadline))

    current_result = 0
    previous_task = None
    current_time = 0
    for task in tasks:
        current_time += task.duration
        if previous_task is not None:
            current_time += swap_times[previous_task.id][task.id]
        previous_task = task
        delay = min(task.duration, max(0, current_time - task.deadline))
        current_result += delay

    out_file = open(output_filename, "w")
    out_file.write(str(current_result))
    out_file.write("\n")
    solution = ' '.join([str(task.id+1) for task in tasks])
    out_file.write(solution)
    out_file.close()

if __name__ == '__main__':
    main()

