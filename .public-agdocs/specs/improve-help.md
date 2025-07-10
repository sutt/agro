Currently copied below is what prints for help.

Update this to reflect more concise and more informative and utilize best practices.

contents:

usage: agro [-h] [--version] [-v] [-q]

A script to manage git worktrees for agent-based development.

options:
  -h, --help     show this help message and exit
  --version      Show program's version number and exit.
  -v, --verbose  Increase verbosity. -v for debug, -vv for command output.
  -q, --quiet    Suppress all output except warnings and errors.

Main command:
  exec [args] [taskfile] [num-trees] [exec-cmd]   
                                
        Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees to create.
          -t <indices>          Specified worktree indice(s) (e.g., '1,2,3').
          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree
          ...others             See below.

Other Commands:
  surrender [indices]           Kill running agent processes (default: all).
  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <pattern>                Delete local branches matching a regex pattern.
  make <index>                  Create a new worktree.
  delete <indices>|--all        Delete one, multiple, or all worktrees.
  task [task-name]              Create a new task spec file and open it.
  init                          Initialize agro project structure.
  mirror                        Mirror internal docs to public docs directory.
  help                          Show this help message.

Common options for 'make' and 'exec':
  --fresh-env         When creating a worktree, use .env.example as the base instead of .env.
  --no-env-overrides  When creating a worktree, do not add port overrides to the .env file.

Options for 'muster':
  -s, --server        Run command as a background server, redirecting output and saving PID.
  -k, --kill-server   Kill the background server and clean up pid/log files.
    
Options for 'init':
  --conf              Only add a template agro.conf.yml to .agdocs/conf
