
create a --server flag for the muster command that appends two features to the command as passed:
1. suppress the output by appending something like: "> server.log 2>&1"
2. capture and save the pid of the program started by the shell command, something like: "& echo $! > server.pid"
- make sure these files are being output in the agents worktree, not the root git workspace.

So the user should be able to do something like this:
- pass in command: agscript muster 'python app/main.py' 1,2 --server
- and get behavior like this:
agscript muster 'python app/main.py > server.log 2>&1 & echo $! > server.pid' 

And add a flag --kill-server to muster that will do something like this
agscript muster 'kill $(cat server.pid) && rm server.pid server.log' '1,2'
when called as: agscript muster 'dummy command' 1,2 --kill-server
