import random
import time
import sys

def generate_random_rows(n):
    if n < 5:
        raise ValueError("n musi być większe lub równe 5, aby można było stworzyć 5 wierszy.")
    
    numbers = list(range(1, n + 1))
    random.shuffle(numbers)

    rows = []
    remaining_numbers = n
    for i in range(5):
        if i == 4:
            rows.append(numbers[:remaining_numbers])
            break
        max_row_length = remaining_numbers - (4 - i)
        row_length = random.randint(1, max_row_length)
        rows.append(numbers[:row_length])
        numbers = numbers[row_length:]
        remaining_numbers -= row_length

    return rows

def read_in(filename):
    f = open(filename)
    dane = f.read()
    f.close()

    dane = dane.split('\n')
    n = int(dane[0])
    p = []
    r = []
    d = []
    for i in range(1, 1 + n):
        line = dane[i].split(' ')
        if(line[0] == ''):
            line = line[1:]
        if(line[-1] == ''):
            line = line[0:-1]
        p.append([int(x) for x in line[0:5]])
        r.append(int(line[-2]))
        d.append(int(line[-1]))
    return n, p, r, d


def calculate_result(tab, p, r, d):
    result = 0
    
    for machine_nr, machine_tasks in enumerate(tab):
        current_time_machine = 0
        for i in range(len(machine_tasks)):
            task_nr = machine_tasks[i] - 1
            task_time = p[task_nr][machine_nr]
            task_time_delay = r[task_nr]
            task_due_date = d[task_nr]
            if(current_time_machine < task_time_delay):
                current_time_machine = task_time_delay
            current_time_machine += task_time
            if(current_time_machine > task_due_date):
                result += 1
    return result

def execute_until(time_limit, start_time, n, p, r, d):
    best_tab = generate_random_rows(n)
    best_result = calculate_result(best_tab, p, r, d)

    while True:
        tab = generate_random_rows(n)
        result = calculate_result(tab, p, r, d)

        if result < best_result:
            best_tab = tab
            best_result = result

        if time.time() - start_time > time_limit:
            break
    return [best_result, best_tab]

def write_to_file(filename, result, tab):
    f = open(filename, 'w')
    f.write(str(result) + '\n')
    for row in tab:
        for el in row:
            f.write(str(el) + ' ')
        f.write('\n')

start_time = time.time()
filename_in = sys.argv[1]
filename_out = sys.argv[2]
n, p, r, d = read_in(filename_in)
best_results = execute_until(int(sys.argv[3]) - 0.1, start_time, n, p, r, d)
result = best_results[0]
tab = best_results[1]
write_to_file(filename_out, result, tab)