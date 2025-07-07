We're writing a wrapper around git worktree functionality.

Assume the "root workspace" / "root worktree" is master and there are multiple worktrees being created and destroyed that are checked out to their own branches.

We want to be able to checkout a branch that another worktree may currently be on. So we need to create a copy of that branch or move the other worktree off of that branch. For example in the following we see output/add-about.1 has a + next to it showing that branch is checked out on another worktree so if we're on the main worktree on the master branch, we can't do git checkout output/add-about-1

* master
+ output/add-about.1
+ output/serve-main.1
  tree/t1
  tree/t2

Add a command to agscript "grab" <branch-name> that will attempt to checkout the branch name normally, and if it's refused because theres already another worktree with that branch checkedout, it creates a copy of the branch with name `<branch-name>.copy`.

If possible allow bash autocomplete of the branch name when typing the command `agscript grab ...`.