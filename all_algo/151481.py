import time
import pandas as pd


def calc_late(tasks, assign):
    end_time = {
        k: 0 for k in range(1, 6)
    }
    late = 0
    results = []

    # dla każdego pracownika
    for worker, task_list in assign.items():
        # dla kazdego zadania pracownika
        for t_id in task_list:
            for t in tasks:
                if t[0] == t_id:
                    t_data = t[1]
                    break

            p_time = t_data[worker - 1]
            r = t_data[5]
            d = t_data[6]

            start = max(r, end_time[worker])
            finish = start + p_time
            if finish > d:
                late += 1

            end_time[worker] = finish

            results.append({
                "worker": worker,
                "task": t_id,
                "start": start,
                "end": finish,
                "r": r,
                "d": d,
                "late": 1 if finish > d else 0,
            })

    return late, pd.DataFrame(results)


def ptas(n, tasks, eps, time_limit):
    start = time.time()
    # maksymalne d
    d_max = max([t[1][6] for t in tasks]) 
    big = []
    small = []

    for t in tasks:
        t_id, t_data = t
        if max(t_data[:5]) > eps * d_max:  # jeśli czas wykonania jest duży
            big.append(t)
        else:
            small_data = [eps * d_max] * 5 + t_data[5:] # else
            small.append((t_id, small_data))

    all_tasks = big + small
    # sort po czasie r
    all_tasks.sort(key=lambda x: x[1][5])

    assign = {
        k: [] for k in range(1, 6)
    }
    end_time = {
        k: 0 for k in range(1, 6)
    }

    for t in all_tasks:
        t_id, t_data = t
        # limit czasu
        if time.time() - start > time_limit:
            break

        best_worker = None
        best_time = float('inf')

        #szukamy najlepszego pracownika
        for worker in range(1, 6):
            start_time = max(end_time[worker], t_data[5])  # start tasku
            finish_time = start_time + t_data[worker - 1]  # koniec tasku
            if finish_time < best_time:
                best_time = finish_time
                best_worker = worker
        
        # przypisanie
        assign[best_worker].append(t_id) 
        end_time[best_worker] = best_time

    late, details = calc_late(tasks, assign)  # Uj
    return late, assign, details


def read_input(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    tasks = []
    for i, line in enumerate(lines[1:]):
        values = list(map(int, line.strip().split()))
        # dodajemy (id, [p,p,p,p,p,r,d]), bo id !
        tasks.append((i + 1, values))
    return n, tasks


def write_output(file, late, assign):
    with open(file, 'w') as f:
        f.write(f"{late}\n")
        for worker in range(1, 6):
            f.write(" ".join(map(str, assign[worker])) + "\n")


def main(input_file, output_file, time_limit):
    n, tasks = read_input(input_file)
    eps = 0.08  # parametr epsilon

    late, assign, details = ptas(n, tasks, eps, time_limit)
    # print(details)
    write_output(output_file, late, assign)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    limit = float(sys.argv[3])

    main(in_file, out_file, limit)
