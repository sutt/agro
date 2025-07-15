Below is a diff from v0.1.4 to v0.1.5.

Add entries to docs/CHANGELOG.md to describe the change

diff --git a/pyproject.toml b/pyproject.toml
index f11c5ce..03c2f7d 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@ build-backend = "setuptools.build_meta"
 
 [project]
 name = "agro"
-version = "0.1.4"
+version = "0.1.5"
 description = "CLI wrapper for CLI-agents"
 readme = "README.md"
 license = {text = "MIT"}
@@ -22,7 +22,7 @@ agro = "agro.cli:main"
 [tool.setuptools.packages.find]
 where = ["src"]
 
-[dependency-groups]
+[project.optional-dependencies]
 dev = [
     "build>=1.2.2.post1",
     "twine>=6.1.0",
diff --git a/src/agro/cli.py b/src/agro/cli.py
index 11ab156..238ad6c 100644
--- a/src/agro/cli.py
+++ b/src/agro/cli.py
@@ -82,6 +82,20 @@ def _dispatch_exec(args):
                 "No task file specified and no task files found in default directory."
             )
 
+    agent_type = args.agent_type_opt
+
+    # Infer agent_type from exec_cmd if not provided
+    if exec_cmd and not agent_type:
+        for at in core.config.AGENT_CONFIG:
+            if at in exec_cmd:
+                agent_type = at
+                logger.debug(f"Inferred agent type '{agent_type}' from exec_cmd '{exec_cmd}'")
+                break
+    # Infer exec_cmd from agent_type if not provided
+    elif agent_type and not exec_cmd:
+        exec_cmd = agent_type
+        logger.debug(f"Inferred exec_cmd '{exec_cmd}' from agent_type '{agent_type}'")
+
     core.exec_agent(
         task_file=taskfile,
         fresh_env=args.fresh_env,
@@ -91,6 +105,8 @@ def _dispatch_exec(args):
         indices_str=args.tree_indices,
         num_trees=num_trees,
         show_cmd_output=(args.verbose >= 2),
+        agent_type=agent_type,
+        auto_commit=not args.no_auto_commit,
     )
 
 
@@ -257,6 +273,19 @@ Options for 'init':
         help="Run the exec-cmd to launch agent on worktree.",
     )
 
+    parser_exec.add_argument(
+        "-a",
+        "--agent-type",
+        dest="agent_type_opt",
+        help="Specify agent type to override config (e.g., 'aider', 'claude', 'gemini').",
+    )
+
+    parser_exec.add_argument(
+        "--no-auto-commit",
+        action="store_true",
+        help="Disable automatic committing of changes after agent run.",
+    )
+
     parser_exec.add_argument(
         "agent_args",
         nargs=argparse.REMAINDER,
diff --git a/src/agro/committer.py b/src/agro/committer.py
new file mode 100644
index 0000000..e2a9031
--- /dev/null
+++ b/src/agro/committer.py
@@ -0,0 +1,112 @@
+import logging
+import os
+import subprocess
+import sys
+import time
+
+
+def setup_logging(worktree_path):
+    """Set up logging to a file in the worktree's .git directory."""
+    log_file = os.path.join(worktree_path, ".agswap", "agro-committer.log")
+    logging.basicConfig(
+        level=logging.DEBUG,
+        format="%(asctime)s - %(process)d - %(levelname)s - %(message)s",
+        filename=log_file,
+        filemode="w",
+    )
+
+
+def wait_for_pid(pid):
+    """Wait for a process with a given PID to exit."""
+    logging.info(f"Monitoring PID {pid}. Waiting for it to exit.")
+    # On Unix, we can use a simple poll with os.kill(pid, 0)
+    # This will raise an OSError if the process does not exist.
+    while True:
+        try:
+            os.kill(pid, 0)
+            time.sleep(5)
+        except OSError:
+            logging.info(f"Process {pid} has exited.")
+            break
+
+
+def git_commit_changes(worktree_path, task_file, agent_type):
+    """Check for changes in the git repo and commit them if any are found."""
+    logging.info(f"Checking for git changes in {worktree_path}")
+    try:
+        # Check if there are any changes
+        res = subprocess.run(
+            ["git", "status", "--porcelain"],
+            cwd=worktree_path,
+            text=True,
+            capture_output=True,
+        )
+        if res.returncode != 0:
+            logging.error(f"'git status' failed: {res.stderr}")
+            return
+        if not res.stdout.strip():
+            logging.info("No changes detected. Nothing to commit.")
+            return
+
+        logging.info("Changes detected. Staging all changes.")
+        subprocess.run(
+            ["git", "add", "."],
+            cwd=worktree_path,
+            check=True,
+            capture_output=True,
+            text=True,
+        )
+
+        task_file_stem = os.path.splitext(task_file)[0]
+        commit_message = (
+            f"feat: impl {task_file_stem} with {agent_type} (agro auto-commit)"
+        )
+        logging.info(f"Committing with message: '{commit_message}'")
+        subprocess.run(
+            ["git", "commit", "-m", commit_message],
+            cwd=worktree_path,
+            check=True,
+            capture_output=True,
+            text=True,
+        )
+        logging.info("Successfully committed changes.")
+
+    except subprocess.CalledProcessError as e:
+        logging.error(f"A git command failed in {worktree_path}: {e}")
+        logging.error(f"Stderr: {e.stderr.strip()}")
+        logging.error(f"Stdout: {e.stdout.strip()}")
+    except Exception as e:
+        logging.error(f"An unexpected error occurred in git_commit_changes: {e}")
+
+
+def main():
+    """Main entry point for the committer script."""
+    if len(sys.argv) != 5:
+        print(
+            "Usage: python -m agro.committer <pid> <worktree_path> <task_file> <agent_type>",
+            file=sys.stderr,
+        )
+        sys.exit(1)
+
+    try:
+        pid = int(sys.argv[1])
+        worktree_path = sys.argv[2]
+        task_file = sys.argv[3]
+        agent_type = sys.argv[4]
+    except (ValueError, IndexError):
+        print("Invalid arguments.", file=sys.stderr)
+        print(
+            "Usage: python -m agro.committer <pid> <worktree_path> <task_file> <agent_type>",
+            file=sys.stderr,
+        )
+        sys.exit(1)
+
+    setup_logging(worktree_path)
+    logging.info("Committer script started.")
+    wait_for_pid(pid)
+    git_commit_changes(worktree_path, task_file, agent_type)
+    logging.info("Committer script finished.")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/src/agro/config.py b/src/agro/config.py
index e3b3d82..bdb6f49 100644
--- a/src/agro/config.py
+++ b/src/agro/config.py
@@ -10,10 +10,45 @@ DEFAULTS = {
     'WORKTREE_BRANCH_PREFIX': 'tree/t',
     'WORKTREE_OUTPUT_BRANCH_PREFIX': 'output/',
     'EXEC_CMD_DEFAULT': 'aider',
+    'AGENT_TYPE': 'aider',
+    'AGENT_CONFIG': {
+        'aider': {
+            'task_file_arg_template': ['-f', '{task_file}'],
+            'args': [
+                "--yes",
+                "--no-check-update",
+                "--no-attribute-author",
+                "--no-attribute-committer",
+                "--no-attribute-co-authored-by",
+            ]
+        },
+        'claude': {
+            'task_file_arg_template': None,
+            'args': [
+                "-d",
+                "--allowedTools",
+                "Write Edit MultiEdit",
+                "--max-turns",
+                "30",
+                "-p",
+            ]
+        },
+        'gemini': {
+            'task_file_arg_template': None,
+            'args': [
+                "-y",
+            ],
+        }
+    },
+    'AGENT_TIMEOUTS': {
+        'aider': 0,  # 0 means no timeout is applied.
+        'claude': 600,
+        'gemini': 600,  # 10 minutes timeout for gemini calls
+    },
     'AGRO_EDITOR_CMD': 'code',
     'ENV_SETUP_CMDS': [
         'uv venv',
-        'uv sync --quiet --group test',
+        'uv sync --quiet --all-extras',
     ],
     'BASE_API_PORT': 8000,
 }
@@ -30,10 +65,28 @@ def _load_config():
             try:
                 user_config = yaml.safe_load(f)
                 if user_config:
+                    if 'AGENT_TIMEOUTS' in user_config and isinstance(user_config['AGENT_TIMEOUTS'], dict):
+                        config['AGENT_TIMEOUTS'].update(user_config.pop('AGENT_TIMEOUTS'))
+
+                    if 'AGENT_CONFIG' in user_config and isinstance(user_config['AGENT_CONFIG'], dict):
+                        user_agent_config = user_config.pop('AGENT_CONFIG')
+                        for agent_name, agent_data in user_agent_config.items():
+                            if agent_name in config['AGENT_CONFIG']:
+                                config['AGENT_CONFIG'][agent_name].update(agent_data)
+                            else:
+                                config['AGENT_CONFIG'][agent_name] = agent_data
+
                     config.update(user_config)
             except yaml.YAMLError as e:
                 print(f"Warning: Could not parse config file {config_path}. Using default values. Error: {e}", file=sys.stderr)
 
+    valid_agent_types = {"aider", "gemini", "claude"}
+    agent_type = config.get('AGENT_TYPE')
+    if agent_type not in valid_agent_types:
+        valid_types_str = ", ".join(sorted(list(valid_agent_types)))
+        print(f"Error: Invalid AGENT_TYPE '{agent_type}'. Must be one of {valid_types_str}.", file=sys.stderr)
+        sys.exit(1)
+
     return config
 
 _config = _load_config()
@@ -47,6 +100,9 @@ WORKTREE_OUTPUT_BRANCH_PREFIX = _config['WORKTREE_OUTPUT_BRANCH_PREFIX']
 
 # Agro-Agent Configs
 EXEC_CMD_DEFAULT = _config['EXEC_CMD_DEFAULT']
+AGENT_TYPE = _config['AGENT_TYPE']
+AGENT_CONFIG = _config['AGENT_CONFIG']
+AGENT_TIMEOUTS = _config['AGENT_TIMEOUTS']
 AGRO_EDITOR_CMD = _config['AGRO_EDITOR_CMD']
 ENV_SETUP_CMDS = _config['ENV_SETUP_CMDS']
 
diff --git a/src/agro/core.py b/src/agro/core.py
index 7dabf44..5a8c33f 100644
--- a/src/agro/core.py
+++ b/src/agro/core.py
@@ -94,7 +94,7 @@ def _get_config_template():
 # For example, to install all optional dependency groups with uv:
 # ENV_SETUP_CMDS:
 #   - 'uv venv'
-#   - 'uv sync --quiet --group test'
+#   - 'uv sync --quiet --all-extras'
 
 
 # --- Agent Execution ---
@@ -102,6 +102,26 @@ def _get_config_template():
 # Default command to execute for 'agro exec'.
 # EXEC_CMD_DEFAULT: {config.DEFAULTS['EXEC_CMD_DEFAULT']}
 
+# The type of agent being used. Determines how built-in flags are passed.
+# Supported values: "aider", "claude", "gemini".
+# AGENT_TYPE: {config.DEFAULTS['AGENT_TYPE']}
+
+# Agent-specific configuration.
+# AGENT_CONFIG:
+#   aider:
+#     args: ["--yes", "--no-check-update", "--no-attribute-author", "--no-attribute-committer", "--no-attribute-co-authored-by"]
+#   claude:
+#     args: ["-d", "--allowedTools", "Write Edit MultiEdit", "--max-turns", "30", "-p"]
+#   gemini:
+#     args: ["-y"]
+
+# Agent-specific timeout settings in seconds.
+# A value of 0 means no timeout is applied, overriding any default.
+# AGENT_TIMEOUTS:
+#   aider: 0
+#   claude: 600
+#   gemini: 600
+
 # Default command to open spec files with 'agro task'.
 # AGRO_EDITOR_CMD: {config.DEFAULTS['AGRO_EDITOR_CMD']}
 """
@@ -495,6 +515,8 @@ def exec_agent(
     indices_str=None,
     num_trees=None,
     show_cmd_output=False,
+    agent_type=None,
+    auto_commit=True,
 ):
     """Deletes, recreates, and runs detached agent processes in worktrees."""
     task_path = Path(task_file)
@@ -610,33 +632,76 @@ def exec_agent(
 
         log_file_path = agswap_dir / "agro-exec.log"
         exec_command = exec_cmd or config.EXEC_CMD_DEFAULT
-        command = [
-            exec_command,
-            "--yes",
-            "-f",
-            str(task_in_swap_path.relative_to(worktree_path)),
-            "--no-check-update",
-            "--no-attribute-author",
-            "--no-attribute-committer",
-            "--no-attribute-co-authored-by",
-        ] + agent_args
 
-        with open(log_file_path, "wb") as log_file:
-            process = subprocess.Popen(
-                command,
-                cwd=str(worktree_path),
-                stdout=log_file,
-                stderr=subprocess.STDOUT,
-                start_new_session=True,  # Detach from parent
+        agent_type_to_use = agent_type or config.AGENT_TYPE
+        agent_config_data = config.AGENT_CONFIG.get(agent_type_to_use)
+        if not agent_config_data:
+            raise ValueError(f"Unknown or unsupported agent type: '{agent_type_to_use}'")
+
+        command = [exec_command]
+        command.extend(agent_config_data.get("args", []))
+
+        task_file_rel_path = str(task_in_swap_path.relative_to(worktree_path))
+        task_file_arg_template = agent_config_data.get("task_file_arg_template")
+
+        if task_file_arg_template:
+            task_args = [
+                arg.format(task_file=task_file_rel_path)
+                for arg in task_file_arg_template
+            ]
+            command.extend(task_args)
+
+        command.extend(agent_args)
+
+        popen_kwargs = {
+            "cwd": str(worktree_path),
+            "stderr": subprocess.STDOUT,
+            "start_new_session": True,  # Detach from parent
+        }
+
+        # Apply timeout wrapper
+        timeout_seconds = config.AGENT_TIMEOUTS.get(agent_type_to_use)
+        if timeout_seconds:
+            timeout_command = ["timeout", str(timeout_seconds)] + command
+            command = timeout_command
+            logger.debug(
+                f"Applied timeout of {timeout_seconds} seconds to {agent_type_to_use} command"
             )
 
+        with open(log_file_path, "wb") as log_file:
+            popen_kwargs["stdout"] = log_file
+            logger.debug(f"Running agents process: {str(command)}, {str(popen_kwargs.copy())}")
+            if task_file_arg_template:
+                # Agent takes task file as command-line argument
+                process = subprocess.Popen(command, **popen_kwargs)
+            else:
+                # Agent takes task file via stdin
+                with open(task_in_swap_path, "r") as task_f:
+                    popen_kwargs["stdin"] = task_f
+                    process = subprocess.Popen(command, **popen_kwargs)
+
         pid_file.write_text(str(process.pid))
 
+        if auto_commit and agent_type_to_use != "aider":
+            logger.debug(f"Spawning auto-commit monitor for worktree {worktree_path}")
+            committer_cmd = [
+                sys.executable,
+                "-m",
+                "agro.committer",
+                str(process.pid),
+                str(worktree_path.resolve()),
+                task_path.name,
+                agent_type_to_use,
+            ]
+            committer_process = subprocess.Popen(committer_cmd)
+            logger.debug(f"Committer PID: {committer_process.pid}")
+
         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         logger.info(f"🏃 Agent for index {index} started successfully.")
         logger.info(f"   Worktree: {worktree_path.resolve()}")
         logger.info(f"   Task file: {task_path.resolve()}")
         logger.info(f"   Branch: {new_branch_name}")
+        logger.info(f"   Agent type: {agent_type_to_use}")
         logger.info(f"   Initial commit SHA: {initial_sha[:6]}")
         logger.info(f"   Start time: {current_time}")
         logger.debug(f"   PID: {process.pid} (saved to {pid_file.resolve()})")
diff --git a/tests/test_cli.py b/tests/test_cli.py
index a2a3f93..517a98d 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -39,9 +39,11 @@ def test_dispatch_exec_simple(mock_find, mock_find_recent, mock_exec_agent):
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_find.assert_called_once_with("task.md")
@@ -54,6 +56,8 @@ def test_dispatch_exec_simple(mock_find, mock_find_recent, mock_exec_agent):
         indices_str=None,
         num_trees=None,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -70,9 +74,11 @@ def test_dispatch_exec_with_num_trees_positional(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_find.assert_called_once_with("task.md")
@@ -85,6 +91,8 @@ def test_dispatch_exec_with_num_trees_positional(
         indices_str=None,
         num_trees=3,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -101,9 +109,11 @@ def test_dispatch_exec_with_exec_cmd_positional(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_find.assert_any_call("task.md")
@@ -117,6 +127,8 @@ def test_dispatch_exec_with_exec_cmd_positional(
         indices_str=None,
         num_trees=None,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -133,9 +145,11 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=True,
         no_env_overrides=True,
         verbose=2,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_exec_agent.assert_called_once_with(
@@ -147,6 +161,8 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional(
         indices_str=None,
         num_trees=3,
         show_cmd_output=True,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -163,9 +179,11 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=True,
         no_env_overrides=True,
         verbose=2,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_exec_agent.assert_called_once_with(
@@ -177,6 +195,8 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2(
         indices_str=None,
         num_trees=3,
         show_cmd_output=True,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -193,9 +213,11 @@ def test_dispatch_exec_with_num_trees_option(
         num_trees_opt=3,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_exec_agent.assert_called_once_with(
@@ -207,6 +229,8 @@ def test_dispatch_exec_with_num_trees_option(
         indices_str=None,
         num_trees=3,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -223,9 +247,11 @@ def test_dispatch_exec_with_tree_indices_option(
         num_trees_opt=None,
         tree_indices="1,2,3",
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_exec_agent.assert_called_once_with(
@@ -237,6 +263,8 @@ def test_dispatch_exec_with_tree_indices_option(
         indices_str="1,2,3",
         num_trees=None,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -253,9 +281,11 @@ def test_dispatch_exec_with_exec_cmd_option(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt="my-agent",
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_exec_agent.assert_called_once_with(
@@ -267,6 +297,8 @@ def test_dispatch_exec_with_exec_cmd_option(
         indices_str=None,
         num_trees=None,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -277,6 +309,7 @@ def test_dispatch_exec_num_trees_conflict_positional():
         num_trees_opt=3,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
@@ -292,6 +325,7 @@ def test_dispatch_exec_num_trees_conflict_indices():
         num_trees_opt=None,
         tree_indices="1,2",
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
@@ -310,6 +344,7 @@ def test_dispatch_exec_exec_cmd_conflict():
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt="my-agent",
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
@@ -328,6 +363,7 @@ def test_dispatch_exec_no_taskfile_found(mock_find_recent, mock_find):
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
@@ -349,9 +385,11 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_yes(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
+        no_auto_commit=False,
     )
     _dispatch_exec(args)
     mock_input.assert_called_once()
@@ -364,6 +402,8 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_yes(
         indices_str=None,
         num_trees=None,
         show_cmd_output=False,
+        agent_type=None,
+        auto_commit=True,
     )
 
 
@@ -380,6 +420,7 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_no(
         num_trees_opt=None,
         tree_indices=None,
         exec_cmd_opt=None,
+        agent_type_opt=None,
         fresh_env=False,
         no_env_overrides=False,
         verbose=0,
@@ -387,3 +428,142 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_no(
     _dispatch_exec(args)
     mock_input.assert_called_once()
     mock_exec_agent.assert_not_called()
+
+
+@patch("agro.cli.core.exec_agent")
+@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
+@patch("agro.cli.core.find_task_file")
+def test_dispatch_exec_with_agent_type_option(
+    mock_find, mock_find_recent, mock_exec_agent
+):
+    """Test exec with -a option for agent_type."""
+    mock_find.return_value = Path("task.md")
+    args = argparse.Namespace(
+        agent_args=["task.md"],
+        num_trees_opt=None,
+        tree_indices=None,
+        exec_cmd_opt=None,
+        agent_type_opt="gemini",
+        fresh_env=False,
+        no_env_overrides=False,
+        verbose=0,
+        no_auto_commit=False,
+    )
+    _dispatch_exec(args)
+    mock_exec_agent.assert_called_once_with(
+        task_file="task.md",
+        fresh_env=False,
+        no_overrides=False,
+        agent_args=[],
+        exec_cmd="gemini",
+        indices_str=None,
+        num_trees=None,
+        show_cmd_output=False,
+        agent_type="gemini",
+        auto_commit=True,
+    )
+
+
+@patch("agro.cli.core.exec_agent")
+@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
+@patch("agro.cli.core.find_task_file")
+def test_dispatch_exec_infer_agent_type_from_exec_cmd(
+    mock_find, mock_find_recent, mock_exec_agent
+):
+    """Test agent_type is inferred from exec_cmd."""
+    mock_find.return_value = Path("task.md")
+    with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}}):
+        args = argparse.Namespace(
+            agent_args=["task.md"],
+            num_trees_opt=None,
+            tree_indices=None,
+            exec_cmd_opt="my-gemini-agent",
+            agent_type_opt=None,
+            fresh_env=False,
+            no_env_overrides=False,
+            verbose=0,
+            no_auto_commit=False,
+        )
+        _dispatch_exec(args)
+        mock_exec_agent.assert_called_once_with(
+            task_file="task.md",
+            fresh_env=False,
+            no_overrides=False,
+            agent_args=[],
+            exec_cmd="my-gemini-agent",
+            indices_str=None,
+            num_trees=None,
+            show_cmd_output=False,
+            agent_type="gemini",
+            auto_commit=True,
+        )
+
+
+@patch("agro.cli.core.exec_agent")
+@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
+@patch("agro.cli.core.find_task_file")
+def test_dispatch_exec_infer_agent_type_from_positional_exec_cmd(
+    mock_find, mock_find_recent, mock_exec_agent
+):
+    """Test agent_type is inferred from positional exec_cmd."""
+    mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
+    with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}}):
+        args = argparse.Namespace(
+            agent_args=["task.md", "my-gemini-agent"],
+            num_trees_opt=None,
+            tree_indices=None,
+            exec_cmd_opt=None,
+            agent_type_opt=None,
+            fresh_env=False,
+            no_env_overrides=False,
+            verbose=0,
+            no_auto_commit=False,
+        )
+        _dispatch_exec(args)
+        mock_exec_agent.assert_called_once_with(
+            task_file="task.md",
+            fresh_env=False,
+            no_overrides=False,
+            agent_args=[],
+            exec_cmd="my-gemini-agent",
+            indices_str=None,
+            num_trees=None,
+            show_cmd_output=False,
+            agent_type="gemini",
+            auto_commit=True,
+        )
+
+
+@patch("agro.cli.core.exec_agent")
+@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
+@patch("agro.cli.core.find_task_file")
+def test_dispatch_exec_no_inference_when_both_provided(
+    mock_find, mock_find_recent, mock_exec_agent
+):
+    """Test no inference occurs when both agent_type and exec_cmd are provided."""
+    mock_find.return_value = Path("task.md")
+    with patch("agro.cli.core.config.AGENT_CONFIG", {"gemini": {}, "aider": {}}):
+        args = argparse.Namespace(
+            agent_args=["task.md"],
+            num_trees_opt=None,
+            tree_indices=None,
+            exec_cmd_opt="my-gemini-agent",
+            agent_type_opt="aider",
+            fresh_env=False,
+            no_env_overrides=False,
+            verbose=0,
+            no_auto_commit=False,
+        )
+        _dispatch_exec(args)
+        mock_exec_agent.assert_called_once_with(
+            task_file="task.md",
+            fresh_env=False,
+            no_overrides=False,
+            agent_args=[],
+            exec_cmd="my-gemini-agent",
+            indices_str=None,
+            num_trees=None,
+            show_cmd_output=False,
+            agent_type="aider",
+            auto_commit=True,
+        )
diff --git a/uv.lock b/uv.lock
index 4c2cfa4..4e988c5 100644
--- a/uv.lock
+++ b/uv.lock
@@ -4,13 +4,13 @@ requires-python = ">=3.9"
 
 [[package]]
 name = "agro"
-version = "0.1.4"
+version = "0.1.5"
 source = { editable = "." }
 dependencies = [
     { name = "pyyaml" },
 ]
 
-[package.dev-dependencies]
+[package.optional-dependencies]
 dev = [
     { name = "build" },
     { name = "twine" },
@@ -20,14 +20,13 @@ test = [
 ]
 
 [package.metadata]
-requires-dist = [{ name = "pyyaml" }]
-
-[package.metadata.requires-dev]
-dev = [
-    { name = "build", specifier = ">=1.2.2.post1" },
-    { name = "twine", specifier = ">=6.1.0" },
+requires-dist = [
+    { name = "build", marker = "extra == 'dev'", specifier = ">=1.2.2.post1" },
+    { name = "pytest", marker = "extra == 'test'", specifier = ">=8.4.1" },
+    { name = "pyyaml" },
+    { name = "twine", marker = "extra == 'dev'", specifier = ">=6.1.0" },
 ]
-test = [{ name = "pytest", specifier = ">=8.4.1" }]
+provides-extras = ["dev", "test"]
 
 [[package]]
 name = "backports-tarfile"
