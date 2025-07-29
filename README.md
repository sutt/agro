# Agro

A script to manage git worktrees for agent-based development. This tool simplifies creating, managing, and running processes within isolated worktrees, each with its own environment configuration.

[![PyPI version](https://img.shields.io/pypi/v/agro)](https://pypi.org/project/agro/)

- **View [Docs](./docs/index.md)**
- **View [Case Studies](./docs/case-studies/index.md)**
- **View [AI Dev Log](./docs/dev-summary-v1.md)**

---

**Agro is** *simple*, *powerful*, *flexible* and *open-source*.

- **Simple:** get started with a pip install and two commands. 
    - No signups, free trials or api keys needed. 
    - Works in your terminal with git, no new tools to learn.
- **Powerful:** compare the results of different coding agents.
    - Run agents in parallel with built in support for environment reproduction and unique env vars.
- **Flexible:** works with multiple different cli agents, models, and IDE / editors.
    - Works with all IDE's including: VSCode, Vim, Emacs, Cursor, and others.
- **Open-source:** avoid lock-in and subscriptions for your development environment.
    - Agro is command line and always opensource. You can modify at will and share with others.
    - Agro uses git under the hood so you can always substitue any or all parts of the recommended workflow with your own bash or git commands.
    

**There is no magic**, it's just shell calls to _git, claude, aider, ps, etc_. 
 - Since git's not going anywhere you'll always have support for your workflow, and
 - Wrapping coder-agents allows drop-in addition or replacement as they become available.

So you can take agro to your nineteen side-projects and four remote jobs, and it will work everywhere.

---

**Supported Agents:** _aider, claude code, gemini cli_
- Shared context files
- Customizable agent behavior

**Supported Models:** _Anthropic, OpenAI, Google, Grok4 and more_

---
**Agro-Builds-Agro:** If you think vibe-coding can't stand-up to multiple iterations, this is your chance to think again. Agro is 150 commits and going strong (roughly 80% ai generated). See the [Dev Log](./docs/dev-summary-v1.md) and [Case Studies](./docs/case-studies/index.md) to see a record of all the prompts and their accepted solutions.

---

## Quickstart

Install with `pip` or `uv tool`:

```bash
pip install agro
# or
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

---

### Agro at a glance - Hello, World!

**Also see the [case studies](./docs/case-studies/index.md) for more advanced guidance on using this tool**

**0A. Clone the Demo Repo**

```bash
git clone https://github.com/sutt/agro-demo
cd agro-demo

# setup environment and run server
uv sync
uv run python app/main.py
# hit ctrl+c to shutdown server, and let's start...
```

**0B. Copy the supplied docs**

Copy the public git-tracked `.public-agdocs` directory to an internal git-ignored repo `.agdocs`

```bash
cp -r .public-agdocs .agdocs
```

The `.agdocs` directory is the default lookup for where **agro** will attempt to access configurations, guidance, and 

This repo comes with tasks (.md files in /specs/ subdirectory). These should now be available if you copied it correctly in the step above.

```
.agdocs/
├── conf
│   └── agro.conf.yml
├── guides
│   └── GUIDE.md
├── specs
│   ├── add-about.md
│   ├── infer-model.md
│   └── query-web.md
└── swap
```


**1. Launch four agents in parallel**


```bash
$ agro exec add-about 2       # launch two agents of aider 
$ agro exec add-about claude  # if you have claude-code installed
$ agro exec add-about gemini  # if you have gemini installed
```
_Agro is configured to use aider by default. Add the name of the coding agent you have installed as the argument to use the one you have installed, see [docs for more info on this](./docs/configuration.md#default-agent)._

_For the purposes of this tutorial, you don't need to launch all three different type of agents, simple use one or two that you have installed. If you don't have any installed, find instructions of how to install [here](./docs/agents.md#agent-installation)._

These commands launched agents on a pre-written task in `.agdocs/specs/add-about.md`. _(Ultimately you will write your own but let's start with a simple pre-written one.)_

**add-about.md**
>add an about page and route
add a unique message of encouragment to the about page
add a test 
run the test to make sure it passes before exiting

**Basic Output**
- notice the git worktree / branch management + launch of aider, claude and gemini

```bash
♻️  Cleanup for index 1 complete.
🏃 Agent for index 1 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t1
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.1
   Agent type: aider
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:12:20
♻️  Cleanup for index 2 complete.
🏃 Agent for index 2 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t2
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.2
   Agent type: aider
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:12:20

♻️  Cleanup for index 3 complete.
🏃 Agent for index 3 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t3
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.3
   Agent type: claude
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:13:13

♻️  Cleanup for index 4 complete.
🏃 Agent for index 4 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t4
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.4
   Agent type: gemini
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:13:27
```

Now you should see multiple branches created, one for each agent:

```bash
$ git branch
* master
+ output/add-about.1
+ output/add-about.2
+ output/add-about.3
+ output/add-about.4
```

**2. Launch Server on each worktree**

```bash
agro muster -c server-start
```
- The argument `-c` / `--common-cmd` arg allows us to pass an alias for common commands we'll use. See [docs on common commands](./docs/configuration.md#muster-common-commands) for more info.

**Output**

```bash
agro muster -c server-start output

--- Running command in t1 (output/add-about.1) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t2 (output/add-about.2) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t3 (output/add-about.3) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t4 (output/add-about.4) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
```

**Check About Page Contents**
_You could do this in browser as well_

```bash
# check worktree t1 - aider agent (#1)
curl http://127.0.0.1:8001/about
# {"message":"Keep up the great work!"}

# check worktree t2 - aider agent (#2)
curl http://127.0.0.1:8002/about
# {"message":"You are doing great!"}

# check worktree t3 - claude agent
curl http://localhost:8003/about
# {"message":"🌱 Every great journey begins with a single step. You're already on your way to something amazing!","title":"About AgSwap","description":"Welcome to AgSwap - where agricultural innovation meets community collaboration."}

# check worktree t4 - gemini agent
curl http://localhost:8004/about
# {"message":"Keep up the great work, you're awesome!"}

```

Now clean up the server:

```bash
# run muster with server-kill (builtin common command) to take it down each worktree
$ agro muster -c server-kill

--- Running command in t1 (output/add-about.1) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t2 (output/add-about.2) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t3 (output/add-about.3) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t4 (output/add-about.4) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

# checking agent1's worktree env, we see the server is no longer responding
$ curl http://localhost:8001
curl: (7) Failed to connect to localhost port 8001 after 0 ms: Connection refused
```

**3. Checking tests**

We run our existing tests with:

```bash
$ uv run pytest -q
3 passed in 0.28s
```

So we see have 3 existing tests, now let's check the output of our agents:

```bash
$ agro muster -c testq output

--- Running command in t1 (output/add-about.1) ---
$ uv run pytest -q
4 passed in 0.25s

--- Running command in t2 (output/add-about.2) ---
$ uv run pytest -q
4 passed in 0.28s

--- Running command in t3 (output/add-about.3) ---
$ uv run pytest -q
4 passed in 0.25s

--- Running command in t4 (output/add-about.4) ---
$ uv run pytest -q
3 passed in 0.24s
```
Cool, so we see all Agents left the tests green, and Agents 1-3 added a new unit test (since they now have 4 tests and we started with 3 tests).

**Check the code changes from each agent**

TODO - add the agro diff command

TODO - add the branch-patterns example

### Or add your own spec to a project

For example:

**Create and commit a spec file and pass to an agent**
```bash
agro init # if you don't already have an `.agdocs` at root

# create a spec
agro task hello-world  
# then add the text to the spec: "add hello world to the readme of this project"
# equivalent to:
echo "add hello world to the readme of this project" > .agdocs/specs/hello-world.md

agro exec  
# when not supplying an argument for the task name, 
# agro will chose the most recently modified .md file in specs/, so 
# this is equivalent to:
agro exec hello-world 1 aider
```

### Full Walk-Through

TODO - add a full tutorial here


## Commands

TODO

### Help

```
usage: agro [-v / -vv] <subcommand> [subcommand-args]

A script to manage git branches & worktrees for agent-based development.

Main command:
  exec [args] [taskfile] [num-trees] [exec-cmd]   
                                
    Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees / agents to create.
          -c <exec-cmd>         Custom command to launch agent on worktree.
          -a <agent-type>       Specify agent type to override config.
                                Supported: aider, claude, gemini.

Other Commands:
  muster [opts] [command] [branch-patterns]    Run a command in specified worktrees.
  diff [branch-patterns] [diff-opts]   Show git diff for specified worktrees.
  surrender [branch-patterns]   Kill running agent processes (default: all).
  grab <branch-name>            Checkout a branch, creating a copy if it's in use.
  fade <branch-patterns>        Delete local branches matching a regex pattern.
  clean [opts] [branch-patterns]    Clean up worktrees and/or branches.
  state [branch-patterns]       Show the worktree to branch mappings (default: all).
  task [task-name]              Create a new task spec file and open it.
  init                          Initialize agro project structure in .agdocs/.
  mirror                        Mirror internal docs to public docs directory.
  make <index>                  Create a new worktree.
  delete <indices>|--all        Delete one, multiple, or all worktrees.

Branch-patterns examples (for regex like matching):
  output/add-thing              Match output/add-thing*
  output/add-thing.{2,5}        Match output/add-thing.2, output/add-thing.5
  output/add-thing.{1-4}        Match output/add-thing.1, ... output/add-thing.4

Common options for 'make' and 'exec':
  --fresh-env         Use .env.example as the base instead of .env.
  --no-env-overrides  Do not add port overrides to the .env file.

Options for 'muster':
  -c, --common-cmd <key> Run a pre-defined command from config.

Options for 'clean':
  --soft              Only delete worktrees, not branches.
  --hard              Delete both worktrees and branches (default).
    
Options for 'init':
  --conf              Only add a template agro.conf.yml to .agdocs/conf


```

## Layout

The script will create two directories in the code repo:
- `.agdocs/` - specs, configs, logs for agro (when `agro init` run)
- `trees/` - root for worktrees (when `agro exec` run)
- both of these are added to gitignore by default

```
- .agdocs/
    - specs/
        - task1
        - task2
        ...
    - swap/  <- gitignored
        - shared logs 
    - conf/
      - agro.conf.yml
    - guides/
      - GUIDE.md
      - other-guide.md
      - ...
- <your-code>
- <your-configs>
- trees/
    - t1/
        - <your-code>
        - <t1-configs>
    - t2/
        - <your-code>
        - <t1-configs>
    ...
```

#### Worktree Configuration

agro will port `.env` files into the worktrees and override particular settings for parallel execution environments. And clone the env  ironment (currently only supported for `uv`) from the main workspace into the 

```agro muster 'uv run which python' output/add-about.{1,2}```

```bash

--- Running command in t1 (trees/t1) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t1/.venv/bin/python

--- Running command in t2 (trees/t2) ---
$ uv run which python
/home/user/tools_dev/agscript/trees/t2/.venv/bin/python

```

Or

```agro muster 'cat .env' output/add-about.{1,2}```

```bash

--- Running command in t1 (output/add-about.1) ---
$ cat .env
API_PORT=8000
### Worktree Overrides ---
API_PORT=8001

--- Running command in t2 (output/add-about.2) ---
$ cat .env
API_PORT=8000
### Worktree Overrides ---
API_PORT=8002

```

### What it does

Three functionalities needed for the ai-generated workflow:
- **Wrapper around CLI-Agents**
    - Agents operate in non-interactive mode (both YOLO and safe modes available)
- **Markdown file based tasks**
    - You can track these with git and publish to github or keep them internal
        - see this example [Dev Log](./docs/dev-summary-v1.md) for agro.
- **A git branch + worktree workflow for reviewing generated code:**
    - Don't dread the process of reviewing reams of ai generated code, embrace it with some 

**What it doesn't do:** agro is not an agent itself. Agro is a micro-framework to call other agents and simiplify workflow for dipatching, review, and comparison between different agents and models.

---

#### Currently Supporting / Tested With

- python
    - uv + virtualenv
- node
  - npm


### Docs

Check out the full docs here: [Agro Docs](./docs/index.md)

### Tutorials

### Philosophy

### Future Development
