# Agro

A script to manage git worktrees for agent-based development. This tool simplifies creating, managing, and running processes within isolated worktrees, each with its own environment configuration.

## Quickstart

**Create and commit a spec file and pass to an agent**
```bash
mkdir .agdocs
touch .agdocs/hello-world.md
echo "add hello world to the readme of this project" > .agdocs/hello-world.md

git add .agdocs
git commit -m "spec: hello-world"

agro exec 1 .agdocs/hello-world.md

```

**Output**

```bash
Attempting to remove existing worktree for index 1 (if any)...
♻️  Cleanup for index 1 complete.

Creating new worktree for index 1...
HEAD is now at caa7ed1 refactor: name package agro
Copying .env to trees/t1/.env
Adding worktree overrides to trees/t1/.env
Setting up Python environment in trees/t1...

🌴 New worktree created successfully.
   Worktree: trees/t1
   Branch: tree/t1
   API Port: 8001
   DB Port:  5433

🌱 Working on new branch: output/ignore-swap.1

🏃 Agent for index 1 started successfully.
   Worktree: /home/user/tools_dev/agscript/trees/t1
   Task file: /home/user/tools_dev/agscript/.agdocs/specs/ignore-swap.md
   Branch: output/ignore-swap.1
   Start time: 2025-07-03 14:27:36
   PID: 519708 (saved to /home/user/tools_dev/agscript/.agdocs/swap/t1.pid)
   Log file: /home/user/tools_dev/agscript/trees/t1/maider.log

```

Now let's a second agent (on the same task)

```bash
🌴 New worktree created successfully.
   Worktree: trees/t2
   Branch: tree/t2
   API Port: 8002
   DB Port:  5434

🏃 Agent for index 2 started successfully.
   Worktree: /home/user/tools_dev/agscript/trees/t2
```


Now wait for the both agents to finish and examine the results

```bash
agro exec 1 .agdocs/hello-world.md
```

```bash
# execute pytest in both worktrees
agro muster 'uv run pytest' 1,2

# start the local server on both worktrees
# start your browser on localhost:8000, localhost:8001
# the --server flag allows the dispatch to be non-blocking 
# across each worktree
agro muster 'uv run app/main.py' 1,2 --server

# use --kill-server to destroy the worktree servers running
# in the background
argo muster '' 1,2 --kill-server

```




## Commands

### Worktree / Agent Dispatch
- exec
- muster
- surrender

### Git Helpers
- grab
- fade

### Worktree Utility
- make
- delete


### Full Help

```bash

usage: agro [-h]

A script to manage git worktrees for agent-based development.

options:
  -h, --help  show this help message and exit

Available commands:
  make <index>                  Create a new worktree.
  delete <index>                Delete the worktree with the given index.
  exec <index> <taskfile> ...   Run an agent in a new worktree.
  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <pattern>                Delete local branches matching a regex pattern.
  surrender [indices]           Kill running agent processes (default: all).
  help                          Show this help message.

Common options for 'make' and 'exec':
  --fresh-env         When creating a worktree, use .env.example as the base instead of .env.
  --no-env-overrides  When creating a worktree, do not add port overrides to the .env file.
  --no-all-extras     Do not install all extra dependencies when running 'uv sync'.

Options for 'muster':
  -s, --server        Run command as a background server, redirecting output and saving PID.
  -k, --kill-server   Kill the background server and clean up pid/log files.

```


## Installation

You can install this tool and its dependencies from the local project directory using `uv`: `uv tool install . --no-cache`

From the root of the project directory, run:

```
./redeploy
```


## Layout

The script creates two directories in the code repo:
- `.agdocs/` - specs, configs, logs for agro
- `trees/` - root for worktrees (gitignored)

```
- .agdocs
    - specs/
        - task1
        - task2
        ...
    - swap
        - shared logs 
        - (gitignored)
- <your-code>
    ...
- <your-configs>
    ...
- trees/
    - t1
        - <your-code>
        - <t1-configs>
    - t2
        - <your-code>
        - <t1-configs>
    ...
```

#### Worktree Configuration

agro will port `.env` files into the worktrees and override particular settings for parallel execution environments. And clone the environment (currently only supported for `uv`) from the main workspace into the 

```agro muster 'uv run which python' 1,2```

```bash

--- Running command in t1 (trees/t1) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t1/.venv/bin/python

--- Running command in t2 (trees/t2) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t2/.venv/bin/python

```