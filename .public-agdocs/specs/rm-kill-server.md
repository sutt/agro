refactor the --server and --kill-server cli flags and functionality: make these work off the pattern establish in MUSTER_COMMON_CMDS where the command string is specified in defaults / config file, and can be invoked with "agro muster -c <command_key>"

- the existing flags for --server and --kill-server should be removed from the interface.
- Add these alias and their full command to the defaults and conf init functionality for muster -c

Add tests to verify the new cli bahvior is working an d succesfully mock calling these command