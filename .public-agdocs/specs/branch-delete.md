add a command to agscript "fade" which will delete branches from the git repo that match a certain pattern. 

The command should first do a dry run then create a Y/n prompt to continue the real run.

- dry-run (but also printout 1 branch name for each line)
> git branch | grep "your-pattern-here" | sed 's/^[ *+]*//' | xargs echo

- non dry-run
> git branch | grep "your-pattern-here" | sed 's/^[ *+]*//' | xargs git branch -D