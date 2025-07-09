# Agro

A script to manage git worktrees for agent-based development. This tool simplifies creating, managing, and running processes within isolated worktrees, each with its own environment configuration.

[![PyPI version](https://img.shields.io/pypi/v/agro)](https://pypi.org/project/agro/)


## Quickstart

Install with `pip` or `uv tool`:

```bash
pip install agro
uv tool install agro
```

#### Local Development Install
You can install this tool and its dependencies from the local clone of the project directory using `uv`: 

```bash
git clone git@github.com:sutt/agro.git"
cd agro
uv tool install . --no-cache
```

For local dev updates run the `./redeploy` script to reinstall the local repo as `agro`.

### At a Glance - Hello, World!

**Warning: this workflow is deprecated as of v0.1.4, see this [case study](./docs/case-studies/aba-1.md) for a better tutorial for for working with v0.1.4**

**0. Clone the Demo Repo**


```bash
git clone git@github.com:sutt/agro-demo.git
cd agro-demo

uv sync
```

Use the pre-built app + built in task in `.agdocs/specs`.

**1. Launch two agents in parallel**
- target worktrees 1 and 2.

```bash
$ agro exec 1 .agdocs/specs/add-about.md 
$ agro exec 2 .agdocs/specs/add-about.md 
```

**Basic Output**
- notice the git worktree / branch management + launch of aider

```bash
♻️  Cleanup for index 1 complete.
🌴 New worktree created successfully.
   Worktree: trees/t1
   API Port: 8001
🌱 Working on new branch: output/add-about.1
🏃 Agent for index 1 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t1
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md

   ...

♻️  Cleanup for index 2 complete.
🌴 New worktree created successfully.
   Worktree: trees/t2
   API Port: 8002
🌱 Working on new branch: output/add-about.2
🏃 Agent for index 2 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t2
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md


```

##### full output
<details>
    <summary>
    expand full output
    </summary>

```bash
♻️  Cleanup for index 1 complete.

Creating new worktree for index 1...
Creating new worktree 't1' at 'trees/t1' on branch 'tree/t1'...
Preparing worktree (new branch 'tree/t1')
HEAD is now at f0b97b1 refactor: .agdocs structure
Copying .env to trees/t1/.env
Warning: Source env file '.env' not found. Creating an empty .env file.
Adding worktree overrides to trees/t1/.env
Setting up Python environment in trees/t1...

🌴 New worktree created successfully.
   Worktree: trees/t1
   Branch: tree/t1
   API Port: 8001
   DB Port:  5433

🌱 Working on new branch: output/add-about.1

Launching agent in detached mode from within trees/t1...

🏃 Agent for index 1 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t1
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
   Branch: output/add-about.1
   Start time: 2025-07-03 17:13:58
   PID: 579494 (saved to /home/user/tools_dev/demo_fastapi/.agdocs/swap/t1.pid)
   Log file: /home/user/tools_dev/demo_fastapi/trees/t1/maider.log
```
**2. Launch a second agent on same task**

**Run command:**
```bash
$ agro exec 2 .agdocs/specs/add-about.md 
```

- notice how work tree is incremented
- notice how API_PORT is incremented

```bash
♻️  Cleanup for index 2 complete.

🌴 New worktree created successfully.
   Worktree: trees/t2
   Branch: tree/t2
   API Port: 8002

🌱 Working on new branch: output/add-about.2

Launching agent in detached mode from within trees/t2...

🏃 Agent for index 2 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t2
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
   Branch: output/add-about.2

```
</details>

**2. Launch Server on each worktree**

```bash
agro muster 'python app/main.py' 1,2 --server
```
- The argument `--server` allows detach mode to run multiple servers out of one shell.

**Output**

```bash
--- Running command in t1 (trees/t1) ---
$ python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t2 (trees/t2) ---
$ python app/main.py > server.log 2>&1 & echo $! > server.pid
```

**Check About Page Contents**
_You could do this in browser as well_

```bash
# check worktree app, here the /about route hasn't been created
curl http://127.0.0.1:8000/about
# {"detail":"Not Found"}

# check worktree t1
curl http://127.0.0.1:8001/about
{"message":"Keep up the great work!"}

# check worktree t2
curl http://127.0.0.1:8002/about
{"message":"This is an about page. Keep up the great work!"}

```

### Or add your own spec to a project

For example:

**Create and commit a spec file and pass to an agent**
```bash
mkdir .agdocs
touch .agdocs/hello-world.md
echo "add hello world to the readme of this project" > .agdocs/hello-world.md

git add .agdocs
git commit -m "spec: hello-world"

agro exec 1 .agdocs/hello-world.md

```

### Full Walk-Through

5-minute Wwlk-through here: https://github.com/sutt/agro-demo#agro-walk-through


## Commands

### Worktree / Agent Dispatch

- `exec <index> <taskfile> ...`: Run an agent in a new worktree. This command first cleans up any existing worktree for the given index, creates a fresh one, and then launches a detached agent process with the specified task file.
- `muster <command> <indices>`: Run a command in one or more specified worktrees. This is useful for running tests, starting servers, or executing any shell command across multiple environments.
- `surrender [indices]`: Kill running agent processes. If no indices are specified, it targets all running agents.

### Git Helpers

- `grab <branch-name>`: Checkout a branch. If the branch is already in use by another worktree, it creates a copy (e.g., `branch.copy`) and checks out the copy.
- `fade <pattern>`: Delete local branches that match a given regex pattern, after a confirmation prompt.

### Worktree Utility

- `make <index>`: Create a new worktree with a specified index. This sets up the directory, git branch, and environment.
- `delete <index>`: Delete the worktree and the associated git branch for a given index.


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

agro will port `.env` files into the worktrees and override particular settings for parallel execution environments. And clone the env  ironment (currently only supported for `uv`) from the main workspace into the 

```agro muster 'uv run which python' 1,2```

```bash

--- Running command in t1 (trees/t1) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t1/.venv/bin/python

--- Running command in t2 (trees/t2) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t2/.venv/bin/python

```
