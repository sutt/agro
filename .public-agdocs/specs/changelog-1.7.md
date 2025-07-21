Below is a diff from v0.1.6 to v0.1.7.

Add entries to docs/CHANGELOG.md to describe the changes

One thing to note is there was many changes to docs/ which we've stat diffed here but there's no need to give a detailed report of doc updates except mention them at a highlevel. Same thing with readme updates.

$git diff --stat v0.1.6 HEAD -- docs/ 
 docs/agents.md                                     |  147 +++
 docs/case-studies/aba-1.md                         |   44 +-
 docs/case-studies/aba-2.md                         |  104 +-
 docs/case-studies/aba-3.md                         |  107 ++
 docs/case-studies/aba-4.md                         |   56 ++
 docs/case-studies/aba-5.md                         |  201 ++++
 docs/case-studies/aba-6.md                         |  227 +++++
 docs/case-studies/assets/aba5-aider-tbl.md         |   17 +
 docs/case-studies/assets/aba5-aider.chat.md        |  159 +++
 docs/case-studies/assets/claude-summary-diff-1.log |  458 +++++++++
 docs/case-studies/assets/tbl-1.png                 |  Bin 0 -> 78964 bytes
 docs/case-studies/index.md                         |   18 +
 docs/commands.md                                   |  507 ++++++++++
 docs/configuration.md                              |  115 +++
 docs/contributing.md                               |  536 ++++++++++
 docs/core-concepts.md                              |  346 +++++++
 docs/dev-summary-v1.md                             |   90 ++
 docs/examples.md                                   | 1022 ++++++++++++++++++++
 docs/getting-started.md                            |  238 +++++
 docs/index.md                                      |   98 ++
 docs/troubleshooting.md                            |  710 ++++++++++++++
 docs/workflows.md                                  |  497 ++++++++++
 22 files changed, 5651 insertions(+), 46 deletions(-)


Here's the diff to the source and other dev repo files:

git diff v0.1.6 HEAD -- . ':(exclude)docs/'


diff --git a/.public-agdocs/conf/agro.conf.yml b/.public-agdocs/conf/agro.conf.yml
index 09e5eb2..ed2f8ca 100644
--- a/.public-agdocs/conf/agro.conf.yml
+++ b/.public-agdocs/conf/agro.conf.yml
@@ -65,3 +65,12 @@ EXEC_CMD_DEFAULT: maider.sh
 
 # Default command to open spec files with 'agro task'.
 # AGRO_EDITOR_CMD: code
+
+
+# --- Muster ---
+
+# Pre-defined commands for 'agro muster -c'.
+# MUSTER_COMMON_CMDS:
+#   testq: 'uv run pytest --tb=no -q'
+#   server-start: 'uv run python -m http.server > server.log 2>&1 & echo $! > server.pid'
+#   server-kill: 'kill $(cat server.pid) && rm -f server.pid server.log'
diff --git a/README.md b/README.md
index e87ebd8..ec04c53 100644
--- a/README.md
+++ b/README.md
@@ -4,6 +4,44 @@ A script to manage git worktrees for agent-based development. This tool simplifi
 
 [![PyPI version](https://img.shields.io/pypi/v/agro)](https://pypi.org/project/agro/)
 
+- **View [Docs](./docs)**
+- **View [Case Studies](./docs/case-studies/)**
+- **View [AI Dev Log](./docs/dev-summary-v1.md)**
+
+---
+
+**Agro is** *simple*, *powerful*, *flexible* and *open-source*.
+
+- **Simple:** get started with a pip install and two commands. 
+    - No signups, free trials or api keys needed. 
+    - Works in your terminal with git, no new tools to learn.
+- **Powerful:** compare the results of different coding agents.
+    - Run agents in parallel with built in support for environment reproduction and unique env vars.
+- **Flexible:** works with multiple different cli agents, models, and IDE / editors.
+    - Works with all IDE's including: VSCode, Vim, Emacs, Cursor, and others.
+- **Open-source:** avoid lock-in and subscriptions for your development environment.
+    - Agro is command line and always opensource. You can modify at will and share with others.
+    - Agro uses git under the hood so you can always substitue any or all parts of the recommended workflow with your own bash or git commands.
+    
+
+**There is no magic**, it's just shell calls to _git, claude, aider, ps, etc_. 
+ - Since git's not going anywhere you'll always have support for your workflow, and
+ - Wrapping coder-agents allows drop-in addition or replacement as they become available.
+
+So you can take agro to your nineteen side-projects and four remote jobs, and it will work everywhere.
+
+---
+
+**Supported Agents:** _aider, claude code, gemini cli_
+- Shared context files
+- Customizable agent behavior
+
+**Supported Models:** _Anthropic, OpenAI, Google, Grok4 and more_
+
+---
+**Agro-Builds-Agro:** If you think vibe-coding can't stand-up to multiple iterations, this is your chance to think again. Agro is 150 commits and going strong (roughly 80% ai generated). See the [Dev Log](./docs/dev-summary-v1.md) and [Case Studies](./docs/case-studies) to see a record of all the prompts and their accepted solutions.
+
+---
 
 ## Quickstart
 
@@ -11,6 +49,7 @@ Install with `pip` or `uv tool`:
 
 ```bash
 pip install agro
+# or
 uv tool install agro
 ```
 
@@ -25,13 +64,14 @@ uv tool install . --no-cache
 
 For local dev updates run the `./redeploy` script to reinstall the local repo as `agro`.
 
+---
+
 ### At a Glance - Hello, World!
 
-**Warning: this workflow is deprecated as of v0.1.4, see this [case study](./docs/case-studies/aba-1.md) for a better tutorial for for working with v0.1.4**
+**Also see the [case studies](./docs/case-studies/aba-1.md) for more advanced guidance on using this tool**
 
 **0. Clone the Demo Repo**
 
-
 ```bash
 git clone git@github.com:sutt/agro-demo.git
 cd agro-demo
@@ -39,244 +79,285 @@ cd agro-demo
 uv sync
 ```
 
-Use the pre-built app + built in task in `.agdocs/specs`.
+**1. Launch four agents in parallel**
 
-**1. Launch two agents in parallel**
-- target worktrees 1 and 2.
+_Agro is configured to use aider by default. Add the name of the coding agent you have installed as the argument to use the one you have installed._
 
 ```bash
-$ agro exec 1 .agdocs/specs/add-about.md 
-$ agro exec 2 .agdocs/specs/add-about.md 
+$ agro exec add-about 2       # launch two agents of aider 
+$ agro exec add-about claude  # if you have claude-code installed
+$ agro exec add-about gemini  # if you have gemini installed
 ```
+This repo comes with tasks in `.agdocs/specs` including the spec
+
+**add-about.md**
+>add an about page and route
+add a unique message of encouragment to the about page
+add a test 
+run the test to make sure it passes before exiting
 
 **Basic Output**
-- notice the git worktree / branch management + launch of aider
+- notice the git worktree / branch management + launch of aider, claude and gemini
 
 ```bash
 ♻️  Cleanup for index 1 complete.
-🌴 New worktree created successfully.
-   Worktree: trees/t1
-   API Port: 8001
-🌱 Working on new branch: output/add-about.1
 🏃 Agent for index 1 started successfully.
-   Worktree: /home/user/tools_dev/demo_fastapi/trees/t1
-   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
-
-   ...
-
+   Worktree: /home/user/dev/agro/agro-demo/trees/t1
+   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
+   Branch: output/add-about.1
+   Agent type: aider
+   Initial commit SHA: 31ad99
+   Start time: 2025-07-18 09:12:20
 ♻️  Cleanup for index 2 complete.
-🌴 New worktree created successfully.
-   Worktree: trees/t2
-   API Port: 8002
-🌱 Working on new branch: output/add-about.2
 🏃 Agent for index 2 started successfully.
-   Worktree: /home/user/tools_dev/demo_fastapi/trees/t2
-   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
+   Worktree: /home/user/dev/agro/agro-demo/trees/t2
+   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
+   Branch: output/add-about.2
+   Agent type: aider
+   Initial commit SHA: 31ad99
+   Start time: 2025-07-18 09:12:20
+
+♻️  Cleanup for index 3 complete.
+🏃 Agent for index 3 started successfully.
+   Worktree: /home/user/dev/agro/agro-demo/trees/t3
+   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
+   Branch: output/add-about.3
+   Agent type: claude
+   Initial commit SHA: 31ad99
+   Start time: 2025-07-18 09:13:13
+
+♻️  Cleanup for index 4 complete.
+🏃 Agent for index 4 started successfully.
+   Worktree: /home/user/dev/agro/agro-demo/trees/t4
+   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
+   Branch: output/add-about.4
+   Agent type: gemini
+   Initial commit SHA: 31ad99
+   Start time: 2025-07-18 09:13:27
+```
 
+Now you should see multiple branches created, one for each agent:
 
+```bash
+$ git branch
+* master
++ output/add-about.1
++ output/add-about.2
++ output/add-about.3
++ output/add-about.4
 ```
 
-##### full output
-<details>
-    <summary>
-    expand full output
-    </summary>
+**2. Launch Server on each worktree**
 
 ```bash
-♻️  Cleanup for index 1 complete.
+agro muster --server 'uv run python app/main.py' output
+```
+- The argument `--server` allows detach mode to run multiple servers out of one shell.
 
-Creating new worktree for index 1...
-Creating new worktree 't1' at 'trees/t1' on branch 'tree/t1'...
-Preparing worktree (new branch 'tree/t1')
-HEAD is now at f0b97b1 refactor: .agdocs structure
-Copying .env to trees/t1/.env
-Warning: Source env file '.env' not found. Creating an empty .env file.
-Adding worktree overrides to trees/t1/.env
-Setting up Python environment in trees/t1...
+**Output**
 
-🌴 New worktree created successfully.
-   Worktree: trees/t1
-   Branch: tree/t1
-   API Port: 8001
-   DB Port:  5433
+```bash
+agro muster --server 'uv run python app/main.py' output
 
-🌱 Working on new branch: output/add-about.1
+--- Running command in t1 (output/add-about.1) ---
+$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
 
-Launching agent in detached mode from within trees/t1...
+--- Running command in t2 (output/add-about.2) ---
+$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
 
-🏃 Agent for index 1 started successfully.
-   Worktree: /home/user/tools_dev/demo_fastapi/trees/t1
-   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
-   Branch: output/add-about.1
-   Start time: 2025-07-03 17:13:58
-   PID: 579494 (saved to /home/user/tools_dev/demo_fastapi/.agdocs/swap/t1.pid)
-   Log file: /home/user/tools_dev/demo_fastapi/trees/t1/maider.log
-```
-**2. Launch a second agent on same task**
+--- Running command in t3 (output/add-about.3) ---
+$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
 
-**Run command:**
-```bash
-$ agro exec 2 .agdocs/specs/add-about.md 
+--- Running command in t4 (output/add-about.4) ---
+$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
 ```
 
-- notice how work tree is incremented
-- notice how API_PORT is incremented
+**Check About Page Contents**
+_You could do this in browser as well_
 
 ```bash
-♻️  Cleanup for index 2 complete.
+# check worktree t1 - aider agent (#1)
+curl http://127.0.0.1:8001/about
+# {"message":"Keep up the great work!"}
 
-🌴 New worktree created successfully.
-   Worktree: trees/t2
-   Branch: tree/t2
-   API Port: 8002
+# check worktree t2 - aider agent (#2)
+curl http://127.0.0.1:8002/about
+# {"message":"You are doing great!"}
 
-🌱 Working on new branch: output/add-about.2
+# check worktree t3 - claude agent
+curl http://localhost:8003/about
+# {"message":"🌱 Every great journey begins with a single step. You're already on your way to something amazing!","title":"About AgSwap","description":"Welcome to AgSwap - where agricultural innovation meets community collaboration."}
 
-Launching agent in detached mode from within trees/t2...
-
-🏃 Agent for index 2 started successfully.
-   Worktree: /home/user/tools_dev/demo_fastapi/trees/t2
-   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
-   Branch: output/add-about.2
+# check worktree t4 - gemini agent
+curl http://localhost:8004/about
+# {"message":"Keep up the great work, you're awesome!"}
 
 ```
-</details>
 
-**2. Launch Server on each worktree**
+Now clean up the server:
 
 ```bash
-agro muster 'python app/main.py' 1,2 --server
+# run muster with --kill-server to take it down each worktree
+$ agro muster --kill-server '' output
+
+--- Running command in t1 (output/add-about.1) ---
+$ kill $(cat server.pid) && rm -f server.pid server.log
+
+--- Running command in t2 (output/add-about.2) ---
+$ kill $(cat server.pid) && rm -f server.pid server.log
+
+--- Running command in t3 (output/add-about.3) ---
+$ kill $(cat server.pid) && rm -f server.pid server.log
+
+--- Running command in t4 (output/add-about.4) ---
+$ kill $(cat server.pid) && rm -f server.pid server.log
+
+# checking agent1's worktree env, we see the server is no longer responding
+$ curl http://localhost:8001
+curl: (7) Failed to connect to localhost port 8001 after 0 ms: Connection refused
 ```
-- The argument `--server` allows detach mode to run multiple servers out of one shell.
 
-**Output**
+**3. Checking tests**
 
-```bash
---- Running command in t1 (trees/t1) ---
-$ python app/main.py > server.log 2>&1 & echo $! > server.pid
+We run our existing tests with:
 
---- Running command in t2 (trees/t2) ---
-$ python app/main.py > server.log 2>&1 & echo $! > server.pid
+```bash
+$ uv run pytest -q
+3 passed in 0.28s
 ```
 
-**Check About Page Contents**
-_You could do this in browser as well_
+So we see have 3 existing tests, now let's check the output of our agents:
 
 ```bash
-# check worktree app, here the /about route hasn't been created
-curl http://127.0.0.1:8000/about
-# {"detail":"Not Found"}
+$ agro muster 'uv run pytest -q' output
 
-# check worktree t1
-curl http://127.0.0.1:8001/about
-{"message":"Keep up the great work!"}
+--- Running command in t1 (output/add-about.1) ---
+$ uv run pytest -q
+4 passed in 0.25s
 
-# check worktree t2
-curl http://127.0.0.1:8002/about
-{"message":"This is an about page. Keep up the great work!"}
+--- Running command in t2 (output/add-about.2) ---
+$ uv run pytest -q
+4 passed in 0.28s
 
-```
+--- Running command in t3 (output/add-about.3) ---
+$ uv run pytest -q
+4 passed in 0.25s
 
+--- Running command in t4 (output/add-about.4) ---
+$ uv run pytest -q
+3 passed in 0.24s
+```
 ### Or add your own spec to a project
 
 For example:
 
 **Create and commit a spec file and pass to an agent**
 ```bash
-mkdir .agdocs
-touch .agdocs/hello-world.md
-echo "add hello world to the readme of this project" > .agdocs/hello-world.md
-
-git add .agdocs
-git commit -m "spec: hello-world"
+agro init # add .agdocs/ to repo
 
-agro exec 1 .agdocs/hello-world.md
+# create a spec
+agro task hello-world  
+# then add the text to the spec: "add hello world to the readme of this project"
+# equivalent to:
+echo "add hello world to the readme of this project" > .agdocs/specs/hello-world.md
 
+agro exec
+# equivalent to:
+agro exec add-about 1 aider
 ```
 
 ### Full Walk-Through
 
-5-minute Wwlk-through here: https://github.com/sutt/agro-demo#agro-walk-through
+TODO - add a full tutorial here
 
 
 ## Commands
 
-### Worktree / Agent Dispatch
-
-- `exec <index> <taskfile> ...`: Run an agent in a new worktree. This command first cleans up any existing worktree for the given index, creates a fresh one, and then launches a detached agent process with the specified task file.
-- `muster <command> <indices>`: Run a command in one or more specified worktrees. This is useful for running tests, starting servers, or executing any shell command across multiple environments.
-- `surrender [indices]`: Kill running agent processes. If no indices are specified, it targets all running agents.
-
-### Git Helpers
-
-- `grab <branch-name>`: Checkout a branch. If the branch is already in use by another worktree, it creates a copy (e.g., `branch.copy`) and checks out the copy.
-- `fade <pattern>`: Delete local branches that match a given regex pattern, after a confirmation prompt.
-
-### Worktree Utility
-
-- `make <index>`: Create a new worktree with a specified index. This sets up the directory, git branch, and environment.
-- `delete <index>`: Delete the worktree and the associated git branch for a given index.
-
+TODO
 
 ### Full Help
 
-```bash
+```
 
-usage: agro [-h]
+usage: agro [-h] [--version] [-v] [-q]
 
-A script to manage git worktrees for agent-based development.
+A script to manage git branches & worktrees for agent-based development.
 
 options:
-  -h, --help  show this help message and exit
-
-Available commands:
-  make <index>                  Create a new worktree.
-  delete <index>                Delete the worktree with the given index.
-  exec <index> <taskfile> ...   Run an agent in a new worktree.
-  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
+  -h, --help     show this help message and exit
+  --version      Show program's version number and exit.
+  -v, --verbose  Increase verbosity. -v for debug, -vv for command output.
+  -q, --quiet    Suppress all output except warnings and errors.
+
+Main command:
+  exec [args] [taskfile] [num-trees] [exec-cmd]   
+                                
+    Run an agent in new worktree(s)
+        args:
+          -n <num-trees>        Number of worktrees to create.
+          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree.
+          -a <agent-type>       Specify agent type to override config.
+                                Supported: aider, claude, gemini.
+
+Other Commands:
+  muster <command> <branch-patterns>    Run a command in specified worktrees.
+  surrender [branch-patterns]   Kill running agent processes (default: all).
   grab <branch-name>            Checkout a branch, creating a copy if it's in use.
-  fade <pattern>                Delete local branches matching a regex pattern.
-  surrender [indices]           Kill running agent processes (default: all).
-  help                          Show this help message.
+  fade <branch-patterns>        Delete local branches matching a regex pattern.
+  state [branch-patterns]       Show the worktree to branch mappings (default: all).
+  task [task-name]              Create a new task spec file and open it.
+  init                          Initialize agro project structure in .agdocs/.
+  mirror                        Mirror internal docs to public docs directory.
+  make <index>                  Create a new worktree.
+  delete <indices>|--all        Delete one, multiple, or all worktrees.
+
+Branch-patterns examples (for regex like matching):
+  output/add-thing              Match output/add-thing*
+  output/add-thing.{2,5}        Match output/add-thing.2, output/add-thing.5
+  output/add-thing.{1-4}        Match output/add-thing.1, ... output/add-thing.4
 
 Common options for 'make' and 'exec':
-  --fresh-env         When creating a worktree, use .env.example as the base instead of .env.
-  --no-env-overrides  When creating a worktree, do not add port overrides to the .env file.
-  --no-all-extras     Do not install all extra dependencies when running 'uv sync'.
+  --fresh-env         Use .env.example as the base instead of .env.
+  --no-env-overrides  Do not add port overrides to the .env file.
 
 Options for 'muster':
-  -s, --server        Run command as a background server, redirecting output and saving PID.
+  -s, --server        Run command as a background server (and log server PID)
   -k, --kill-server   Kill the background server and clean up pid/log files.
-
-```
-
+    
+Options for 'init':
+  --conf              Only add a template agro.conf.yml to .agdocs/conf
 
 
+```
 
 ## Layout
 
-The script creates two directories in the code repo:
-- `.agdocs/` - specs, configs, logs for agro
-- `trees/` - root for worktrees (gitignored)
+The script will create two directories in the code repo:
+- `.agdocs/` - specs, configs, logs for agro (when `agro init` run)
+- `trees/` - root for worktrees (when `agro exec` run)
+- both of these are added to gitignore by default
 
 ```
-- .agdocs
+- .agdocs/
     - specs/
         - task1
         - task2
         ...
-    - swap
+    - swap/  <- gitignored
         - shared logs 
-        - (gitignored)
+    - conf/
+      - agro.conf.yml
+    - guides/
+      - GUIDE.md
+      - other-guide.md
+      - ...
 - <your-code>
-    ...
 - <your-configs>
-    ...
 - trees/
-    - t1
+    - t1/
         - <your-code>
         - <t1-configs>
-    - t2
+    - t2/
         - <your-code>
         - <t1-configs>
     ...
@@ -286,7 +367,7 @@ The script creates two directories in the code repo:
 
 agro will port `.env` files into the worktrees and override particular settings for parallel execution environments. And clone the env  ironment (currently only supported for `uv`) from the main workspace into the 
 
-```agro muster 'uv run which python' 1,2```
+```agro muster 'uv run which python' output/add-about.{1,2}```
 
 ```bash
 
@@ -299,3 +380,56 @@ $ uv run which python
 /home/user/tools_dev/agscript/trees/t2/.venv/bin/python
 
 ```
+
+Or
+
+```agro muster 'cat .env' output/add-about.{1,2}```
+
+```bash
+
+--- Running command in t1 (output/add-about.1) ---
+$ cat .env
+API_PORT=8000
+### Worktree Overrides ---
+API_PORT=8001
+
+--- Running command in t2 (output/add-about.2) ---
+$ cat .env
+API_PORT=8000
+### Worktree Overrides ---
+API_PORT=8002
+
+```
+
+### What it does
+
+Three functionalities needed for the ai-generated workflow:
+- **Wrapper around CLI-Agents**
+    - Agents operate in non-interactive mode (both YOLO and safe modes available)
+- **Markdown file based tasks**
+    - You can track these with git and publish to github or keep them internal
+        - see this example [Dev Log](./docs/dev-summary-v1.md) for agro.
+- **A git branch + worktree workflow for reviewing generated code:**
+    - Don't dread the process of reviewing reams of ai generated code, embrace it with some 
+
+**What it doesn't do:** agro is not an agent itself. Agro is a micro-framework to call other agents and simiplify workflow for dipatching, review, and comparison between different agents and models.
+
+---
+
+#### Currently Supporting / Tested With
+
+- python
+    - uv + virtualenv
+- node
+  - npm
+
+
+### Docs
+
+Check out the full docs here: [Agro Docs](./docs/index.md)
+
+### Tutorials
+
+### Philosophy
+
+### Future Development
diff --git a/src/agro/cli.py b/src/agro/cli.py
index fd19fc6..afd0a95 100644
--- a/src/agro/cli.py
+++ b/src/agro/cli.py
@@ -106,6 +106,30 @@ def _dispatch_exec(args):
     )
 
 
+def _dispatch_muster(args):
+    """Helper to dispatch muster command with complex argument parsing."""
+    command_str = args.command_str
+    branch_patterns = args.branch_patterns
+    common_cmd_key = args.common_cmd_key
+
+    if common_cmd_key:
+        if command_str:
+            # Positional command_str is treated as a branch pattern when -c is used
+            branch_patterns.insert(0, command_str)
+        command_str = None  # Command will be looked up from config
+    elif not command_str:
+        raise ValueError(
+            "Muster command requires a command string or -c/--common-cmd option."
+        )
+
+    core.muster_command(
+        command_str=command_str,
+        branch_patterns=branch_patterns,
+        common_cmd_key=common_cmd_key,
+        show_cmd_output=(args.verbose >= 2),
+    )
+
+
 def main():
     """
     Main entry point for the agro command-line interface.
@@ -121,10 +145,12 @@ def main():
                                 Supported: aider, claude, gemini.
 
 Other Commands:
-  muster <command> <branch-patterns>    Run a command in specified worktrees.
+  muster [opts] [command] [branch-patterns]    Run a command in specified worktrees.
+  diff [branch-patterns]        Show git diff for specified worktrees.
   surrender [branch-patterns]   Kill running agent processes (default: all).
   grab <branch-name>            Checkout a branch, creating a copy if it's in use.
   fade <branch-patterns>        Delete local branches matching a regex pattern.
+  clean [opts] [branch-patterns]    Clean up worktrees and/or branches.
   state [branch-patterns]       Show the worktree to branch mappings (default: all).
   task [task-name]              Create a new task spec file and open it.
   init                          Initialize agro project structure in .agdocs/.
@@ -142,8 +168,14 @@ Common options for 'make' and 'exec':
   --no-env-overrides  Do not add port overrides to the .env file.
 
 Options for 'muster':
-  -s, --server        Run command as a background server (and log server PID)
-  -k, --kill-server   Kill the background server and clean up pid/log files.
+  -c, --common-cmd <key> Run a pre-defined command from config.
+
+Options for 'diff':
+  --stat              Show diffstat instead of full diff.
+
+Options for 'clean':
+  --soft              Only delete worktrees, not branches.
+  --hard              Delete both worktrees and branches (default).
     
 Options for 'init':
   --conf              Only add a template agro.conf.yml to .agdocs/conf"""
@@ -292,33 +324,45 @@ Options for 'init':
     parser_muster = subparsers.add_parser(
         "muster", help="Run a command in specified worktrees."
     )
+    parser_muster.add_argument(
+        "-c",
+        "--common-cmd",
+        dest="common_cmd_key",
+        help="Run a pre-defined command from config.",
+    )
     parser_muster.add_argument(
         "command_str",
-        help="The command to execute. A dummy value can be used with --kill-server.",
+        nargs="?",
+        default=None,
+        help="The command to execute. Optional if -c is used.",
     )
     parser_muster.add_argument(
         "branch_patterns",
-        nargs="+",
-        help="One or more branch patterns to select worktrees.",
+        nargs="*",
+        default=[],
+        help="One or more branch patterns. Defaults to output branches.",
     )
-    parser_muster.add_argument(
-        "-s",
-        "--server",
-        action="store_true",
-        help="Run command as a background server, redirecting output and saving PID.",
+    parser_muster.set_defaults(func=_dispatch_muster)
+
+    # --- diff command ---
+    parser_diff = subparsers.add_parser(
+        "diff", help="Show git diff for specified worktrees."
     )
-    parser_muster.add_argument(
-        "-k",
-        "--kill-server",
+    parser_diff.add_argument(
+        "branch_patterns",
+        nargs="*",
+        default=[],
+        help="Optional branch pattern(s) to select worktrees. Defaults to all.",
+    )
+    parser_diff.add_argument(
+        "--stat",
         action="store_true",
-        help="Kill the background server and clean up pid/log files.",
+        help="Show diffstat instead of full diff.",
     )
-    parser_muster.set_defaults(
-        func=lambda args: core.muster_command(
-            args.command_str,
+    parser_diff.set_defaults(
+        func=lambda args: core.diff_worktrees(
             args.branch_patterns,
-            server=args.server,
-            kill_server=args.kill_server,
+            stat=args.stat,
             show_cmd_output=(args.verbose >= 2),
         )
     )
@@ -347,6 +391,36 @@ Options for 'init':
         )
     )
 
+    # --- clean command ---
+    parser_clean = subparsers.add_parser(
+        "clean",
+        help="Delete worktrees and/or associated branches matching pattern(s).",
+    )
+    parser_clean.add_argument(
+        "branch_patterns",
+        nargs="*",
+        default=[],
+        help="Optional branch pattern(s) to select what to clean. Defaults to all output branches.",
+    )
+    clean_group = parser_clean.add_mutually_exclusive_group()
+    clean_group.add_argument(
+        "--soft",
+        action="store_true",
+        help="Only delete worktrees, not the branches.",
+    )
+    clean_group.add_argument(
+        "--hard",
+        action="store_true",
+        help="Delete both worktrees and branches (default).",
+    )
+    parser_clean.set_defaults(
+        func=lambda args: core.clean_worktrees(
+            branch_patterns=args.branch_patterns,
+            mode="soft" if args.soft else "hard",
+            show_cmd_output=(args.verbose >= 2),
+        )
+    )
+
     # --- surrender command ---
     parser_surrender = subparsers.add_parser(
         "surrender", help="Kill running agent processes."
diff --git a/src/agro/config.py b/src/agro/config.py
index bdb6f49..470953d 100644
--- a/src/agro/config.py
+++ b/src/agro/config.py
@@ -45,6 +45,11 @@ DEFAULTS = {
         'claude': 600,
         'gemini': 600,  # 10 minutes timeout for gemini calls
     },
+    'MUSTER_COMMON_CMDS': {
+        'testq': 'uv run pytest --tb=no -q',
+        'server-start': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
+        'server-kill': 'kill $(cat server.pid) && rm -f server.pid server.log',
+    },
     'AGRO_EDITOR_CMD': 'code',
     'ENV_SETUP_CMDS': [
         'uv venv',
@@ -76,6 +81,9 @@ def _load_config():
                             else:
                                 config['AGENT_CONFIG'][agent_name] = agent_data
 
+                    if 'MUSTER_COMMON_CMDS' in user_config and isinstance(user_config['MUSTER_COMMON_CMDS'], dict):
+                        config['MUSTER_COMMON_CMDS'].update(user_config.pop('MUSTER_COMMON_CMDS'))
+
                     config.update(user_config)
             except yaml.YAMLError as e:
                 print(f"Warning: Could not parse config file {config_path}. Using default values. Error: {e}", file=sys.stderr)
@@ -103,6 +111,7 @@ EXEC_CMD_DEFAULT = _config['EXEC_CMD_DEFAULT']
 AGENT_TYPE = _config['AGENT_TYPE']
 AGENT_CONFIG = _config['AGENT_CONFIG']
 AGENT_TIMEOUTS = _config['AGENT_TIMEOUTS']
+MUSTER_COMMON_CMDS = _config['MUSTER_COMMON_CMDS']
 AGRO_EDITOR_CMD = _config['AGRO_EDITOR_CMD']
 ENV_SETUP_CMDS = _config['ENV_SETUP_CMDS']
 
diff --git a/src/agro/core.py b/src/agro/core.py
index 85f1eba..343d2b7 100644
--- a/src/agro/core.py
+++ b/src/agro/core.py
@@ -139,6 +139,33 @@ def _get_matching_branches(pattern: str, show_cmd_output=False) -> list[str]:
 
 def _get_config_template():
     """Returns the content for the default agro.conf.yml."""
+
+    # Format ENV_SETUP_CMDS
+    env_setup_cmds_lines = ["# ENV_SETUP_CMDS:"]
+    for cmd in config.DEFAULTS.get("ENV_SETUP_CMDS", []):
+        env_setup_cmds_lines.append(f"#   - {json.dumps(cmd)}")
+    env_setup_cmds_str = "\n".join(env_setup_cmds_lines)
+
+    # Format AGENT_CONFIG
+    agent_config_lines = ["# AGENT_CONFIG:"]
+    for agent, settings in config.DEFAULTS.get("AGENT_CONFIG", {}).items():
+        agent_config_lines.append(f"#   {agent}:")
+        for key, value in settings.items():
+            agent_config_lines.append(f"#     {key}: {json.dumps(value)}")
+    agent_config_str = "\n".join(agent_config_lines)
+
+    # Format AGENT_TIMEOUTS
+    agent_timeouts_lines = ["# AGENT_TIMEOUTS:"]
+    for agent, timeout in config.DEFAULTS.get("AGENT_TIMEOUTS", {}).items():
+        agent_timeouts_lines.append(f"#   {agent}: {timeout}")
+    agent_timeouts_str = "\n".join(agent_timeouts_lines)
+
+    # Format MUSTER_COMMON_CMDS
+    muster_common_cmds_lines = ["# MUSTER_COMMON_CMDS:"]
+    for key, cmd in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
+        muster_common_cmds_lines.append(f"#   {key}: {json.dumps(cmd)}")
+    muster_common_cmds_str = "\n".join(muster_common_cmds_lines)
+
     return f"""# Agro Configuration File
 #
 # This file allows you to customize the behavior of Agro.
@@ -174,9 +201,7 @@ def _get_config_template():
 
 # Commands to set up the Python environment in a new worktree.
 # For example, to install all optional dependency groups with uv:
-# ENV_SETUP_CMDS:
-#   - 'uv venv'
-#   - 'uv sync --quiet --all-extras'
+{env_setup_cmds_str}
 
 
 # --- Agent Execution ---
@@ -189,23 +214,20 @@ def _get_config_template():
 # AGENT_TYPE: {config.DEFAULTS['AGENT_TYPE']}
 
 # Agent-specific configuration.
-# AGENT_CONFIG:
-#   aider:
-#     args: ["--yes", "--no-check-update", "--no-attribute-author", "--no-attribute-committer", "--no-attribute-co-authored-by"]
-#   claude:
-#     args: ["-d", "--allowedTools", "Write Edit MultiEdit", "--max-turns", "30", "-p"]
-#   gemini:
-#     args: ["-y"]
+{agent_config_str}
 
 # Agent-specific timeout settings in seconds.
 # A value of 0 means no timeout is applied, overriding any default.
-# AGENT_TIMEOUTS:
-#   aider: 0
-#   claude: 600
-#   gemini: 600
+{agent_timeouts_str}
 
 # Default command to open spec files with 'agro task'.
 # AGRO_EDITOR_CMD: {config.DEFAULTS['AGRO_EDITOR_CMD']}
+
+
+# --- Muster ---
+
+# Pre-defined commands for 'agro muster -c'.
+{muster_common_cmds_str}
 """
 
 
@@ -893,31 +915,95 @@ def _get_indices_from_branch_patterns(branch_patterns=None, show_cmd_output=Fals
     return sorted(matching_indices)
 
 
+def diff_worktrees(branch_patterns, stat=False, show_cmd_output=False):
+    """Runs 'git diff' in multiple worktrees."""
+    indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
+    if not indices:
+        logger.warning("No worktrees found matching the provided patterns.")
+        return
+
+    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
+
+    for index in indices:
+        tree_name = f"t{index}"
+        worktree_path = Path(config.WORKTREE_DIR) / tree_name
+        branch_name = worktree_state.get(tree_name, "<unknown branch>")
+
+        if not worktree_path.is_dir():
+            logger.warning(
+                f"Worktree t{index} at '{worktree_path}' not found. Skipping."
+            )
+            continue
+
+        logger.info(f"\n--- Diff for t{index} ({branch_name}) ---")
+
+        original_branch = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
+        command = ["git", "diff"]
+        if stat:
+            command.append("--stat")
+        command.extend([original_branch, "HEAD"])
+
+        cmd_str = shlex.join(command)
+        logger.info(f"$ {cmd_str}")
+
+        try:
+            _run_command(
+                command,
+                cwd=str(worktree_path),
+                show_cmd_output=True,
+            )
+        except (subprocess.CalledProcessError, FileNotFoundError):
+            # _run_command already prints details.
+            logger.error(f"--- Command failed in t{index}. Continuing... ---")
+            continue
+
+
 def muster_command(
-    command_str, branch_patterns, server=False, kill_server=False, show_cmd_output=False
+    command_str,
+    branch_patterns,
+    show_cmd_output=False,
+    common_cmd_key=None,
 ):
     """Runs a command in multiple worktrees."""
-    if server and kill_server:
-        raise ValueError("--server and --kill-server cannot be used together.")
+    if common_cmd_key:
+        final_command_str = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
+        if not final_command_str:
+            config_path = Path(config.AGDOCS_DIR) / "conf" / "agro.conf.yml"
+            msg = f"Common command '{common_cmd_key}' not found in 'MUSTER_COMMON_CMDS'."
+            if config_path.is_file():
+                msg += f" Check your config file at '{config_path}'."
+            else:
+                msg += f" No config file found at '{config_path}'."
 
-    indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
+            available_cmds = ", ".join(sorted(config.MUSTER_COMMON_CMDS.keys()))
+            if available_cmds:
+                msg += f" Available commands are: {available_cmds}."
+
+            raise ValueError(msg)
+    else:
+        final_command_str = command_str
+
+    if not branch_patterns:
+        patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
+        logger.info(
+            f"No branch pattern specified. Using default pattern for output branches: '{config.WORKTREE_OUTPUT_BRANCH_PREFIX}*'"
+        )
+    else:
+        patterns_to_use = branch_patterns
+
+    indices = _get_indices_from_branch_patterns(patterns_to_use, show_cmd_output)
     if not indices:
         logger.warning("No worktrees found matching the provided patterns.")
         return
 
     worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
 
-    use_shell = False
-    final_command_str = command_str
+    if not final_command_str:
+        raise ValueError("Empty command provided.")
 
-    if kill_server:
-        final_command_str = "kill $(cat server.pid) && rm -f server.pid server.log"
-        use_shell = True
-    elif server:
-        if not command_str.strip():
-            raise ValueError("Empty command provided for --server.")
-        final_command_str = f"{command_str} > server.log 2>&1 & echo $! > server.pid"
-        use_shell = True
+    # Detect if shell is needed for complex commands (e.g., with pipes, redirects)
+    shell_chars = ['|', '&', ';', '<', '>', '(', ')', '$', '`']
+    use_shell = any(char in final_command_str for char in shell_chars)
 
     if use_shell:
         command = final_command_str
@@ -1068,6 +1154,108 @@ def fade_branches(patterns, show_cmd_output=False):
     )
 
 
+def clean_worktrees(branch_patterns=None, mode="hard", show_cmd_output=False):
+    """Deletes worktrees and optionally their branches based on patterns."""
+    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
+    if not worktree_state and not branch_patterns:
+        logger.info("No worktrees found to clean.")
+        return
+
+    if not branch_patterns:
+        patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
+        logger.info(
+            f"No branch pattern specified. Using default pattern for output branches: '{config.WORKTREE_OUTPUT_BRANCH_PREFIX}*'"
+        )
+    else:
+        patterns_to_use = branch_patterns
+
+    all_matching_branches = set()
+    for pattern in patterns_to_use:
+        matching_branches = _get_matching_branches(
+            pattern, show_cmd_output=show_cmd_output
+        )
+        all_matching_branches.update(matching_branches)
+
+    worktrees_to_delete = {}  # 't1': 'output/branch.1'
+    for wt_name, branch in worktree_state.items():
+        if branch in all_matching_branches:
+            worktrees_to_delete[wt_name] = branch
+
+    branches_to_delete = all_matching_branches if mode == "hard" else set()
+
+    if not worktrees_to_delete and not branches_to_delete:
+        logger.info("No worktrees or branches found matching the criteria to clean.")
+        return
+
+    logger.info("\n--- Dry Run ---")
+    if worktrees_to_delete:
+        logger.info("The following worktrees will be deleted:")
+        for wt_name, branch in sorted(worktrees_to_delete.items()):
+            logger.info(f"  - {wt_name} (branch: {branch})")
+
+    if branches_to_delete:
+        logger.info("The following branches will be deleted (hard clean):")
+        for branch in sorted(list(branches_to_delete)):
+            logger.info(f"  - {branch}")
+    logger.info("--- End Dry Run ---\n")
+
+    try:
+        confirm = input("Proceed with cleaning? [Y/n]: ")
+    except (EOFError, KeyboardInterrupt):
+        logger.warning("\nOperation cancelled.")
+        return
+    if confirm.lower() not in ("y", ""):
+        logger.warning("Operation cancelled by user.")
+        return
+
+    if worktrees_to_delete:
+        indices_to_delete = [int(wt_name[1:]) for wt_name in worktrees_to_delete]
+        logger.info("\nDeleting worktrees...")
+        for index in sorted(indices_to_delete):
+            try:
+                # This will not trigger confirmation prompt in delete_tree
+                delete_tree(str(index), show_cmd_output=show_cmd_output)
+            except Exception as e:
+                logger.error(f"Failed to delete worktree for index {index}: {e}")
+
+    if branches_to_delete:
+        logger.info("\nDeleting branches (hard clean)...")
+        result = _run_command(
+            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
+            capture_output=True,
+            check=True,
+            show_cmd_output=show_cmd_output,
+        )
+        current_branch = result.stdout.strip()
+
+        deleted_count = 0
+        failed_count = 0
+        for branch in sorted(list(branches_to_delete)):
+            if branch == current_branch:
+                logger.warning(f"Skipping currently checked out branch '{branch}'")
+                continue
+
+            result = _run_command(
+                ["git", "branch", "-D", branch],
+                capture_output=True,
+                check=False,
+                show_cmd_output=show_cmd_output,
+            )
+            if result.returncode == 0:
+                logger.info(f"Deleted branch '{branch}'.")
+                deleted_count += 1
+            else:
+                logger.error(f"Failed to delete branch '{branch}':")
+                if result.stderr:
+                    logger.error(result.stderr.strip())
+                failed_count += 1
+        logger.info(
+            f"\nBranch cleanup complete. Deleted {deleted_count} branches, {failed_count} failed."
+        )
+
+    logger.info("\n✅ Clean complete.")
+
+
 def mirror_docs(show_cmd_output=False):
     """Mirrors the documentation directory to its public counterpart."""
     source_dir_str = config.AGDOCS_DIR
diff --git a/syncdocs b/syncdocs
deleted file mode 100755
index ae8ee09..0000000
--- a/syncdocs
+++ /dev/null
@@ -1 +0,0 @@
-rsync -av --delete .agdocs/ .public-agdocs/
\ No newline at end of file
diff --git a/tests/test_cli.py b/tests/test_cli.py
index 4c30e95..e6908b4 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -3,7 +3,7 @@ from unittest.mock import patch
 
 import pytest
 
-from agro.cli import _dispatch_exec, _is_indices_list
+from agro.cli import _dispatch_exec, _is_indices_list, _dispatch_muster
 
 
 @pytest.mark.parametrize(
@@ -468,6 +468,67 @@ def test_dispatch_exec_infer_agent_type_from_positional_exec_cmd(
         )
 
 
+@patch("agro.cli.core.muster_command")
+def test_dispatch_muster(mock_muster_command):
+    # Basic case: command and pattern
+    args = argparse.Namespace(
+        command_str="ls",
+        branch_patterns=["p1"],
+        common_cmd_key=None,
+        verbose=0,
+    )
+    _dispatch_muster(args)
+    mock_muster_command.assert_called_once_with(
+        command_str="ls",
+        branch_patterns=["p1"],
+        common_cmd_key=None,
+        show_cmd_output=False,
+    )
+    mock_muster_command.reset_mock()
+
+    # Common command and pattern
+    args = argparse.Namespace(
+        command_str="p1",
+        branch_patterns=[],
+        common_cmd_key="testq",
+        verbose=0,
+    )
+    _dispatch_muster(args)
+    mock_muster_command.assert_called_once_with(
+        command_str=None,
+        branch_patterns=["p1"],
+        common_cmd_key="testq",
+        show_cmd_output=False,
+    )
+    mock_muster_command.reset_mock()
+
+    # Common command, no pattern
+    args = argparse.Namespace(
+        command_str=None,
+        branch_patterns=[],
+        common_cmd_key="testq",
+        verbose=0,
+    )
+    _dispatch_muster(args)
+    mock_muster_command.assert_called_once_with(
+        command_str=None,
+        branch_patterns=[],
+        common_cmd_key="testq",
+        show_cmd_output=False,
+    )
+    mock_muster_command.reset_mock()
+
+    # No command and no common command -> error
+    args = argparse.Namespace(
+        command_str=None,
+        branch_patterns=[],
+        common_cmd_key=None,
+        verbose=0,
+    )
+    with pytest.raises(ValueError):
+        _dispatch_muster(args)
+
+
 @patch("agro.cli.core.exec_agent")
 @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
 @patch("agro.cli.core.find_task_file")
diff --git a/tests/test_core.py b/tests/test_core.py
index cfa4b46..f1ab286 100644
--- a/tests/test_core.py
+++ b/tests/test_core.py
@@ -259,3 +259,337 @@ def test_fade_branches_no_match(mock_logger, mock_get_matching_branches):
     mock_logger.info.assert_called_with(
         "No branches found matching the patterns to delete."
     )
+
+
+@patch("agro.core.Path")
+@patch("agro.core._get_indices_from_branch_patterns")
+@patch("agro.core.get_worktree_state")
+@patch("agro.core._run_command")
+@patch("agro.core.logger")
+def test_diff_worktrees(
+    mock_logger,
+    mock_run_command,
+    mock_get_worktree_state,
+    mock_get_indices,
+    mock_path,
+):
+    # setup
+    mock_get_indices.return_value = [1, 2]
+    mock_get_worktree_state.return_value = {
+        "t1": "output/branch.1",
+        "t2": "output/branch.2",
+    }
+    # Mock Path(...).is_dir() to return True
+    mock_path.return_value.__truediv__.return_value.is_dir.return_value = True
+
+    # test without stat
+    core.diff_worktrees([], stat=False, show_cmd_output=False)
+
+    mock_get_indices.assert_called_once()
+    mock_get_worktree_state.assert_called_once()
+
+    expected_calls = [
+        call(
+            ["git", "diff", "tree/t1", "HEAD"],
+            cwd=str(mock_path.return_value / "t1"),
+            show_cmd_output=True,
+        ),
+        call(
+            ["git", "diff", "tree/t2", "HEAD"],
+            cwd=str(mock_path.return_value / "t2"),
+            show_cmd_output=True,
+        ),
+    ]
+    mock_run_command.assert_has_calls(expected_calls)
+    assert mock_run_command.call_count == 2
+
+    # test with stat
+    mock_run_command.reset_mock()
+    core.diff_worktrees([], stat=True, show_cmd_output=False)
+    expected_calls_stat = [
+        call(
+            ["git", "diff", "--stat", "tree/t1", "HEAD"],
+            cwd=str(mock_path.return_value / "t1"),
+            show_cmd_output=True,
+        ),
+        call(
+            ["git", "diff", "--stat", "tree/t2", "HEAD"],
+            cwd=str(mock_path.return_value / "t2"),
+            show_cmd_output=True,
+        ),
+    ]
+    mock_run_command.assert_has_calls(expected_calls_stat)
+    assert mock_run_command.call_count == 2
+
+    # test no indices
+    mock_run_command.reset_mock()
+    mock_get_indices.return_value = []
+    core.diff_worktrees([], stat=False, show_cmd_output=False)
+    mock_run_command.assert_not_called()
+    mock_logger.warning.assert_called_with("No worktrees found matching the provided patterns.")
+
+    # test worktree dir not found
+    mock_logger.reset_mock()
+    mock_run_command.reset_mock()
+    mock_get_indices.return_value = [1]
+    mock_path.return_value.__truediv__.return_value.is_dir.return_value = False
+    core.diff_worktrees([], stat=False, show_cmd_output=False)
+    mock_run_command.assert_not_called()
+    mock_logger.warning.assert_called_with(
+        f"Worktree t1 at '{mock_path.return_value / 't1'}' not found. Skipping."
+    )
+
+
+@patch("agro.core.logger")
+@patch("builtins.input", return_value="y")
+@patch("agro.core._run_command")
+@patch("agro.core.delete_tree")
+@patch("agro.core._get_matching_branches")
+@patch("agro.core.get_worktree_state")
+def test_clean_worktrees_hard(
+    mock_get_worktree_state,
+    mock_get_matching_branches,
+    mock_delete_tree,
+    mock_run_command,
+    mock_input,
+    mock_logger,
+):
+    # Arrange
+    mock_get_worktree_state.return_value = {
+        "t1": "output/feat.1",
+        "t2": "output/feat.2",
+        "t3": "another/branch",
+    }
+    mock_get_matching_branches.return_value = ["output/feat.1", "output/feat.2"]
+    # for git rev-parse HEAD
+    mock_run_command.return_value = MagicMock(stdout="main")
+
+    # Act
+    core.clean_worktrees(branch_patterns=["output/feat.*"], mode="hard", show_cmd_output=False)
+
+    # Assert
+    mock_get_matching_branches.assert_called_once_with("output/feat.*", show_cmd_output=False)
+
+    # Dry run logs
+    mock_logger.info.assert_any_call("The following worktrees will be deleted:")
+    mock_logger.info.assert_any_call("  - t1 (branch: output/feat.1)")
+    mock_logger.info.assert_any_call("  - t2 (branch: output/feat.2)")
+    mock_logger.info.assert_any_call("The following branches will be deleted (hard clean):")
+    mock_logger.info.assert_any_call("  - output/feat.1")
+    mock_logger.info.assert_any_call("  - output/feat.2")
+
+    mock_input.assert_called_once()
+
+    # delete_tree calls
+    mock_delete_tree.assert_has_calls(
+        [
+            call("1", show_cmd_output=False),
+            call("2", show_cmd_output=False),
+        ],
+        any_order=True,
+    )
+    assert mock_delete_tree.call_count == 2
+
+    # branch deletion calls
+    # 1 for git rev-parse, 2 for git branch -D
+    assert mock_run_command.call_count == 3
+    mock_run_command.assert_any_call(
+        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
+        capture_output=True,
+        check=True,
+        show_cmd_output=False,
+    )
+    mock_run_command.assert_any_call(
+        ["git", "branch", "-D", "output/feat.1"],
+        capture_output=True,
+        check=False,
+        show_cmd_output=False,
+    )
+    mock_run_command.assert_any_call(
+        ["git", "branch", "-D", "output/feat.2"],
+        capture_output=True,
+        check=False,
+        show_cmd_output=False,
+    )
+
+
+@patch("agro.core.logger")
+@patch("builtins.input", return_value="y")
+@patch("agro.core._run_command")
+@patch("agro.core.delete_tree")
+@patch("agro.core._get_matching_branches")
+@patch("agro.core.get_worktree_state")
+def test_clean_worktrees_soft(
+    mock_get_worktree_state,
+    mock_get_matching_branches,
+    mock_delete_tree,
+    mock_run_command,
+    mock_input,
+    mock_logger,
+):
+    # Arrange
+    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
+    mock_get_matching_branches.return_value = ["output/feat.1"]
+
+    # Act
+    core.clean_worktrees(branch_patterns=["output/feat.1"], mode="soft", show_cmd_output=False)
+
+    # Assert
+    mock_logger.info.assert_any_call("The following worktrees will be deleted:")
+    mock_logger.info.assert_any_call("  - t1 (branch: output/feat.1)")
+    # Ensure hard clean message is NOT present
+    for call_args in mock_logger.info.call_args_list:
+        assert "branches will be deleted" not in call_args[0][0]
+
+    mock_input.assert_called_once()
+    mock_delete_tree.assert_called_once_with("1", show_cmd_output=False)
+    mock_run_command.assert_not_called()  # No branch deletion
+
+
+@patch("agro.core.config")
+@patch("agro.core.logger")
+@patch("builtins.input", return_value="y")
+@patch("agro.core.delete_tree")
+@patch("agro.core._get_matching_branches")
+@patch("agro.core.get_worktree_state")
+def test_clean_worktrees_no_pattern(
+    mock_get_worktree_state,
+    mock_get_matching_branches,
+    mock_delete_tree,
+    mock_input,
+    mock_logger,
+    mock_config,
+):
+    # Arrange
+    mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
+    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
+    mock_get_matching_branches.return_value = ["output/feat.1"]
+
+    # Act
+    core.clean_worktrees(branch_patterns=[], mode="soft", show_cmd_output=False)
+
+    # Assert
+    mock_get_matching_branches.assert_called_once_with("output/", show_cmd_output=False)
+    mock_delete_tree.assert_called_once_with("1", show_cmd_output=False)
+
+
+@patch("agro.core.logger")
+@patch("builtins.input", return_value="n")
+@patch("agro.core.delete_tree")
+@patch("agro.core._get_matching_branches")
+@patch("agro.core.get_worktree_state")
+def test_clean_worktrees_cancel(
+    mock_get_worktree_state,
+    mock_get_matching_branches,
+    mock_delete_tree,
+    mock_input,
+    mock_logger,
+):
+    # Arrange
+    mock_get_worktree_state.return_value = {"t1": "output/feat.1"}
+    mock_get_matching_branches.return_value = ["output/feat.1"]
+
+    # Act
+    core.clean_worktrees(branch_patterns=["output/feat.1"], mode="hard", show_cmd_output=False)
+
+    # Assert
+    mock_input.assert_called_once()
+    mock_logger.warning.assert_called_with("Operation cancelled by user.")
+    mock_delete_tree.assert_not_called()
+
+
+@patch("agro.core.Path")
+@patch("agro.core.config")
+@patch("agro.core._get_indices_from_branch_patterns")
+@patch("agro.core.get_worktree_state")
+@patch("agro.core._run_command")
+@patch("agro.core.logger")
+def test_muster_command(
+    mock_logger,
+    mock_run_command,
+    mock_get_worktree_state,
+    mock_get_indices,
+    mock_config,
+    mock_path,
+):
+    # Arrange
+    mock_get_indices.return_value = [1]
+    mock_get_worktree_state.return_value = {"t1": "output/branch.1"}
+    mock_path.return_value.is_dir.return_value = True
+    mock_config.MUSTER_COMMON_CMDS = {
+        "testq": "uv run pytest -q",
+        "server-start": "my-app --daemon > server.log 2>&1 &",
+        "server-kill": "kill $(cat server.pid)",
+    }
+    mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
+    mock_config.AGDOCS_DIR = ".agdocs"
+
+    # Test with common command (no shell)
+    core.muster_command(
+        command_str=None,
+        branch_patterns=["output/branch.1"],
+        common_cmd_key="testq",
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        ["uv", "run", "pytest", "-q"],
+        cwd=str(mock_path.return_value / "t1"),
+        shell=False,
+        show_cmd_output=True,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with positional command (no shell)
+    core.muster_command(
+        command_str="ls -l",
+        branch_patterns=["output/branch.1"],
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        ["ls", "-l"],
+        cwd=str(mock_path.return_value / "t1"),
+        shell=False,
+        show_cmd_output=True,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with server-start common command (needs shell)
+    core.muster_command(
+        command_str=None,
+        branch_patterns=["output/branch.1"],
+        common_cmd_key="server-start",
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        "my-app --daemon > server.log 2>&1 &",
+        cwd=str(mock_path.return_value / "t1"),
+        shell=True,
+        show_cmd_output=True,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with server-kill common command (needs shell)
+    core.muster_command(
+        command_str=None,
+        branch_patterns=["output/branch.1"],
+        common_cmd_key="server-kill",
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        "kill $(cat server.pid)",
+        cwd=str(mock_path.return_value / "t1"),
+        shell=True,
+        show_cmd_output=True,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with no branch pattern (uses default)
+    core.muster_command(command_str="ls", branch_patterns=[], show_cmd_output=False)
+    mock_get_indices.assert_called_with(["output/"], False)
+    mock_logger.info.assert_any_call(
+        "No branch pattern specified. Using default pattern for output branches: 'output/*'"
+    )
+
+    # Test common command not found
+    with pytest.raises(ValueError, match="Common command 'nonexistent' not found"):
+        core.muster_command(command_str=None, branch_patterns=[], common_cmd_key="nonexistent")
