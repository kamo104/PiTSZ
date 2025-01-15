import argparse
import random
import time
from typing import List, Tuple
from itertools import chain
import sys
import copy

class File:
    def __init__(self, filename: str = ""):
        self.filename = filename
        self.file_stream = None
        if filename:
            self.open(filename)

    def open(self, filename: str = None):
        if filename:
            self.filename = filename
        try:
            self.file_stream = open(self.filename, 'r+')
        except FileNotFoundError:
            self.file_stream = open(self.filename, 'w+')

    def clear(self):
        self.file_stream.close()
        self.file_stream = open(self.filename, 'w+')
        if not self.file_stream:
            raise RuntimeError(f"Failed to clear the file: {self.filename}")

    def read(self, input_stream=None):
        if input_stream is None:
            input_stream = self.file_stream

        raise NotImplementedError("Subclasses must implement read")

    def write(self, output_stream=None):
        if output_stream is None:
            output_stream = self.file_stream

        raise NotImplementedError("Subclasses must implement write")


class Solution(File):
    def __init__(self, filename: str = "", load: bool = False):
        super().__init__(filename)
        self.score = 0.0  # Wartość kryterium (zmiennoprzecinkowa)
        self.patient_schedules = []  # Sekwencje pacjentów (5 linii)
        self.task_sequences = []  # Sekwencje odwiedzania gabinetów (n linii)
        if load:
            self.read()

    def read(self, input_stream=None):
        if input_stream is None:
            input_stream = self.file_stream

        try:
            lines = input_stream.readlines()
            if not lines:
                raise ValueError("Plik wejściowy jest pusty.")

            # Wczytanie wartości kryterium
            self.score = float(lines[0].strip())

            # Wczytanie 5 linii sekwencji pacjentów
            self.patient_schedules = [
                list(map(int, lines[i + 1].split())) for i in range(5)
            ]

            # Wczytanie pozostałych linii jako sekwencje zadań
            self.task_sequences = [
                list(map(int, line.split())) for line in lines[6:]
            ]
        except (ValueError, IndexError) as e:
            raise ValueError(f"Błąd wczytywania pliku: {e}")

    def write(self, output_stream=None):
        if output_stream is None:
            output_stream = self.file_stream

        try:
            # Zapis wartości kryterium
            output_stream.write(f"{self.score}\n")

            # Zapis 5 linii sekwencji pacjentów
            for row in self.patient_schedules:
                output_stream.write(" ".join(map(str, row)) + "\n")

            # Zapis sekwencji zadań
            for row in self.task_sequences:
                output_stream.write(" ".join(map(str, row)) + "\n")
        except Exception as e:
            raise IOError(f"Błąd zapisu do pliku: {e}")


class Instance(File):
    def __init__(self, filename: str = "", size: int = 0, load: bool = False):
        super().__init__(filename)
        self.size = size
        self.tasks = []  # List of task dictionaries
        if load:
            self.read()
        elif size > 0:
            self.generate(size)


    def read(self, input_stream=None):
        if input_stream is None:
            input_stream = self.file_stream
        
        lines = input_stream.readlines()
        self.size = int(lines[0].strip())  # Pierwsza linia: liczba pracowników
        self.tasks = []  # Reset listy zadań
    
        for line in lines[1:]:
            values = list(map(int, line.split()))
            task = {
                'p1': values[0],
                'p2': values[1],
                'p3': values[2],
                'p4': values[3],
                'p5': values[4],
                'r': values[5],
                'w': values[6]
            }
            self.tasks.append(task)

        
    def write(self, output_stream=None):
        if output_stream is None:
            output_stream = self.file_stream

        output_stream.write(f"{self.size}\n")
        for task in self.tasks:
            output_stream.write(" ".join(map(str, task['times'] + [task['r'], task['w']])) + "\n")

    def generate(self, n: int):
        random.seed(1)
        self.size = n
        self.tasks = []
        for _ in range(n):
            times = [random.randint(1, 10) for _ in range(5)]
            r = random.randint(0, 50)
            w = random.randint(1, 10)
            self.tasks.append({'times': times, 'r': r, 'w': w})


def get_score(instance: Instance, solution: Solution) -> int:
    n = instance.size
    tasks = instance.tasks

    rooms = copy.deepcopy(solution.patient_schedules)  # 5 linii sekwencji pacjentów (gabinetów)
    doctors_next_machines = copy.deepcopy(solution.task_sequences)      # n linii sekwencji odwiedzin pracowników

    machine_count = 5
    current_doctor_in_room = [[-1, 0] for _ in range(machine_count)]  # (lekarz, czas trwania)
    doctors_time_in_clinic = [-1] * n  # Czas spędzony w klinice przez lekarzy
    current_time = 0

    def all_done():
        # Sprawdzanie, czy wszystkie kolejki są puste i wszystkie gabinety wolne
        if any(rooms) or any(p_id != -1 for p_id, _ in current_doctor_in_room):
            return False
        return True

    while not all_done():
        # Aktualizacja czasu przebywania lekarzy w klinice
        for doctor_idx in range(n):
            rj = tasks[doctor_idx]['r']
            if rj <= current_time:
                still_has_tasks = len(doctors_next_machines[doctor_idx]) > 0
                is_in_room = any(p_id == doctor_idx for p_id, _ in current_doctor_in_room)
                if still_has_tasks or is_in_room:
                    doctors_time_in_clinic[doctor_idx] += 1 # inkrementacja czasu w gabinecie

        # Aktualizacja stanu gabinetów
        for room_nr in range(machine_count):
            if current_doctor_in_room[room_nr][0] != -1:
                current_doctor_in_room[room_nr][1] -= 1 # dekrementacja czasu w gabinecie
                if current_doctor_in_room[room_nr][1] == 0:
                    current_doctor_in_room[room_nr][0] = -1  # Gabinet staje się wolny

        # Próba wpuszczenia pacjentów do wolnych gabinetów
        for room_nr in range(machine_count):
            if current_doctor_in_room[room_nr][0] == -1 and rooms[room_nr]:
                next_doctor_id = rooms[room_nr][0] - 1
                if tasks[next_doctor_id]['r'] <= current_time:
                    if not any(p_id == next_doctor_id for p_id, _ in current_doctor_in_room):
                        if doctors_next_machines[next_doctor_id] and doctors_next_machines[next_doctor_id][0] == room_nr + 1:
                            duration = tasks[next_doctor_id][f'p{room_nr + 1}']
                            current_doctor_in_room[room_nr] = [next_doctor_id, duration]
                            rooms[room_nr].pop(0)
                            doctors_next_machines[next_doctor_id].pop(0)

        current_time += 1

    # Obliczenie kosztu
    total_cost = 0
    for doctor_idx in range(n):
        wj = tasks[doctor_idx]['w']
        Fj = doctors_time_in_clinic[doctor_idx]
        total_cost += wj * Fj

    return total_cost

def solution(args):
    # Load the instance and prepare the solution
    instance = Instance(args.instance_filename, load=True)
    output_filename = args.solution_filename
    solution = Solution(output_filename)

    num_workers = 5

    solution.patient_schedules = [[j+1 for j in range(instance.size)] for i in range(num_workers)]
    solution.task_sequences = [[j+1 for j in range(num_workers)] for i in range(instance.size)]
    solution.score = get_score(instance, solution)
    solution.clear()
    solution.write()

def verify(instance: Instance, solution: Solution) -> int:
    if any([any(v <= 0 for v in x) or any(v > instance.size for v in x) for x in solution.patient_schedules]):
        print("wrong patient index (not in [1,instance.size])", file=sys.stderr)
        return 0

    if any([any(v <= 0 for v in x) or any(v > 5 for v in x) for x in solution.task_sequences]):
        print("wrong machine index (not in [1,instance.size])", file=sys.stderr)
        return 0

    for g in range(5):
        used = [0] * instance.size
        for el in solution.patient_schedules[g]:
            used[el-1] += 1
        if any([e > 1 for e in used]):
            print("patient index used more than once", file=sys.stderr)
            return 0
        if any([e == 0 for e in used]):
            print("patient index not used", file=sys.stderr)
            return 0

    for p in range(instance.size):
        used = [0] * 5
        for el in solution.task_sequences[p]:
            used[el-1] += 1
        if any([e > 1 for e in used]):
            print("machine index used more than once", file=sys.stderr)
            return 0
        if any([e == 0 for e in used]):
            print("machine index not used", file=sys.stderr)
            return 0

    return get_score(instance, solution)

    
def verifier(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename, load=True)

    score = verify(instance, solution)
    print(score)
    return 0

def generator(args):
    if args.size == None:
        print("The size of the instance needs to be provided.", file=sys.stderr)
        exit(1)
    instance = Instance(args.instance_filename, args.size)
    instance.clear()
    instance.write()
    return 0

def parse_args():
    parser = argparse.ArgumentParser(description="Instance and Solution processor")
    parser.add_argument("instance_filename", type=str, nargs="?", default=None, help="name of the instance input file")
    parser.add_argument("solution_filename", type=str, nargs="?", default=None, help="name of the solution output file")
    parser.add_argument("time", type=int, nargs="?", default=None, help="time parameter")
    parser.add_argument("--program", type=str, help="run any of: solution, generator, verifier (defaults to solution)", default="solution")
    parser.add_argument("--size", type=int, help="size of the instance to generate")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.instance_filename == None:
        return 1

    match args.program:
        case "solution":
            if args.instance_filename == None:
                return 1
            return solution(args)
        case "verifier":
            return verifier(args)
        case "generator":
            return generator(args)
        case _:
            return "invalid program name"

if __name__ == "__main__":
    main()
