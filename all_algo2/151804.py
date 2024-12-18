import sys

class Worker:
	def __init__(self, id):
		self.availability = 0
		self.tasks_assigned = []
		self.id = id

class Task:
	def __init__(self, id, start_time=0, deadline=0):
		self.id = id
		self.start_time = start_time
		self.deadline = deadline
		self.execution_times = []

def main(input_filename, solution_filename):
	in_file = open(input_filename, "r")
	worker_count = 5
	task_count = int(in_file.readline().strip())
	workers = [Worker(i) for i in range(worker_count)]
	tasks = []
	for i in range(task_count):
		new_task = Task(i+1)
		line = in_file.readline().strip()
		numbers = [int(word) for word in line.split()]
		for worker in range(worker_count):
			new_task.execution_times.append(numbers.pop(0))
		new_task.start_time = numbers.pop(0)
		new_task.deadline = numbers.pop(0)
		tasks.append(new_task)
	in_file.close()

	failed_tasks = []
	tasks.sort(key= lambda x: x.start_time)
	for task in tasks:
		best_end_time = task.deadline
		best_worker = 0
		for worker in workers:
			end_time = max(worker.availability, task.start_time) + task.execution_times[worker.id]
			if end_time < best_end_time:
				best_worker = worker.id
				best_end_time = end_time
		if best_end_time < task.deadline:
			worker = workers[best_worker]
			worker.tasks_assigned.append(task.id)
			worker.availability = best_end_time
		else:
			failed_tasks.append(task.id)
	for task in failed_tasks:
		workers[0].tasks_assigned.append(task)

	sol_file = open(solution_filename, "w")
	sol_file.write(f"{len(failed_tasks)}\n")
	for worker in workers:
		for task in worker.tasks_assigned:
			sol_file.write(f"{task} ")
		sol_file.write("\n")
	sol_file.close()
            

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Error, expected input filename and solution filename")
	else:
		main(sys.argv[1], sys.argv[2])
