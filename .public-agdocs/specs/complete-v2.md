let's add cli completion for the branch-pattern arguments in this app.

So for commands like muster, diff, grab, and others, if the user entering a branch pattern you should the git repo in the cwd for available branches and match to the input prefix (if any) supplied by the user and complete the full branch name (if no conflicts)

if the user hasn't supplied any input typed, assume the prefix is "output" or the value of WORKTREE_OUTPUT_BRANCH_PREFIX