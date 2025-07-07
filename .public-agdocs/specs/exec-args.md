swap the order and logic of args for exec: 
- current: agro exec <index> <taskfile>
- desired: agro exec <taskfile> [indicies]

Changes:
1. order swaps
2. index -> indices, allow comma separated indices to kick off multiple trees
3. make indicies optional, by default run make one new worktree on a non-existing worktree, 
 - e.g. if there is trees/ t1, t2, t3, create one on t4, or 
 - e.g. if these is trees/ t1, t3, create one for t2