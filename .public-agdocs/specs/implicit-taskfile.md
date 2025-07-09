Update the cli logic to allow taskfile to be an optional and positional argument. 

Update the args to have a -c as an alias for exec-cmd.

- Remember taskfile is always a str, num-trees is always int, exec-cmd is always a str. 
- Num-tree and exec-cmd can swap places positionally

the new docs are
  exec [args] [taskfile] [num-trees] [exec-cmd]   
                                
        Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees to create.
          -t <indices>          Specified worktree indice(s) (e.g., '1,2,3').
          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree
          ...others             See below.


In the case when taskfile is not passed it will be searched for:

- if found the user will get a Prompt to confirm before proceeding with the full command
- if not found the user will be notified, with expected vs actual message and command terminated
(When taskfile is passed explicitly the user should not a prompt confirm)

The takfile that will be selected to pass onto the main command is the most recently modified .md file in ./.agdocs/specs/ directory (or whatever the config points to).

In the case where the taskfile is pass explicitly:

- The taskfile can be searched to match:
    - in .agdocs/specs/ by default (although use config vars)
    - or possibly at root or the path specified

- The taskfile will be a fuzzy match here since taskfiles are .md's and the taskfile might or might not be passed with this extension, and a full relative path might be specified or not in the case assuming you'll look in the default directory. Also the files could be at root, don't worry about the case of collisiosn other than just ignore the user.
    - user could say: agro exec add-db # which will search for .agdocs/specs/add-db.md or ./add-db.md 
    - user could say: agro exec make-readme.md # which will search for .agdocs/specs/make-readme.md or ./make-readme.md
    - user could say: agro exec .agdocs/specs/add-db.md # which will search for only .agdocs/specs/add-db.md
    This functionality of fuzzy matching the taskfile input string to possible existing files in the repo should be include both 

Update and refactor cli tests as needed for these updates, and add new tests for this functionality.