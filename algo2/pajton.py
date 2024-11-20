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
        self.jobs: List[List[int]] = [[],[],[],[],[]]
        if load:
            self.read(self.file_stream)

    def read(self, input_stream=None):
        if input_stream == None:
            input_stream = self.file_stream

        self.score = int(input_stream.readline().strip())
        for i in range(5):
            self.jobs[i] = [int(x)-1 for x in input_stream.read().strip().split()]

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream

        output_stream.write(f"{self.score}\n")
        for i in range(5):
            output_stream.write(" ".join(str(job+1) for job in self.jobs[i]) + "\n")

class Instance(File):
    def __init__(self, filename: str = "", size: int = 0, load: bool = False):
        super().__init__(filename)
        self.size = size
        self.work_times: List[List[int]] = [[],[],[],[],[]]
        self.ready_times: List[int] = []
        self.deadlines: List[int] = []

        if load:
            self.read(self.file_stream)
        if size > 0 and not load:
            self.generate(size)

    def read(self, input_stream=None):
        if input_stream == None:
            input_stream = self.file_stream

        self.size = int(input_stream.readline().strip())
        for _ in range(self.size):
            line = input_stream.readline().split()

            for i,j in zip(range(5), line[0:-2]):
                self.work_times[i].append(int(j))

            self.ready_times.append(int(line[-2]))
            self.deadlines.append(int(line[-1]))

    def write(self, output_stream=None):
        if output_stream == None:
            output_stream = self.file_stream

        output_stream.write(f"{self.size}\n")
        for i in range(self.size):
            for j in range(5):
                output_stream.write(f"{self.work_times[j][i]} ")
            output_stream.write(f"{self.ready_times[i]} {self.deadlines[i]}\n")

    def generate(self, n: int):
        random.seed(1)
        self.size = n
        # Generate random work times for each of the 5 machines and each task
        self.work_times = [[random.randint(1, 20) for _ in range(n)] for _ in range(5)]
    
        # Generate random ready times for each task
        self.ready_times = [random.randint(0, 50) for _ in range(n)]
    
        # Generate random deadlines for each task, ensuring they are not too close to ready times
        self.deadlines = [self.ready_times[i] + random.randint(10, 60) for i in range(n)]


def get_score(instance: Instance, solution: Solution) -> int:
    score = 0
    for i in range(5):
        current_time=0
        for job in solution.jobs[i]:
            current_time = max(instance.ready_times[job], current_time)
            current_time += instance.work_times[i][job]
            score = score if current_time <= instance.deadlines[job] else score + 1
    return score

def solution(args):
    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename)

    # solution.proc = list(range(instance.size))
    solution.jobs[0] = list(range(instance.size))
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
    if any(job+1 <= 0 or job+1 > instance.size for job in used_jobs):
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

    match args.program:
        case "solution":
            return solution(args)
        case "verifier":
            return verifier(args)
        case "generator":
            return generator(args)
        case _:
            return "invalid program name"

if __name__ == "__main__":
    main()
