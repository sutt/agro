add a .agswap directory on worktree creation with a .gitignore inside this log directory (contents=*).
If running from exec_agent:
- write the prompt-file into the log directory with the same filename as the src.
- pipe the stdout / stderr from maider into this directory.