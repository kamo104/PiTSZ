import argparse
import random
import time
from typing import List, Tuple
from itertools import chain
import sys

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
        if input_stream == None:
            input_stream = self.file_stream

        raise NotImplementedError("Subclasses must implement read")

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream

        raise NotImplementedError("Subclasses must implement write")


class Solution(File):
    def __init__(self, filename: str = "", load: bool = False):
        super().__init__(filename)
        self.score = 0
        self.schedule = []
        if load:
            self.read()

    def read(self, input_stream=None):
        if input_stream == None:
            input_stream = self.file_stream
            
        lines = input_stream.readlines()
        self.score = int(lines[0].strip())
        self.schedule = [list(map(int, line.split())) for line in lines[1:]]

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream
        
        output_stream.write(f"{self.score}\n")
        for row in self.schedule:
            output_stream.write(" ".join(map(str, row)) + "\n")


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
        if output_stream == None:
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
    machine_count = 5
    

    machine_times = [0] * machine_count
    completion_times = [0] * n
    
    total_cost = 0

    for task_id, task in enumerate(instance.tasks, start=0):
        for machine in range(machine_count):
            start_time = max(
                machine_times[machine],
                completion_times[task_id - 1] if task_id - 1 < n else 0,
                task['r']
            )
            end_time = start_time + task[f'p{machine + 1}']
            machine_times[machine] = end_time
            completion_times[task_id - 1] = end_time
        

        task_duration = completion_times[task_id - 1] - task['r']
        total_cost += task_duration * task['w']
    
    return total_cost

def solution(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename)

    start_time = time.time()
    best_score = float('inf')
    best_schedule = None

    num_workers = 5

    tasks = list(range(1, instance.size + 1))
    random.shuffle(tasks)

    schedule = [tasks[i::num_workers] for i in range(num_workers)]
    for _ in range(100):
        random.shuffle(tasks)
        candidate_schedule = [tasks[i::num_workers] for i in range(num_workers)]
        candidate_solution = Solution()
        candidate_solution.schedule = candidate_schedule
        candidate_solution.score = get_score(instance, candidate_solution)

        if candidate_solution.score < best_score:
            best_score = candidate_solution.score
            best_schedule = candidate_schedule

    solution.schedule = best_schedule
    solution.score = best_score
    solution.clear()
    solution.write()


def verify(instance: Instance, solution: Solution) -> Tuple[bool, int]:
    try:
        calculated_score = get_score(instance, solution)
        return True, calculated_score
    except IndexError as e:
        print(f"Verification failed: {e}", file=sys.stderr)
        return False, 0

    
def verifier(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename, load=True)

    res, score = verify(instance, solution)
    if not res:
        print("Verification failed.", file=sys.stderr)
        return 1
    print(score, end="")
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
