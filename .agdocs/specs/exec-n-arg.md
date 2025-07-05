Currently this is the specified argument call for agro exec:
    exec <taskfile> [indices]  

Add cli parsing and functionality to enable this new form of cli call:
    exec <taskfile> [num-trees] [-n num-trees] [-t tree-indices]
    
Where 
    - tree-indices: is the same same as the existing indices variable, a single number or comma separated multiple numbers specifying the index of the worktree the agent should be alunched on.
    num-trees
    - num-trees: is an integer representing the number of trees to create, these should be "new" worktrees that haven't been created yet, similiar to how current behavior leaving the indices argument missing right now: e.g.:
        - if there is t1, t2 in trees/ it will create a t3
        - if there if t3, t4 in trees it will create a t1
    But with this update, if -n 2 is specified:
        - if there is t1, t2 in trees/ it will create a t3, t4
        - if there if t3, t4 in trees it will create a t1, t2
        



