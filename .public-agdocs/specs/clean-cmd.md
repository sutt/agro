add an "agro clean" command:
agro clean [opts] [branch-pattern]
opts: --soft, --hard (default)

This command will act as compound command for the existing "agro delete" + "agro fade", where it erases the branch(es) and/or worktrees associated with the branch pattern if supplied, and if not supplied of all the worktrees all the branches matching the WORKTREE_OUTPUT_BRANCH_PREFIX.

Provide similiar dry-run printout of all trees and branches that will be erased with this functionality along with confirmation before proceeding. Note that "agro state" already creates a printout that connects the respective worktrees with their branches like:
t1: output/add-about.1
t2: output/add-about.2
t3: output/add-about.3
t4: output/add-about.4

The opts available will be --soft and --hard. If no opt is supplied the default is --hard. When --soft is used, only the worktree associated with the branch pattern will be deleted, not the branches. For the default --hard, both the worktrees and branches will be deleted.
