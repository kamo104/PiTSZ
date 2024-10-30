import sys
import threading
import time

class TimeoutException(Exception):
    pass

def timeout_handler():
    raise TimeoutException("Time limit exceeded!")

def hodgson_algorithm(n, p, d, S):
    tasks = list(range(n))
    schedule = []
    unscheduled = set(tasks)
    current_time = 0

    tasks_sorted = sorted(tasks, key=lambda x: d[x])

    # Przetwarzanie zadań
    for i in tasks_sorted:
        if schedule:
            last_task = schedule[-1]
            current_time += S[last_task][i]  #Czas przezbrojenia
        
        current_time += p[i]  #Czas lakierowania
        schedule.append(i)
        unscheduled.remove(i)

        if current_time > d[i]:
            max_task = max(schedule, key=lambda x: p[x])
            schedule.remove(max_task)
            unscheduled.add(max_task)
            current_time -= p[max_task]
            if schedule:
                current_time -= S[schedule[-1]][max_task]

    for task in unscheduled:
        if schedule:
            last_task = schedule[-1]
            current_time += S[last_task][task]
        current_time += p[task]
        schedule.append(task)

    Y = 0
    finish_time = 0
    for i in schedule:
        if finish_time > 0:
            finish_time += S[schedule[schedule.index(i) - 1]][i]
        finish_time += p[i]
        Y += min(p[i], max(0, finish_time - d[i]))

    return Y, schedule

def read_input(input_file):
    with open(input_file, "r") as f:
        n = int(f.readline().strip())  # Liczba zadań
        p, d = [], []
        for _ in range(n):
            pj, dj = map(int, f.readline().strip().split())
            p.append(pj)
            d.append(dj)
        S = [list(map(int, f.readline().strip().split())) for _ in range(n)]
    return n, p, d, S

def write_output(output_file, Y, schedule):
    with open(output_file, "w") as f:
        f.write(f"{Y}\n")
        f.write(" ".join(str(x + 1) for x in schedule) + "\n")

def run_algorithm_with_timeout(timeout_sec, algorithm, *args):
    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = algorithm(*args)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.start()

    thread.join(timeout_sec)

    if thread.is_alive():
        raise TimeoutException("Przekroczono limit czasu!")
    
    if exception[0]:
        raise exception[0]

    return result[0]

# Główna funkcja programu
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Użycie: python program.py <plik_wejściowy> <plik_wyjściowy> <limit_czasu_w_sekundach>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_limit = int(sys.argv[3])

    try:
        n, p, d, S = read_input(input_file)

        Y, schedule = run_algorithm_with_timeout(time_limit, hodgson_algorithm, n, p, d, S)

        write_output(output_file, Y, schedule)

        print("Success!")
    except TimeoutException as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
