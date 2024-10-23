import subprocess
import sys

def get_scores_from_file(file_path, metric):
    scores = []

    # Read each ID from the file
    with open(file_path, 'r') as file:
        for line in file:
            person_id = line.strip()  # Get person ID
            if person_id:  # Check if line is not empty
                try:
                    # Run the get-score.sh script
                    result = subprocess.run(
                        ['./get-score.sh', person_id, metric], 
                        capture_output=True, 
                        text=True,
                        check=True
                    )
                    # Split the output into lines and strip whitespace
                    score_list = result.stdout.strip().splitlines()
                    scores.append(score_list)
                except subprocess.CalledProcessError as e:
                    print(f"Error running get-score.sh for ID {person_id}: {e}")

    return scores

def print_scores(scores):
    # Create a grid format for the scores
    max_length = max(len(score) for score in scores)  # Determine the longest score list
    for i in range(max_length):
        row = []
        for score in scores:
            # Append the score or an empty string if this score list is shorter
            row.append(score[i] if i < len(score) else '')
        print(';'.join(row))

def main():
    file_path = 'ludzie.txt'  # Path to the input file
    scores = get_scores_from_file(file_path, sys.argv[1])
    print_scores(scores)

if __name__ == '__main__':
    main()
