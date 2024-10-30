import os
import sys
import threading
import time


def open_file(name):
    try:
        file = open(name, 'r')
        return file
    except FileNotFoundError:
        print(f"File {name} not found")
        return None


def process_instance_file(file):
    number_of_sets = int(file.readline())

    jobs = []
    expected_finish_times = []
    for i in range(number_of_sets):
        line = file.readline()
        line_split = line.split()

        jobs.append(int(line_split[0]))
        expected_finish_times.append(int(line_split[1]))

    job_change_time_matrix = []
    for i in range(number_of_sets):
        line = file.readline()
        line_split = line.split()

        row = []
        for item in line_split:
            row.append(int(item))
        job_change_time_matrix.append(row)

    return number_of_sets, jobs, expected_finish_times, job_change_time_matrix


def save_result_to_file(file_name, lateness, sequence):
    try:
        with open(file_name, 'w') as file:
            file.write(f"{lateness}\n")
            file.write(' '.join(map(str, sequence)) + '\n')
        print(f"Results were saved to file {file_name}.")
    except Exception as e:
        print(f"File not found {file_name}: {e}")


def calculate_lateness(jobs, expected_finish_times, job_change_time_matrix, sequence):
    calculated_lateness = 0
    current_time = 0
    for i in range(len(sequence)):
        job_index = sequence[i] - 1
        job_duration = jobs[job_index]
        current_time += job_duration
        expected_finish_time = expected_finish_times[job_index]
        delay = min(job_duration, max(0, current_time - expected_finish_time))
        calculated_lateness += delay

        is_last = i == len(sequence) - 1
        if not is_last:
            next_job_index = sequence[i + 1] - 1
            current_time += job_change_time_matrix[job_index][next_job_index]

    return calculated_lateness


def find_optimal_sequence(number_of_sets, jobs, expected_finish_times, job_change_time_matrix):
    initial_sequence = list(map(lambda i: i + 1, sorted(range(number_of_sets), key=lambda i: expected_finish_times[i])))

    best_sequence = initial_sequence
    best_lateness = calculate_lateness(jobs, expected_finish_times, job_change_time_matrix, best_sequence)

    return best_lateness, best_sequence


def test_run():
    index = input("Type index: ")
    size = 50
    file_name = f"in_{index}_{size}.txt"
    file = open_file(file_name)

    if file:
        print('Processing file...')
        number_of_sets, jobs, expected_finish_times, job_change_time_matrix = process_instance_file(file)
        print('Finding sequence...')
        lateness, optimal_sequence = find_optimal_sequence(number_of_sets, jobs, expected_finish_times,
                                                           job_change_time_matrix)

        print(lateness)
        print(' '.join(map(str, optimal_sequence)))
        save_result_to_file(f"out_{index}_50.txt", lateness, optimal_sequence)


def production_run():
    instance_filename = sys.argv[1]
    result_filename = sys.argv[2]

    file = open_file(instance_filename)

    if file:
        number_of_sets, jobs, expected_finish_times, job_change_time_matrix = process_instance_file(file)
        lateness, optimal_sequence = find_optimal_sequence(number_of_sets, jobs, expected_finish_times,
                                                           job_change_time_matrix)
        print(lateness)
        print(' '.join(map(str, optimal_sequence)))
        save_result_to_file(result_filename, lateness, optimal_sequence)
    else:
        print(f"The file {instance_filename} does not exist.")
    os._exit(0)


def run_with_timeout(timeout, function):
    task_thread = threading.Thread(target=function)
    task_thread.start()

    time.sleep(timeout)
    if task_thread.is_alive():
        print('Time limit exceeded!')
        os._exit(0)


def main():
    time_limit = int(sys.argv[3])

    run_with_timeout(time_limit, production_run)


if __name__ == "__main__":
    main()
