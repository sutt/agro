Your task is to update the existing documentation in ./docs/ to account for changes to expected behavior of agro cli tool.

You'll be given a diff of all changes made, and a changelog summary you should update, keeping with the same flow and formatting of docs

Do not add any extraneous resource updates, only those that need reflecting in the changes presented

Add TODO statements where there is ambiguity or need developer assistance to fill in details.

Do not alter ./docs/case-studies

git diff v0.1.7 HEAD -- . ':(exclude)docs/'

diff --git a/.public-agdocs/conf/agro.conf.yml b/.public-agdocs/conf/agro.conf.yml
index af9f0ab..54c14ae 100644
--- a/.public-agdocs/conf/agro.conf.yml
+++ b/.public-agdocs/conf/agro.conf.yml
@@ -72,9 +72,18 @@ EXEC_CMD_DEFAULT: maider.sh
 
 # --- Muster ---
 
+# Default timeout in seconds for commands run with 'agro muster'.
+# A value of 0 or null means no timeout.
+# MUSTER_DEFAULT_TIMEOUT: 20
+
 # Pre-defined commands for 'agro muster -c'.
 MUSTER_COMMON_CMDS:
-  testq: "uv run pytest --tb=no -q"
-  server-start: "uv run python app/main.py > server.log 2>&1 & echo $! > server.pid"
-  server-kill: "kill $(cat server.pid) && rm -f server.pid server.log"
-  gitone: "git log -n 1 --oneline"
+  testq:
+    cmd: "uv run pytest --tb=no -q"
+  server-start:
+    cmd: "uv run python app/main.py > server.log 2>&1 & echo $! > server.pid"
+    timeout: null
+  server-kill:
+    cmd: "kill $(cat server.pid) && rm -f server.pid server.log"
+  gitone:
+    cmd: "git log -n 1 --oneline"
diff --git a/README.md b/README.md
index ec04c53..391299e 100644
--- a/README.md
+++ b/README.md
@@ -4,8 +4,8 @@ A script to manage git worktrees for agent-based development. This tool simplifi
 
 [![PyPI version](https://img.shields.io/pypi/v/agro)](https://pypi.org/project/agro/)
 
-- **View [Docs](./docs)**
-- **View [Case Studies](./docs/case-studies/)**
+- **View [Docs](./docs/index.md)**
+- **View [Case Studies](./docs/case-studies/index.md)**
 - **View [AI Dev Log](./docs/dev-summary-v1.md)**
 
 ---
@@ -39,7 +39,7 @@ So you can take agro to your nineteen side-projects and four remote jobs, and it
 **Supported Models:** _Anthropic, OpenAI, Google, Grok4 and more_
 
 ---
-**Agro-Builds-Agro:** If you think vibe-coding can't stand-up to multiple iterations, this is your chance to think again. Agro is 150 commits and going strong (roughly 80% ai generated). See the [Dev Log](./docs/dev-summary-v1.md) and [Case Studies](./docs/case-studies) to see a record of all the prompts and their accepted solutions.
+**Agro-Builds-Agro:** If you think vibe-coding can't stand-up to multiple iterations, this is your chance to think again. Agro is 150 commits and going strong (roughly 80% ai generated). See the [Dev Log](./docs/dev-summary-v1.md) and [Case Studies](./docs/case-studies/index.md) to see a record of all the prompts and their accepted solutions.
 
 ---
 
@@ -66,29 +66,61 @@ For local dev updates run the `./redeploy` script to reinstall the local repo as
 
 ---
 
-### At a Glance - Hello, World!
+### Agro at a glance - Hello, World!
 
-**Also see the [case studies](./docs/case-studies/aba-1.md) for more advanced guidance on using this tool**
+**Also see the [case studies](./docs/case-studies/index.md) for more advanced guidance on using this tool**
 
-**0. Clone the Demo Repo**
+**0A. Clone the Demo Repo**
 
 ```bash
-git clone git@github.com:sutt/agro-demo.git
+git clone https://github.com/sutt/agro-demo
 cd agro-demo
 
+# setup environment and run server
 uv sync
+uv run python app/main.py
+# hit ctrl+c to shutdown server, and let's start...
 ```
 
+**0B. Copy the supplied docs**
+
+Copy the public git-tracked `.public-agdocs` directory to an internal git-ignored repo `.agdocs`
+
+```bash
+cp -r .public-agdocs .agdocs
+```
+
+The `.agdocs` directory is the default lookup for where **agro** will attempt to access configurations, guidance, and 
+
+This repo comes with tasks (.md files in /specs/ subdirectory). These should now be available if you copied it correctly in the step above.
+
+```
+.agdocs/
+├── conf
+│   └── agro.conf.yml
+├── guides
+│   └── GUIDE.md
+├── specs
+│   ├── add-about.md
+│   ├── infer-model.md
+│   └── query-web.md
+└── swap
+```
+
+
 **1. Launch four agents in parallel**
 
-_Agro is configured to use aider by default. Add the name of the coding agent you have installed as the argument to use the one you have installed._
 
 ```bash
 $ agro exec add-about 2       # launch two agents of aider 
 $ agro exec add-about claude  # if you have claude-code installed
 $ agro exec add-about gemini  # if you have gemini installed
 ```
-This repo comes with tasks in `.agdocs/specs` including the spec
+_Agro is configured to use aider by default. Add the name of the coding agent you have installed as the argument to use the one you have installed, see [docs for more info on this](./docs/configuration.md#default-agent)._
+
+_For the purposes of this tutorial, you don't need to launch all three different type of agents, simple use one or two that you have installed. If you don't have any installed, find instructions of how to install [here](./docs/agents.md#agent-installation)._
+
+These commands launched agents on a pre-written task in `.agdocs/specs/add-about.md`. _(Ultimately you will write your own but let's start with a simple pre-written one.)_
 
 **add-about.md**
 >add an about page and route
@@ -150,14 +182,14 @@ $ git branch
 **2. Launch Server on each worktree**
 
 ```bash
-agro muster --server 'uv run python app/main.py' output
+agro muster -c server-start
 ```
-- The argument `--server` allows detach mode to run multiple servers out of one shell.
+- The argument `-c` / `--common-cmd` arg allows us to pass an alias for common commands we'll use. See [docs on common commands](./docs/configuration.md#muster-common-commands) for more info.
 
 **Output**
 
 ```bash
-agro muster --server 'uv run python app/main.py' output
+agro muster -c server-start output
 
 --- Running command in t1 (output/add-about.1) ---
 $ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
@@ -197,8 +229,8 @@ curl http://localhost:8004/about
 Now clean up the server:
 
 ```bash
-# run muster with --kill-server to take it down each worktree
-$ agro muster --kill-server '' output
+# run muster with server-kill (builtin common command) to take it down each worktree
+$ agro muster -c server-kill
 
 --- Running command in t1 (output/add-about.1) ---
 $ kill $(cat server.pid) && rm -f server.pid server.log
@@ -229,7 +261,7 @@ $ uv run pytest -q
 So we see have 3 existing tests, now let's check the output of our agents:
 
 ```bash
-$ agro muster 'uv run pytest -q' output
+$ agro muster -c testq output
 
 --- Running command in t1 (output/add-about.1) ---
 $ uv run pytest -q
@@ -247,13 +279,21 @@ $ uv run pytest -q
 $ uv run pytest -q
 3 passed in 0.24s
 ```
+Cool, so we see all Agents left the tests green, and Agents 1-3 added a new unit test (since they now have 4 tests and we started with 3 tests).
+
+**Check the code changes from each agent**
+
+TODO - add the agro diff command
+
+TODO - add the branch-patterns example
+
 ### Or add your own spec to a project
 
 For example:
 
 **Create and commit a spec file and pass to an agent**
 ```bash
-agro init # add .agdocs/ to repo
+agro init # if you don't already have an `.agdocs` at root
 
 # create a spec
 agro task hello-world  
@@ -261,9 +301,11 @@ agro task hello-world
 # equivalent to:
 echo "add hello world to the readme of this project" > .agdocs/specs/hello-world.md
 
-agro exec
-# equivalent to:
-agro exec add-about 1 aider
+agro exec  
+# when not supplying an argument for the task name, 
+# agro will chose the most recently modified .md file in specs/, so 
+# this is equivalent to:
+agro exec hello-world 1 aider
 ```
 
 ### Full Walk-Through
@@ -275,35 +317,30 @@ TODO - add a full tutorial here
 
 TODO
 
-### Full Help
+### Help
 
 ```
-
-usage: agro [-h] [--version] [-v] [-q]
+usage: agro [-v / -vv] <subcommand> [subcommand-args]
 
 A script to manage git branches & worktrees for agent-based development.
 
-options:
-  -h, --help     show this help message and exit
-  --version      Show program's version number and exit.
-  -v, --verbose  Increase verbosity. -v for debug, -vv for command output.
-  -q, --quiet    Suppress all output except warnings and errors.
-
 Main command:
   exec [args] [taskfile] [num-trees] [exec-cmd]   
                                 
     Run an agent in new worktree(s)
         args:
-          -n <num-trees>        Number of worktrees to create.
-          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree.
+          -n <num-trees>        Number of worktrees / agents to create.
+          -c <exec-cmd>         Custom command to launch agent on worktree.
           -a <agent-type>       Specify agent type to override config.
                                 Supported: aider, claude, gemini.
 
 Other Commands:
-  muster <command> <branch-patterns>    Run a command in specified worktrees.
+  muster [opts] [command] [branch-patterns]    Run a command in specified worktrees.
+  diff [branch-patterns] [diff-opts]   Show git diff for specified worktrees.
   surrender [branch-patterns]   Kill running agent processes (default: all).
   grab <branch-name>            Checkout a branch, creating a copy if it's in use.
   fade <branch-patterns>        Delete local branches matching a regex pattern.
+  clean [opts] [branch-patterns]    Clean up worktrees and/or branches.
   state [branch-patterns]       Show the worktree to branch mappings (default: all).
   task [task-name]              Create a new task spec file and open it.
   init                          Initialize agro project structure in .agdocs/.
@@ -321,8 +358,11 @@ Common options for 'make' and 'exec':
   --no-env-overrides  Do not add port overrides to the .env file.
 
 Options for 'muster':
-  -s, --server        Run command as a background server (and log server PID)
-  -k, --kill-server   Kill the background server and clean up pid/log files.
+  -c, --common-cmd <key> Run a pre-defined command from config.
+
+Options for 'clean':
+  --soft              Only delete worktrees, not branches.
+  --hard              Delete both worktrees and branches (default).
     
 Options for 'init':
   --conf              Only add a template agro.conf.yml to .agdocs/conf
diff --git a/pyproject.toml b/pyproject.toml
index e12c1c2..ad42df7 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,7 +13,8 @@ authors = [
 ]
 requires-python = ">=3.9"
 dependencies = [
-    "PyYAML"
+    "PyYAML",
+    "argcomplete"
 ]
 
 [project.scripts]
diff --git a/src/agro/cli.py b/src/agro/cli.py
index afd0a95..9c1559c 100644
--- a/src/agro/cli.py
+++ b/src/agro/cli.py
@@ -1,3 +1,4 @@
+import argcomplete
 import argparse
 import logging
 import os
@@ -9,6 +10,21 @@ from . import core, __version__
 logger = logging.getLogger("agro")
 
 
+def branch_completer(prefix, parsed_args, **kwargs):
+    """A completer for git branch names."""
+    try:
+        all_branches = core._get_all_branches()
+    except Exception:
+        return []
+
+    if not prefix:
+        # Default to output branches if no prefix
+        default_prefix = core.config.WORKTREE_OUTPUT_BRANCH_PREFIX
+        return [b for b in all_branches if b.startswith(default_prefix)]
+
+    return [b for b in all_branches if b.startswith(prefix)]
+
+
 def _is_indices_list(s):
     """Check if a string is a comma-separated list of digits."""
     if not s:
@@ -106,6 +122,22 @@ def _dispatch_exec(args):
     )
 
 
+def _dispatch_init(args):
+    """Helper to dispatch init command."""
+    show_output = args.verbose >= 2
+    # If --completions is used, only do that.
+    if args.completions:
+        core.setup_completions(mode=args.completions, show_cmd_output=show_output)
+        return
+
+    # Otherwise, do the normal init...
+    core.init_project(conf_only=args.conf)
+
+    # ...and if it's a full init (not --conf), also set up completions.
+    if not args.conf:
+        core.setup_completions(mode="current", show_cmd_output=show_output)
+
+
 def _dispatch_muster(args):
     """Helper to dispatch muster command with complex argument parsing."""
     command_str = args.command_str
@@ -127,6 +159,16 @@ def _dispatch_muster(args):
         branch_patterns=branch_patterns,
         common_cmd_key=common_cmd_key,
         show_cmd_output=(args.verbose >= 2),
+        timeout=args.timeout,
+    )
+
+
+def _dispatch_diff(args):
+    """Helper to dispatch diff command with complex argument parsing."""
+    core.diff_worktrees(
+        branch_patterns=args.branch_patterns,
+        diff_opts=args.diff_opts,
+        show_cmd_output=(args.verbose >= 2),
     )
 
 
+@@ -146,7 +188,7 @@ def main():
 
 Other Commands:
   muster [opts] [command] [branch-patterns]    Run a command in specified worktrees.
-  diff [branch-patterns]        Show git diff for specified worktrees.
+  diff [branch-patterns] [diff-opts]   Show git diff for specified worktrees.
   surrender [branch-patterns]   Kill running agent processes (default: all).
   grab <branch-name>            Checkout a branch, creating a copy if it's in use.
   fade <branch-patterns>        Delete local branches matching a regex pattern.
@@ -169,16 +211,15 @@ Common options for 'make' and 'exec':
 
 Options for 'muster':
   -c, --common-cmd <key> Run a pre-defined command from config.
-
-Options for 'diff':
-  --stat              Show diffstat instead of full diff.
+  --timeout <seconds>   Override command timeout. 0 for no timeout.
 
 Options for 'clean':
   --soft              Only delete worktrees, not branches.
   --hard              Delete both worktrees and branches (default).
     
 Options for 'init':
-  --conf              Only add a template agro.conf.yml to .agdocs/conf"""
+  --conf              Only add a template agro.conf.yml to .agdocs/conf
+  --completions [perm]  Setup shell completions ('perm' for permanent)."""
     parser = argparse.ArgumentParser(
         description="A script to manage git branches & worktrees for agent-based development.",
         prog="agro",
@@ -212,12 +253,21 @@ Options for 'init':
         "init",
         help="Initialize the .agdocs directory structure for the project.",
     )
-    parser_init.add_argument(
+    init_group = parser_init.add_mutually_exclusive_group()
+    init_group.add_argument(
         "--conf",
         action="store_true",
         help="Only generate a blank config file. Fails if the file already exists.",
     )
-    parser_init.set_defaults(func=lambda args: core.init_project(conf_only=args.conf))
+    init_group.add_argument(
+        "--completions",
+        nargs="?",
+        const="current",
+        default=None,
+        choices=["current", "perm"],
+        help="Setup shell completions. With no argument, sets up for current session. Use 'perm' for permanent setup via .bashrc.",
+    )
+    parser_init.set_defaults(func=_dispatch_init)
 
     # --- mirror command ---
     parser_mirror = subparsers.add_parser(
@@ -330,6 +380,12 @@ Options for 'init':
         dest="common_cmd_key",
         help="Run a pre-defined command from config.",
     )
+    parser_muster.add_argument(
+        "--timeout",
+        type=int,
+        default=None,
+        help="Timeout in seconds for the command. Use 0 for no timeout.",
+    )
     parser_muster.add_argument(
         "command_str",
         nargs="?",
@@ -341,7 +397,7 @@ Options for 'init':
         nargs="*",
         default=[],
         help="One or more branch patterns. Defaults to output branches.",
-    )
+    ).completer = branch_completer
     parser_muster.set_defaults(func=_dispatch_muster)
 
     # --- diff command ---
@@ -352,26 +408,15 @@ Options for 'init':
         "branch_patterns",
         nargs="*",
         default=[],
-        help="Optional branch pattern(s) to select worktrees. Defaults to all.",
-    )
-    parser_diff.add_argument(
-        "--stat",
-        action="store_true",
-        help="Show diffstat instead of full diff.",
-    )
-    parser_diff.set_defaults(
-        func=lambda args: core.diff_worktrees(
-            args.branch_patterns,
-            stat=args.stat,
-            show_cmd_output=(args.verbose >= 2),
-        )
-    )
+        help="Optional branch pattern(s).",
+    ).completer = branch_completer
+    parser_diff.set_defaults(func=_dispatch_diff)
 
     # --- grab command ---
     parser_grab = subparsers.add_parser(
         "grab", help="Checkout a branch, creating a copy if it's in use by another worktree."
     )
-    parser_grab.add_argument("branch_name", help="The branch to grab.")
+    parser_grab.add_argument("branch_name", help="The branch to grab.").completer = branch_completer
     parser_grab.set_defaults(
         func=lambda args: core.grab_branch(
             args.branch_name, show_cmd_output=(args.verbose >= 2)
@@ -384,7 +429,7 @@ Options for 'init':
     )
     parser_fade.add_argument(
         "patterns", nargs="+", help="One or more patterns to match branch names against."
-    )
+    ).completer = branch_completer
     parser_fade.set_defaults(
         func=lambda args: core.fade_branches(
             args.patterns, show_cmd_output=(args.verbose >= 2)
@@ -401,7 +446,7 @@ Options for 'init':
         nargs="*",
         default=[],
         help="Optional branch pattern(s) to select what to clean. Defaults to all output branches.",
-    )
+    ).completer = branch_completer
     clean_group = parser_clean.add_mutually_exclusive_group()
     clean_group.add_argument(
         "--soft",
@@ -430,7 +475,7 @@ Options for 'init':
         nargs="*",
         default=[],
         help="Optional branch pattern(s) to select worktrees. Defaults to all.",
-    )
+    ).completer = branch_completer
     parser_surrender.set_defaults(
         func=lambda args: core.surrender(
             args.branch_patterns, show_cmd_output=(args.verbose >= 2)
@@ -446,7 +491,7 @@ Options for 'init':
         nargs="*",
         default=[],
         help="Optional glob-style pattern(s) to filter branches by name.",
-    )
+    ).completer = branch_completer
     parser_state.set_defaults(
         func=lambda args: core.state(
             branch_patterns=args.branch_pattern, show_cmd_output=(args.verbose >= 2)
@@ -473,8 +518,47 @@ Options for 'init':
     parser_help = subparsers.add_parser("help", help="Show this help message.")
     parser_help.set_defaults(func=lambda args: parser.print_help())
 
+    argcomplete.autocomplete(parser)
+
     try:
-        args = parser.parse_args()
+        args, unknown_args = parser.parse_known_args()
+
+        if args.command == "diff":
+            # Reconstruct raw args after 'diff' to support '--' pathspec passthrough
+            try:
+                diff_idx = sys.argv.index("diff") + 1
+                tail = sys.argv[diff_idx:]
+            except ValueError:
+                tail = []
+
+            # Split on '--' to separate pathspec (after) from patterns/options (before)
+            if "--" in tail:
+                dd_i = tail.index("--")
+                before_dd = tail[:dd_i]
+                after_dd = tail[dd_i + 1 :]
+            else:
+                before_dd = tail
+                after_dd = []
+
+            # Extract branch patterns from the start until the first option
+            branch_patterns = []
+            diff_opts = []
+            reached_opts = False
+            for tok in before_dd:
+                if not reached_opts and not tok.startswith("-"):
+                    branch_patterns.append(tok)
+                else:
+                    reached_opts = True
+                    diff_opts.append(tok)
+
+            if after_dd:
+                diff_opts.extend(["--"] + after_dd)
+
+            # Override parsed values
+            args.branch_patterns = branch_patterns
+            args.diff_opts = diff_opts
+        elif unknown_args:
+            parser.error(f"unrecognized arguments: {' '.join(unknown_args)}")
 
         # Setup logging
         if args.quiet:
diff --git a/src/agro/config.py b/src/agro/config.py
index 470953d..7009b6c 100644
--- a/src/agro/config.py
+++ b/src/agro/config.py
@@ -45,10 +45,14 @@ DEFAULTS = {
         'claude': 600,
         'gemini': 600,  # 10 minutes timeout for gemini calls
     },
+    'MUSTER_DEFAULT_TIMEOUT': 20,
     'MUSTER_COMMON_CMDS': {
-        'testq': 'uv run pytest --tb=no -q',
-        'server-start': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
-        'server-kill': 'kill $(cat server.pid) && rm -f server.pid server.log',
+        'testq': {'cmd': 'uv run pytest --tb=no -q'},
+        'server-start': {
+            'cmd': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
+            'timeout': None,
+        },
+        'server-kill': {'cmd': 'kill $(cat server.pid) && rm -f server.pid server.log'},
     },
     'AGRO_EDITOR_CMD': 'code',
     'ENV_SETUP_CMDS': [
@@ -82,7 +86,16 @@ def _load_config():
                                 config['AGENT_CONFIG'][agent_name] = agent_data
 
                     if 'MUSTER_COMMON_CMDS' in user_config and isinstance(user_config['MUSTER_COMMON_CMDS'], dict):
-                        config['MUSTER_COMMON_CMDS'].update(user_config.pop('MUSTER_COMMON_CMDS'))
+                        user_muster_cmds = user_config.pop('MUSTER_COMMON_CMDS')
+                        for key, value in user_muster_cmds.items():
+                            if (
+                                key in config['MUSTER_COMMON_CMDS']
+                                and isinstance(config['MUSTER_COMMON_CMDS'][key], dict)
+                                and isinstance(value, dict)
+                            ):
+                                config['MUSTER_COMMON_CMDS'][key].update(value)
+                            else:
+                                config['MUSTER_COMMON_CMDS'][key] = value
 
                     config.update(user_config)
             except yaml.YAMLError as e:
@@ -111,6 +124,7 @@ EXEC_CMD_DEFAULT = _config['EXEC_CMD_DEFAULT']
 AGENT_TYPE = _config['AGENT_TYPE']
 AGENT_CONFIG = _config['AGENT_CONFIG']
 AGENT_TIMEOUTS = _config['AGENT_TIMEOUTS']
+MUSTER_DEFAULT_TIMEOUT = _config['MUSTER_DEFAULT_TIMEOUT']
 MUSTER_COMMON_CMDS = _config['MUSTER_COMMON_CMDS']
 AGRO_EDITOR_CMD = _config['AGRO_EDITOR_CMD']
 ENV_SETUP_CMDS = _config['ENV_SETUP_CMDS']
diff --git a/src/agro/core.py b/src/agro/core.py
index 343d2b7..e1084c1 100644
--- a/src/agro/core.py
+++ b/src/agro/core.py
@@ -162,8 +162,15 @@ def _get_config_template():
 
     # Format MUSTER_COMMON_CMDS
     muster_common_cmds_lines = ["# MUSTER_COMMON_CMDS:"]
-    for key, cmd in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
-        muster_common_cmds_lines.append(f"#   {key}: {json.dumps(cmd)}")
+    for key, data in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
+        if isinstance(data, dict):
+            muster_common_cmds_lines.append(f"#   {key}:")
+            muster_common_cmds_lines.append(f'#     cmd: {json.dumps(data.get("cmd"))}')
+            if "timeout" in data:
+                timeout_val = "null" if data["timeout"] is None else data["timeout"]
+                muster_common_cmds_lines.append(f"#     timeout: {timeout_val}")
+        else: # old format for robustness
+            muster_common_cmds_lines.append(f"#   {key}: {json.dumps(data)}")
     muster_common_cmds_str = "\n".join(muster_common_cmds_lines)
 
     return f"""# Agro Configuration File
@@ -226,6 +233,10 @@ def _get_config_template():
 
 # --- Muster ---
 
+# Default timeout in seconds for commands run with 'agro muster'.
+# A value of 0 or null means no timeout.
+# MUSTER_DEFAULT_TIMEOUT: {config.DEFAULTS['MUSTER_DEFAULT_TIMEOUT']}
+
 # Pre-defined commands for 'agro muster -c'.
 {muster_common_cmds_str}
 """
@@ -296,6 +307,55 @@ def init_project(conf_only=False):
     logger.debug(f"Created: {agdocs_dir}/.gitignore")
 
 
+def setup_completions(mode, show_cmd_output=False):
+    """Sets up shell completions for agro."""
+    shell = os.environ.get("SHELL", "")
+    if "bash" not in shell:
+        logger.error("Shell is not bash. Completions are only supported for bash.")
+        logger.error("For more information, see the documentation.")
+        raise RuntimeError("Completions only supported for bash.")
+
+    if mode == "perm":
+        if not shutil.which("uv"):
+            logger.error(
+                "'uv' command not found, which is required for permanent completion setup."
+            )
+            logger.error("Please install uv: https://github.com/astral-sh/uv")
+            logger.error("For more information, see the documentation.")
+            raise RuntimeError("'uv' command not found.")
+
+        bashrc_path = Path.home() / ".bashrc"
+        if not bashrc_path.is_file():
+            logger.warning(f"~/.bashrc not found. Cannot set up permanent completions.")
+            return
+
+        completion_line = '# agro cli completions\neval "$(uvx --from argcomplete register-python-argcomplete agro)"\n'
+
+        content = bashrc_path.read_text()
+        if completion_line.strip() in content:
+            logger.info("Agro completions already configured in ~/.bashrc.")
+            return
+
+        logger.info("Adding completions to ~/.bashrc...")
+        with bashrc_path.open("a") as f:
+            f.write("\n" + completion_line)
+        logger.info(
+            "✅ Permanent completions set up. Please restart your shell or run 'source ~/.bashrc'."
+        )
+
+    elif mode == "current":
+        logger.info("To enable tab completion for the current session, run:")
+        cmd = 'eval "$(register-python-argcomplete agro)"'
+        logger.info(f"  {cmd}")
+        if not shutil.which("register-python-argcomplete"):
+            logger.warning(
+                "\nWarning: 'register-python-argcomplete' not found in PATH."
+            )
+            logger.warning(
+                "You may need to run: 'eval \"$(uvx --from argcomplete register-python-argcomplete agro)\"' instead."
+            )
+
+
 def create_task_file(task_name=None, show_cmd_output=False):
     """Creates a new task spec file and opens it in the editor."""
     if not task_name:
@@ -357,6 +417,7 @@ def _run_command(
     shell=False,
     show_cmd_output=False,
     suppress_error_logging=False,
+    timeout=None,
 ):
     """Helper to run a shell command."""
     cmd_str = command if isinstance(command, str) else shlex.join(command)
@@ -373,8 +434,19 @@ def _run_command(
             text=True,
             capture_output=do_capture,
             shell=shell,
+            timeout=timeout,
         )
         return result
+    except subprocess.TimeoutExpired as e:
+        if not suppress_error_logging:
+            cmd_str = command if isinstance(command, str) else shlex.join(command)
+            logger.error(f"Timeout of {timeout}s expired for command: {cmd_str}")
+            # If output was captured, it's in the exception.
+            if e.stdout:
+                logger.error(f"STDOUT:\n{e.stdout.strip()}")
+            if e.stderr:
+                logger.error(f"STDERR:\n{e.stderr.strip()}")
+        raise
     except subprocess.CalledProcessError as e:
         if not suppress_error_logging:
             cmd_str = command if isinstance(command, str) else shlex.join(command)
@@ -915,9 +987,18 @@ def _get_indices_from_branch_patterns(branch_patterns=None, show_cmd_output=Fals
     return sorted(matching_indices)
 
 
-def diff_worktrees(branch_patterns, stat=False, show_cmd_output=False):
+def diff_worktrees(branch_patterns, diff_opts=None, show_cmd_output=False):
     """Runs 'git diff' in multiple worktrees."""
-    indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
+    # Default to output branches if no pattern is provided
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
@@ -939,9 +1020,27 @@ def diff_worktrees(branch_patterns, stat=False, show_cmd_output=False):
 
         original_branch = f"{config.WORKTREE_BRANCH_PREFIX}{index}"
         command = ["git", "diff"]
-        if stat:
-            command.append("--stat")
-        command.extend([original_branch, "HEAD"])
+
+        pre_opts = []
+        pathspec = []
+        if diff_opts:
+            if "--" in diff_opts:
+                dd_idx = diff_opts.index("--")
+                pre_opts = diff_opts[:dd_idx]
+                pathspec = diff_opts[dd_idx + 1 :]
+            else:
+                pre_opts = diff_opts
+
+        if pathspec:
+            # When a pathspec is provided, add options, then commits, then '--' and paths
+            command.extend(pre_opts)
+            command.extend([original_branch, "HEAD"])
+            command.append("--")
+            command.extend(pathspec)
+        else:
+            # No pathspec: place options before the commits
+            command.extend(pre_opts)
+            command.extend([original_branch, "HEAD"])
 
         cmd_str = shlex.join(command)
         logger.info(f"$ {cmd_str}")
@@ -963,11 +1062,15 @@ def muster_command(
     branch_patterns,
     show_cmd_output=False,
     common_cmd_key=None,
+    timeout=None,
 ):
     """Runs a command in multiple worktrees."""
+    final_command_str = None
+    cmd_timeout = None
+
     if common_cmd_key:
-        final_command_str = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
-        if not final_command_str:
+        common_cmd_config = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
+        if not common_cmd_config:
             config_path = Path(config.AGDOCS_DIR) / "conf" / "agro.conf.yml"
             msg = f"Common command '{common_cmd_key}' not found in 'MUSTER_COMMON_CMDS'."
             if config_path.is_file():
@@ -978,11 +1081,32 @@ def muster_command(
             available_cmds = ", ".join(sorted(config.MUSTER_COMMON_CMDS.keys()))
             if available_cmds:
                 msg += f" Available commands are: {available_cmds}."
-
             raise ValueError(msg)
+
+        if isinstance(common_cmd_config, dict):
+            final_command_str = common_cmd_config.get("cmd")
+            if "timeout" in common_cmd_config:
+                cmd_timeout = common_cmd_config.get("timeout")
+                if cmd_timeout is None:
+                    cmd_timeout = 0
+        else:  # Support old string-only format
+            final_command_str = common_cmd_config
+
+        if not final_command_str:
+            raise ValueError(f"Command not found for common command key '{common_cmd_key}'")
     else:
         final_command_str = command_str
 
+    # Determine timeout: CLI > common_cmd config > global config > default
+    if timeout is not None:
+        effective_timeout = timeout if timeout > 0 else None
+    elif cmd_timeout is not None:
+        effective_timeout = cmd_timeout if cmd_timeout > 0 else None
+    else:
+        effective_timeout = (
+            config.MUSTER_DEFAULT_TIMEOUT if config.MUSTER_DEFAULT_TIMEOUT > 0 else None
+        )
+
     if not branch_patterns:
         patterns_to_use = [config.WORKTREE_OUTPUT_BRANCH_PREFIX]
         logger.info(
@@ -1031,8 +1155,9 @@ def muster_command(
                 cwd=str(worktree_path),
                 shell=use_shell,
                 show_cmd_output=True,
+                timeout=effective_timeout,
             )
-        except (subprocess.CalledProcessError, FileNotFoundError):
+        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
             # _run_command already prints details.
             logger.error(f"--- Command failed in t{index}. Continuing... ---")
             continue
diff --git a/tests/test_cli.py b/tests/test_cli.py
index e6908b4..c5b49b2 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -3,7 +3,7 @@ from unittest.mock import patch
 
 import pytest
 
-from agro.cli import _dispatch_exec, _is_indices_list, _dispatch_muster
+from agro.cli import _dispatch_diff, _dispatch_exec, _is_indices_list, _dispatch_muster, _dispatch_init
 
 
 @pytest.mark.parametrize(
@@ -476,6 +476,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=["p1"],
         common_cmd_key=None,
         verbose=0,
+        timeout=None,
     )
     _dispatch_muster(args)
     mock_muster_command.assert_called_once_with(
@@ -483,6 +484,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=["p1"],
         common_cmd_key=None,
         show_cmd_output=False,
+        timeout=None,
     )
     mock_muster_command.reset_mock()
 
@@ -492,6 +494,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=[],
         common_cmd_key="testq",
         verbose=0,
+        timeout=10,
     )
     _dispatch_muster(args)
     mock_muster_command.assert_called_once_with(
@@ -499,6 +502,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=["p1"],
         common_cmd_key="testq",
         show_cmd_output=False,
+        timeout=10,
     )
     mock_muster_command.reset_mock()
 
@@ -508,6 +512,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=[],
         common_cmd_key="testq",
         verbose=0,
+        timeout=None,
     )
     _dispatch_muster(args)
     mock_muster_command.assert_called_once_with(
@@ -515,6 +520,7 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=[],
         common_cmd_key="testq",
         show_cmd_output=False,
+        timeout=None,
     )
     mock_muster_command.reset_mock()
 
@@ -524,11 +530,36 @@ def test_dispatch_muster(mock_muster_command):
         branch_patterns=[],
         common_cmd_key=None,
         verbose=0,
+        timeout=None,
     )
     with pytest.raises(ValueError):
         _dispatch_muster(args)
 
 
+@patch("agro.cli.core.diff_worktrees")
+@pytest.mark.parametrize(
+    "branch_patterns, diff_opts",
+    [
+        (["p1"], ["--stat"]),
+        ([], ["--stat"]),
+        (["p1", "p2"], ["--stat", "--color"]),
+    ],
+)
+def test_dispatch_diff(mock_diff_worktrees, branch_patterns, diff_opts):
+    """Test dispatch_diff passes patterns and opts correctly."""
+    args = argparse.Namespace(
+        branch_patterns=branch_patterns,
+        diff_opts=diff_opts,
+        verbose=0,
+    )
+    _dispatch_diff(args)
+    mock_diff_worktrees.assert_called_once_with(
+        branch_patterns=branch_patterns,
+        diff_opts=diff_opts,
+        show_cmd_output=False,
+    )
+
+
 @patch("agro.cli.core.exec_agent")
 @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
 @patch("agro.cli.core.find_task_file")
@@ -561,3 +592,47 @@ def test_dispatch_exec_no_inference_when_both_provided(
             agent_type="aider",
             auto_commit=True,
         )
+
+
+@patch("agro.cli.core.setup_completions")
+@patch("agro.cli.core.init_project")
+def test_dispatch_init_default(mock_init, mock_setup_completions):
+    """Test `agro init` runs full init and sets up current completions."""
+    args = argparse.Namespace(completions=None, conf=False, verbose=0)
+    _dispatch_init(args)
+    mock_init.assert_called_once_with(conf_only=False)
+    mock_setup_completions.assert_called_once_with(
+        mode="current", show_cmd_output=False
+    )
+
+
+@patch("agro.cli.core.setup_completions")
+@patch("agro.cli.core.init_project")
+def test_dispatch_init_conf_only(mock_init, mock_setup_completions):
+    """Test `agro init --conf` only creates config and does not set up completions."""
+    args = argparse.Namespace(completions=None, conf=True, verbose=0)
+    _dispatch_init(args)
+    mock_init.assert_called_once_with(conf_only=True)
+    mock_setup_completions.assert_not_called()
+
+
+@patch("agro.cli.core.setup_completions")
+@patch("agro.cli.core.init_project")
+def test_dispatch_init_completions_current_only(mock_init, mock_setup_completions):
+    """Test `agro init --completions` only sets up current completions."""
+    args = argparse.Namespace(completions="current", conf=False, verbose=2)
+    _dispatch_init(args)
+    mock_init.assert_not_called()
+    mock_setup_completions.assert_called_once_with(
+        mode="current", show_cmd_output=True
+    )
+
+
+@patch("agro.cli.core.setup_completions")
+@patch("agro.cli.core.init_project")
+def test_dispatch_init_completions_perm_only(mock_init, mock_setup_completions):
+    """Test `agro init --completions perm` only sets up permanent completions."""
+    args = argparse.Namespace(completions="perm", conf=False, verbose=0)
+    _dispatch_init(args)
+    mock_init.assert_not_called()
+    mock_setup_completions.assert_called_once_with(mode="perm", show_cmd_output=False)
diff --git a/tests/test_core.py b/tests/test_core.py
index f1ab286..11f5ce8 100644
--- a/tests/test_core.py
+++ b/tests/test_core.py
@@ -282,8 +282,8 @@ def test_diff_worktrees(
     # Mock Path(...).is_dir() to return True
     mock_path.return_value.__truediv__.return_value.is_dir.return_value = True
 
-    # test without stat
-    core.diff_worktrees([], stat=False, show_cmd_output=False)
+    # test with no diff_opts
+    core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
 
     mock_get_indices.assert_called_once()
     mock_get_worktree_state.assert_called_once()
@@ -303,9 +303,9 @@ def test_diff_worktrees(
     mock_run_command.assert_has_calls(expected_calls)
     assert mock_run_command.call_count == 2
 
-    # test with stat
+    # test with one diff_opt
     mock_run_command.reset_mock()
-    core.diff_worktrees([], stat=True, show_cmd_output=False)
+    core.diff_worktrees([], diff_opts=["--stat"], show_cmd_output=False)
     expected_calls_stat = [
         call(
             ["git", "diff", "--stat", "tree/t1", "HEAD"],
@@ -321,10 +321,66 @@ def test_diff_worktrees(
     mock_run_command.assert_has_calls(expected_calls_stat)
     assert mock_run_command.call_count == 2
 
+    # test with multiple diff_opts
+    mock_run_command.reset_mock()
+    core.diff_worktrees([], diff_opts=["--stat", "--cached"], show_cmd_output=False)
+    expected_calls_multiple = [
+        call(
+            ["git", "diff", "--stat", "--cached", "tree/t1", "HEAD"],
+            cwd=str(mock_path.return_value / "t1"),
+            show_cmd_output=True,
+        ),
+        call(
+            ["git", "diff", "--stat", "--cached", "tree/t2", "HEAD"],
+            cwd=str(mock_path.return_value / "t2"),
+            show_cmd_output=True,
+        ),
+    ]
+    mock_run_command.assert_has_calls(expected_calls_multiple)
+    assert mock_run_command.call_count == 2
+
+    # test with pathspec
+    mock_run_command.reset_mock()
+    core.diff_worktrees([], diff_opts=["--", "my/path"], show_cmd_output=False)
+    expected_calls_pathspec = [
+        call(
+            ["git", "diff", "tree/t1", "HEAD", "--", "my/path"],
+            cwd=str(mock_path.return_value / "t1"),
+            show_cmd_output=True,
+        ),
+        call(
+            ["git", "diff", "tree/t2", "HEAD", "--", "my/path"],
+            cwd=str(mock_path.return_value / "t2"),
+            show_cmd_output=True,
+        ),
+    ]
+    mock_run_command.assert_has_calls(expected_calls_pathspec)
+    assert mock_run_command.call_count == 2
+
+    # test with options and pathspec
+    mock_run_command.reset_mock()
+    core.diff_worktrees(
+        [], diff_opts=["--stat", "--", "my/path"], show_cmd_output=False
+    )
+    expected_calls_opts_pathspec = [
+        call(
+            ["git", "diff", "--stat", "tree/t1", "HEAD", "--", "my/path"],
+            cwd=str(mock_path.return_value / "t1"),
+            show_cmd_output=True,
+        ),
+        call(
+            ["git", "diff", "--stat", "tree/t2", "HEAD", "--", "my/path"],
+            cwd=str(mock_path.return_value / "t2"),
+            show_cmd_output=True,
+        ),
+    ]
+    mock_run_command.assert_has_calls(expected_calls_opts_pathspec)
+    assert mock_run_command.call_count == 2
+
     # test no indices
     mock_run_command.reset_mock()
     mock_get_indices.return_value = []
-    core.diff_worktrees([], stat=False, show_cmd_output=False)
+    core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
     mock_run_command.assert_not_called()
     mock_logger.warning.assert_called_with("No worktrees found matching the provided patterns.")
 
@@ -333,7 +389,7 @@ def test_diff_worktrees(
     mock_run_command.reset_mock()
     mock_get_indices.return_value = [1]
     mock_path.return_value.__truediv__.return_value.is_dir.return_value = False
-    core.diff_worktrees([], stat=False, show_cmd_output=False)
+    core.diff_worktrees([], diff_opts=None, show_cmd_output=False)
     mock_run_command.assert_not_called()
     mock_logger.warning.assert_called_with(
         f"Worktree t1 at '{mock_path.return_value / 't1'}' not found. Skipping."
@@ -517,10 +573,14 @@ def test_muster_command(
     mock_get_worktree_state.return_value = {"t1": "output/branch.1"}
     mock_path.return_value.is_dir.return_value = True
     mock_config.MUSTER_COMMON_CMDS = {
-        "testq": "uv run pytest -q",
-        "server-start": "my-app --daemon > server.log 2>&1 &",
-        "server-kill": "kill $(cat server.pid)",
+        "testq": {"cmd": "uv run pytest -q"},
+        "server-start": {
+            "cmd": "my-app --daemon > server.log 2>&1 &",
+            "timeout": None,
+        },
+        "server-kill": {"cmd": "kill $(cat server.pid)"},
     }
+    mock_config.MUSTER_DEFAULT_TIMEOUT = 20
     mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
     mock_config.AGDOCS_DIR = ".agdocs"
 
@@ -536,6 +596,7 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=False,
         show_cmd_output=True,
+        timeout=20,
     )
     mock_run_command.reset_mock()
 
@@ -550,10 +611,11 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=False,
         show_cmd_output=True,
+        timeout=20,
     )
     mock_run_command.reset_mock()
 
-    # Test with server-start common command (needs shell)
+    # Test with server-start common command (needs shell, no timeout)
     core.muster_command(
         command_str=None,
         branch_patterns=["output/branch.1"],
@@ -565,10 +627,11 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=True,
         show_cmd_output=True,
+        timeout=None,
     )
     mock_run_command.reset_mock()
 
-    # Test with server-kill common command (needs shell)
+    # Test with server-kill common command (needs shell, default timeout)
     core.muster_command(
         command_str=None,
         branch_patterns=["output/branch.1"],
@@ -580,6 +643,7 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=True,
         show_cmd_output=True,
+        timeout=20,
     )
     mock_run_command.reset_mock()
 
@@ -593,3 +657,73 @@ def test_muster_command(
     # Test common command not found
     with pytest.raises(ValueError, match="Common command 'nonexistent' not found"):
         core.muster_command(command_str=None, branch_patterns=[], common_cmd_key="nonexistent")
+
+
+@patch("agro.core.Path")
+@patch("agro.core.config")
+@patch("agro.core._get_indices_from_branch_patterns", return_value=[1])
+@patch("agro.core.get_worktree_state", return_value={"t1": "b1"})
+@patch("agro.core._run_command")
+def test_muster_command_timeout_overrides(
+    mock_run_command,
+    mock_get_worktree_state,
+    mock_get_indices,
+    mock_config,
+    mock_path,
+):
+    mock_path.return_value.is_dir.return_value = True
+    mock_config.MUSTER_DEFAULT_TIMEOUT = 20
+    mock_config.MUSTER_COMMON_CMDS = {
+        "default_timeout": {"cmd": "cmd1"},
+        "custom_timeout": {"cmd": "cmd2", "timeout": 10},
+        "no_timeout": {"cmd": "cmd3", "timeout": 0},
+        "null_timeout": {"cmd": "cmd4", "timeout": None},
+    }
+
+    # 1. Default timeout from config
+    core.muster_command(command_str="some-cmd", branch_patterns=["b1"])
+    mock_run_command.assert_called_with(
+        ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=20
+    )
+
+    # 2. Common command with default timeout
+    core.muster_command(command_str=None, common_cmd_key="default_timeout", branch_patterns=["b1"])
+    mock_run_command.assert_called_with(
+        ["cmd1"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=20
+    )
+
+    # 3. Common command with custom timeout
+    core.muster_command(command_str=None, common_cmd_key="custom_timeout", branch_patterns=["b1"])
+    mock_run_command.assert_called_with(
+        ["cmd2"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=10
+    )
+
+    # 4. Common command with timeout: 0
+    core.muster_command(command_str=None, common_cmd_key="no_timeout", branch_patterns=["b1"])
+    mock_run_command.assert_called_with(
+        ["cmd3"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
+    )
+
+    # 5. Common command with timeout: null
+    core.muster_command(command_str=None, common_cmd_key="null_timeout", branch_patterns=["b1"])
+    mock_run_command.assert_called_with(
+        ["cmd4"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
+    )
+
+    # 6. CLI flag overrides common command timeout
+    core.muster_command(command_str=None, common_cmd_key="custom_timeout", branch_patterns=["b1"], timeout=30)
+    mock_run_command.assert_called_with(
+        ["cmd2"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=30
+    )
+
+    # 7. CLI flag overrides default timeout
+    core.muster_command(command_str="some-cmd", branch_patterns=["b1"], timeout=30)
+    mock_run_command.assert_called_with(
+        ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=30
+    )
+
+    # 8. CLI flag of 0 means no timeout
+    core.muster_command(command_str="some-cmd", branch_patterns=["b1"], timeout=0)
+    mock_run_command.assert_called_with(
+        ["some-cmd"], cwd=str(mock_path.return_value / "t1"), shell=False, show_cmd_output=True, timeout=None
+    )
diff --git a/uv.lock b/uv.lock
index b688172..244eb86 100644
--- a/uv.lock
+++ b/uv.lock
@@ -7,6 +7,7 @@ name = "agro"
 version = "0.1.7"
 source = { editable = "." }
 dependencies = [
+    { name = "argcomplete" },
     { name = "pyyaml" },
 ]
 
@@ -21,6 +22,7 @@ test = [
 
 [package.metadata]
 requires-dist = [
+    { name = "argcomplete" },
     { name = "build", marker = "extra == 'dev'", specifier = ">=1.2.2.post1" },
     { name = "pytest", marker = "extra == 'test'", specifier = ">=8.4.1" },
     { name = "pyyaml" },
@@ -28,6 +30,15 @@ requires-dist = [
 ]
 provides-extras = ["dev", "test"]
 
+[[package]]
+name = "argcomplete"
+version = "3.6.2"
+source = { registry = "https://pypi.org/simple" }
+sdist = { url = "https://files.pythonhosted.org/packages/16/0f/861e168fc813c56a78b35f3c30d91c6757d1fd185af1110f1aec784b35d0/argcomplete-3.6.2.tar.gz", hash = "sha256:d0519b1bc867f5f4f4713c41ad0aba73a4a5f007449716b16f385f2166dc6adf", size = 73403, upload-time = "2025-04-03T04:57:03.52Z" }
+wheels = [
+    { url = "https://files.pythonhosted.org/packages/31/da/e42d7a9d8dd33fa775f467e4028a47936da2f01e4b0e561f9ba0d74cb0ca/argcomplete-3.6.2-py3-none-any.whl", hash = "sha256:65b3133a29ad53fb42c48cf5114752c7ab66c1c38544fdf6460f450c09b42591", size = 43708, upload-time = "2025-04-03T04:57:01.591Z" },
+]
+
 [[package]]
 name = "backports-tarfile"
 version = "1.2.0"



