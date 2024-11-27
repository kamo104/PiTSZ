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
        # Open in 'r+' mode to prevent erasure of contents and allow reading and writing
        try:
            self.file_stream = open(self.filename, 'r+')
        except FileNotFoundError:
            # If file doesn't exist, create it in 'w+' mode initially
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
        self.jobs: List[List[int]] = []
        if load:
            self.read()

    def read(self, input_stream=None):
        if input_stream == None:
            input_stream = self.file_stream
            
        lines = input_stream.readlines()

        self.score = int(lines[0].strip())
        for line in lines[1:]:
            values = list(map(int, line.strip().split()))
            self.jobs.append(values)

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream

        output_stream.write(f"{self.score}\n")
        for i in range(5):
            output_stream.write(" ".join(str(job) for job in self.jobs[i]) + "\n")


class Instance(File):
    def __init__(self, filename: str = "", size: int = 0, load: bool = False):
        super().__init__(filename)
        self.size = size
        self.tasks = []  # List of dictionaries to store task info
        if load:
            self.read()
        elif size > 0:
            self.generate(size)

    def read(self, input_stream=None):
        if input_stream == None:
            input_stream = self.file_stream
            
        lines = input_stream.readlines()

        # First line: number of tasks
        self.size = int(lines[0].strip())
        if len(lines) - 1 != self.size:
            raise ValueError(f"Expected {self.size} tasks, but found {len(lines) - 1} lines of task data.")

        self.tasks = []
        for idx, line in enumerate(lines[1:], start=1):
            values = list(map(int, line.strip().split()))
            if len(values) != 7:
                raise ValueError(f"Line {idx + 1} should contain exactly 7 integers (found {len(values)}).")
            
            task = {
                'pkj': values[:5],  # Processing times for 5 workers
                'rj': values[5],    # Ready time
                'dj': values[6],    # Deadline
            }
            self.tasks.append(task)

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream

        output_stream.write(f"{self.size}\n")
        for task in self.tasks:
            pkj = " ".join(map(str, task['pkj']))
            rj = task['rj']
            dj = task['dj']
            output_stream.write(f"{pkj} {rj} {dj}\n")


    def generate(self, n: int):
        random.seed(1)
        self.size = n
        self.tasks = []  # Clear existing tasks and generate new ones

        for _ in range(n):
            # Generate random work times for each of the 5 workers
            pkj = [random.randint(1, 20) for _ in range(5)]

            # Generate random ready time
            rj = random.randint(0, 50)

            # Generate random deadline, ensuring it's not too close to ready time
            dj = rj + random.randint(10, 60)

            # Append the task to the list
            self.tasks.append({'pkj': pkj, 'rj': rj, 'dj': dj})

def get_score(instance: Instance, solution: Solution) -> int:
    score = 0

    # print(solution.)
    for worker in range(5):  # Iterate over each worker
        current_time = 0

        for job in solution.jobs[worker]:  # Iterate over jobs assigned to the worker
            task = instance.tasks[job-1]    # Access task data from the tasks list
            w_j = task['pkj'][worker]     # Work time for the specific worker
            r_j = task['rj']              # Ready time
            d_j = task['dj']              # Deadline

            # Calculate start and finish times
            start_time = max(r_j, current_time)
            finish_time = start_time + w_j

            # Update score if the task finishes after its deadline
            if finish_time > d_j:
                score += 1

            # Update current time for the worker
            current_time = finish_time

    return score        

def solution(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename)

    solution.size = instance.size
    solution.jobs = [[x+1 for x in range(instance.size)],[],[],[],[]]
    solution.score = get_score(instance, solution)

    solution.clear()
    solution.write()

def verify(instance: Instance, solution: Solution) -> Tuple[bool, int]:
    # Check if the number of processes in solution matches the instance size
    used_jobs = list(chain.from_iterable(solution.jobs))
    if instance.size != len(used_jobs):
        print(f"The number of jobs used({len(used_jobs)}) is different than in the instance({instance.size})", file=sys.stderr)
        return False, 0

    # Check if each process in the solution is within the allowed range
    if any(job <= 0 or job > instance.size for job in used_jobs):
        # lst = [job for job in used_jobs if job <= 0 or job > instance.size]
        print(f"The solution contains a job outside the allowed range ([1:{instance.size}])", file=sys.stderr)
        return False, 0

    # Check if all processes are unique and match the expected count
    used = [False] * instance.size
    for job in used_jobs:
        used[job - 1] = True

    if not all(used):
        missing_process = (used.index(False) + 1)%instance.size+1
        print(f"The solution doesn't include job {missing_process}", file=sys.stderr)
        return False, 0

    # Calculate the score and check if it matches the reported score in the solution
    calculated_score = get_score(instance, solution)
    if calculated_score != solution.score:
        print(f"The reported score ({solution.score}) is different from the calculated ({calculated_score})", file=sys.stderr)
        return False, 0

    return True, calculated_score

def verifier(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename, load=True)

    res, score = verify(instance,solution)
    if(res==False):
        return 1
    print(score,end="")
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
