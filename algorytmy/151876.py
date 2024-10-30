#!/usr/bin/env python3
import sys
import time
import random

random.seed(151876)

P_TIME_RANGE = {
    'mini': 15,
    'maxi': 30
}
SETUP_TIME_RANGE = {
    'mini': 1,
    'maxi': 5
}


class Data:
    def __init__(self, n: int, p: list[int], d: list[int], s: list[list[int]]):
        # ilość elementów
        self.n = n
        # arrayka z wartościami p
        self.p = p
        # arrayka z wartościami d
        self.d = d
        # 2d arrayka z wartościami S
        self.s = s
    def __str__(self):
        out = str(self.n) + '\n'
        out += ''.join([str(self.p[i]) + ' ' + str(self.d[i]) + '\n' for i in range(self.n)])
        out += ''.join([' '.join(list(map(str, self.s[i]))) + '\n' for i in range(self.n)])
        return out


class Solution:
    def __init__(self, y: int, j_order: list[int]):
        # suma przestrzałów
        self.y = y
        # arrayka z indeksami J w koejniści
        self.j_order = j_order
    def __str__(self):
        out = str(self.y) + '\n'
        out += ' '.join(list(map(lambda x: str(x+1), self.j_order)))
        return out


def _sort_by_deadlines(data: Data) -> Solution:
    deadlines = list(enumerate(data.d))
    order = sorted(deadlines, key=lambda x: x[1])
    order = list(map(lambda x: x[0], order))
    return Solution(calc_overshoots(order, data), order)


def calc_overshoots(j_order: list, data: Data, dead_y = 1e20):
    y_sum = 0
    c = 0
    for i in range(len(j_order)):
        curr = j_order[i]
        if i > 0:
            prev = j_order[i-1]
            c += data.s[prev][curr]
        c += data.p[curr]
        y_sum += _eval_overshoot(c, data.p[curr], data.d[curr])
        if y_sum > dead_y:
            # przypadek kiedy sum_y przekracza jakąś ustaloną wartość,
            # dalsze liczenie jest przerywane (wiadomo, że już jest gorsze)
            return -1
    return y_sum


def _eval_overshoot(c, p, d):
    return min(p, max(0, c - d))


def _tabu_search(data: Data, t_limit=-1)->Solution:
    # działanie z uwzględnieniem czasu na obliczenia wg. zasady t[s] = n/10
    startt = time.perf_counter()
    deadline = data.n / 10 if t_limit==-1 else t_limit
    def _we_have_time(): return time.perf_counter() - startt < (deadline - 0.1)  # dodajemy limit 0.1 sekundy na każde

    sol0 = _sort_by_deadlines(data)
    y_best , order_best = sol0.y, sol0.j_order
    checked = [order_best]

    indeces = list(range(data.n))
    while _we_have_time():
        new_order = order_best.copy()
        pair = random.sample(indeces, 2)
        new_order[pair[0]], new_order[pair[1]] = new_order[pair[1]], new_order[pair[0]]
        if new_order in checked: continue
        new_y = calc_overshoots(new_order, data, y_best)
        if new_y!=-1 and new_y < y_best:
            y_best, order_best = new_y, new_order
        checked.append(new_order)

    return Solution(y_best, order_best)


def load_from_file(filename):
    with open(filename) as fd:
        out = fd.readlines()
    fd.close()
    return out


def save_to_file(data: str, filename):
    with open(filename, mode='w') as fd:
        fd.write(data)
    fd.close()


def validate_solution(solution: Solution, data: Data)->int:
    if len(solution.j_order) < data.n:  # czy użyte wszystkie
        return -1
    if len(set(solution.j_order)) < data.n:  # czy brak duplikatów
        return 2
    res = calc_overshoots(solution.j_order, data)
    if solution.y != res:
        return 1
    return solution.y


def _parse_data_to_struct(source: list) -> Data:
    n = int(source.pop(0))
    p, d = [], []
    for i in range(n):
        p_, d_ = source.pop(0).split(' ', maxsplit=1)
        p.append(int(p_))
        d.append(int(d_))
    s = []
    for i in range(n):
        s_row = source.pop(0).split()
        s.append(list(map(int, s_row)))
    return Data(n, p, d, s)


if __name__ == '__main__':
    start = time.perf_counter()
    args = sys.argv[1:]
    in_file, out_file = args[0], args[1]
    t_limit = float(args[2]) if len(args)==3 else -1

    print(in_file, out_file, t_limit)
    print('Starting...')
    data = _parse_data_to_struct(load_from_file(in_file))
    sol = _tabu_search(data, t_limit)
    save_to_file(str(sol), out_file)
    print(sol.y)
    print(time.perf_counter() - start)
    print('valid' if validate_solution(sol, data) == sol.y else 'no nie do kocna valid')