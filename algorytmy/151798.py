import numpy as np
import argparse


def calculate(sequence, p, d, matrix):
    n = len(sequence)
    time = 0
    y = 0

    for i in range(n):
        task = sequence[i] - 1
        time += p[task]
        y += min(p[task], max(0, time - d[task]))

        if i < n - 1:
            next_task = sequence[i + 1] - 1
            time += matrix[task][next_task]

    return y


def greedy(n, p, d, S):
    tasks = sorted(range(n), key=lambda x: (d[x], p[x]))
    sequence = [tasks[0] + 1]
    tasks.remove(tasks[0])
    while tasks:
        last_task = sequence[-1] - 1
        next_task = min(tasks, key=lambda x: S[last_task][x])
        sequence.append(next_task + 1)
        tasks.remove(next_task)

    y = calculate(sequence, p, d, S)
    return y, sequence

def read_input(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        p = []
        d = []
        for i in range(n):
            pi, di = map(int, file.readline().strip().split())
            p.append(pi)
            d.append(di)
        matrix = np.zeros((n, n), dtype=int)
        for i in range(n):
            matrix[i] = list(map(int, file.readline().strip().split()))
    return n, p, d, matrix

def write_output(filename, y, sequence):
    with open(filename, 'w') as file:
        file.write(str(y) + '\n')
        file.write(' '.join(map(str, [s for s in sequence])) + '\n')

parser = argparse.ArgumentParser(description="Porównanie wyników obliczeń.")
parser.add_argument("input_file", help="Ścieżka do pliku wejściowego.")
parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego.")
parser.add_argument("time", help="Czas wykonania.")

args = parser.parse_args()

n, p, d, S = read_input(args.input_file)
y, sequence = greedy(n, p, d, S)
write_output(args.output_file, y, sequence)
