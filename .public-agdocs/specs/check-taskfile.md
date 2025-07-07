When the task file specified in the <taskfile> specified as an arg to agro exec is not found, the exec command still: creates the worktree, new dev env, and launches maider.
Add behavior to check the taskfile exists and it's not empty before doing those processes.
