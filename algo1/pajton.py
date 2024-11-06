import argparse
import random
import time
from typing import List, Tuple
import os

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

    def read(self, input_stream):
        raise NotImplementedError("Subclasses must implement read")

    def write(self, output_stream):
        raise NotImplementedError("Subclasses must implement write")

class Solution(File):
    def __init__(self, filename: str = "", load: bool = False):
        super().__init__(filename)
        self.score = 0
        self.proc: List[int] = []
        if load:
            self.read(self.file_stream)

    def read(self, input_stream):
        self.score = int(input_stream.readline().strip())
        self.proc = [int(x) - 1 for x in input_stream.read().strip().split()]

    def write(self, output_stream):
        output_stream.write(f"{self.score}\n")
        output_stream.write(" ".join(str(i + 1) for i in self.proc) + "\n")

class Instance(File):
    def __init__(self, filename: str = "", size: int = 0, load: bool = False):
        super().__init__(filename)
        self.size = size
        self.begin_end: List[Tuple[int, int]] = []
        self.cost: List[List[int]] = []
        if load:
            self.read(self.file_stream)
        if size > 0 and not load:
            self.generate(size)

    def read(self, input_stream):
        self.size = int(input_stream.readline().strip())
        self.begin_end = [tuple(map(int, input_stream.readline().strip().split())) for _ in range(self.size)]
        self.cost = [list(map(int, input_stream.readline().strip().split())) for _ in range(self.size)]

    def write(self, output_stream):
        output_stream.write(f"{self.size}\n")
        for start, end in self.begin_end:
            output_stream.write(f"{start} {end}\n")
        for row in self.cost:
            output_stream.write(" ".join(map(str, row)) + "\n")

    def generate(self, n: int):
        random.seed(time.time())
        self.size = n

        d_mean = self.size + self.size // 10 + self.size // 8
        d_stddev = 4 * self.size + d_mean
        p_mean = self.size // 10
        p_stddev = self.size // 10 + p_mean
        s_mean = self.size // 100 + 5
        s_stddev = s_mean

        self.begin_end = [(max(0, int(random.gauss(p_mean, p_stddev))),
                           max(0, int(random.gauss(d_mean, d_stddev))))
                          for _ in range(self.size)]
        
        self.cost = [[0 if i == j else max(0, int(random.gauss(s_mean, s_stddev)))
                      for j in range(self.size)]
                     for i in range(self.size)]

def get_score(instance: Instance, solution: Solution) -> int:
    score = 0
    current_time = 0
    for idx, task in enumerate(solution.proc):
        p_j, d_j = instance.begin_end[task]
        if idx > 0:
            previous_task = solution.proc[idx - 1]
            current_time += instance.cost[previous_task][task]
        current_time += p_j
        C_j = current_time
        Y_j = min(p_j, max(0, C_j - d_j))
        score += Y_j
    return score

def parse_args():
    parser = argparse.ArgumentParser(description="Instance and Solution processor")
    parser.add_argument("instance_filename", type=str, help="name of the instance input file")
    parser.add_argument("solution_filename", type=str, help="name of the solution output file")
    parser.add_argument("time", type=int, help="time parameter")
    return parser.parse_args()

def main():
    args = parse_args()

    instance = Instance(args.instance_filename, load=True)
    solution = Solution(args.solution_filename)

    solution.proc = list(range(instance.size))  # Populate with task indices
    solution.score = get_score(instance, solution)

    solution.clear()
    solution.write(solution.file_stream)
    solution.file_stream.close()

if __name__ == "__main__":
    main()

