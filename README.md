# Task ordering problem

**The source code is contained in algo{1..3} folders for each problem variation**


### Generating an instance:
To generate an instance run the python script with option: --program generator <br>
``
script.py instance_filename --program generator
``

### Solving an instance:
To solve an instance run the python script with the following arguments: <br>
``
script.py instance_filename solution_filename timeout
``

### Verifying an instance:
To verify an instance run the python script with option: --program verifier <br>
``
script.py instance_filename solution_filename --program verifier
``


### Batch scoring and verifying
To run algorithms in parallel and verify them use the script: <br>
``
run.sh
`` <br>
The results will be logged into

