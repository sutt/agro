refactor logging in this script:
- convert prints to logger
    - add several logger layers which correspond to running agro with -v (default) , -vv, -vvv. Also add an option for mostly silent run.
- suppress output from shell commands (stderr / stdout) from getting printing from the script run, execept under higher logger levels like -vv -vvv.

