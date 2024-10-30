import random
import time
import sys

def read_input_data(fileName: str):
    f = open(fileName)
    dane = f.read()
    f.close()

    dane = dane.split('\n')
    n = int(dane[0])
    p = []
    d = []
    for i in range(1, 1 + n):
        p.append(int(dane[i].split(' ')[0]))
        d.append(int(dane[i].split(' ')[1]))

    s = []
    for i in range( 1 + n, 1 + 2*n):
        s.append(dane[i])

    for i in range(n):
        s[i] = s[i].split(' ')
        if s[i][0] == '':
            s[i] = s[i][1:]
        if s[i][-1] == '':
            s[i] = s[i][:-1]
        for j in range(n):
            s[i][j] = int(s[i][j])
    return [n, p, d, s]

def calculate_result(tab, p, d, s):
    correct_result = 0
    sum = 0
    val = tab[0]
    sum += p[val-1]

    correct_result += min(p[0], max(0, sum - d[0]))
    for i in range(1, len(tab)):
        prev_val = tab[i - 1]
        curr_val = tab[i]
        due_termin = d[curr_val-1]
        time_p = p[curr_val-1]
        time_s = s[prev_val - 1][curr_val - 1]
        sum += time_p + time_s
        correct_result += min(time_p, max(0, sum - due_termin))

    return correct_result

def generate_random_tab(n):
    tab = list(range(1, n + 1))
    random.shuffle(tab)
    return tab

def execute_until(time_limit, start_time):
    best_tab = generate_random_tab(n)
    best_result = calculate_result(best_tab, p, d, s)

    while True:
        tab = generate_random_tab(n)
        result = calculate_result(tab, p, d, s)

        if result < best_result:
            best_tab = tab
            best_result = result

        if time.time() - start_time > time_limit:
            break
    return [best_result, best_tab]
        
def write_to_file(filename, result, tab):
    f = open(filename, 'w')
    f.write(str(result) + '\n')
    for el in tab:
        f.write(str(el) + ' ')

start_time = time.time()
filename_in = sys.argv[1]
data = read_input_data(filename_in)

n = data[0]
p = data[1]
d = data[2]
s = data[3]

best_results = execute_until(int(sys.argv[3]), start_time)
result = best_results[0]
tab = best_results[1]
filename_out = sys.argv[2]
write_to_file(filename_out, result, tab)
print(time.time() - start_time)