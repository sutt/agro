create an "agro diff" command:
> agro diff [opts] [branch-pattern]

This command will call "git diff [args]" command on each worktree that matches branch-pattern. or if branch-pattern is blank.

This is roughly the equivalent of what "agro muster 'git diff HEAD~1' output" does by running a command on each worktree that matches branch-pattern. Like muster, make sure this command sufficiently prints the output of shell commands to the user's terminal.

the opts for agro diff should include "--stat" which gets passed to the underlying shell out to "git diff..."

By default, the underling git diff command should be between when the agent started its work and finished. This should be "git diff tree/tX HEAD" where X in tree/tX is the index of the worktree the command is being run on.