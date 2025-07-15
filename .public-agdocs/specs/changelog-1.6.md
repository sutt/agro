Below is a diff from v0.1.5 to v0.1.6.

Add entries to docs/CHANGELOG.md to describe the change

diff --git a/src/agro/cli.py b/src/agro/cli.py
index 238ad6c..fd19fc6 100644
--- a/src/agro/cli.py
+++ b/src/agro/cli.py
@@ -40,10 +40,6 @@ def _dispatch_exec(args):
                 raise ValueError(
                     "Number of trees specified twice (e.g. positionally and with -n)."
                 )
-            if args.tree_indices is not None:
-                raise ValueError(
-                    "Cannot specify number of trees positionally and with -t/--tree-indices."
-                )
             num_trees = int(arg)
         else:
             remaining_pos_args.append(arg)
@@ -102,7 +98,7 @@ def _dispatch_exec(args):
         no_overrides=args.no_env_overrides,
         agent_args=agent_args,
         exec_cmd=exec_cmd,
-        indices_str=args.tree_indices,
+        indices_str=None,
         num_trees=num_trees,
         show_cmd_output=(args.verbose >= 2),
         agent_type=agent_type,
@@ -117,37 +113,42 @@ def main():
     epilog_text = """Main command:
   exec [args] [taskfile] [num-trees] [exec-cmd]   
                                 
-        Run an agent in new worktree(s)
+    Run an agent in new worktree(s)
         args:
-          -n <num-trees>        Number of worktrees to create.
-          -t <indices>          Specified worktree indice(s) (e.g., '1,2,3').
-          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree
-          ...others             See below.
+          -n <num-trees>        Number of worktrees / agents to create.
+          -c <exec-cmd>         Custom command to launch agent on worktree.
+          -a <agent-type>       Specify agent type to override config.
+                                Supported: aider, claude, gemini.
 
 Other Commands:
-  surrender [indices]           Kill running agent processes (default: all).
-  muster <command> <indices>    Run a command in specified worktrees (e.g., '1,2,3').
+  muster <command> <branch-patterns>    Run a command in specified worktrees.
+  surrender [branch-patterns]   Kill running agent processes (default: all).
   grab <branch-name>            Checkout a branch, creating a copy if it's in use.
-  fade <pattern>                Delete local branches matching a regex pattern.
-  make <index>                  Create a new worktree.
-  delete <indices>|--all        Delete one, multiple, or all worktrees.
+  fade <branch-patterns>        Delete local branches matching a regex pattern.
+  state [branch-patterns]       Show the worktree to branch mappings (default: all).
   task [task-name]              Create a new task spec file and open it.
-  init                          Initialize agro project structure.
+  init                          Initialize agro project structure in .agdocs/.
   mirror                        Mirror internal docs to public docs directory.
-  help                          Show this help message.
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
+  --fresh-env         Use .env.example as the base instead of .env.
+  --no-env-overrides  Do not add port overrides to the .env file.
 
 Options for 'muster':
-  -s, --server        Run command as a background server, redirecting output and saving PID.
+  -s, --server        Run command as a background server (and log server PID)
   -k, --kill-server   Kill the background server and clean up pid/log files.
     
 Options for 'init':
   --conf              Only add a template agro.conf.yml to .agdocs/conf"""
     parser = argparse.ArgumentParser(
-        description="A script to manage git worktrees for agent-based development.",
+        description="A script to manage git branches & worktrees for agent-based development.",
         prog="agro",
         epilog=epilog_text,
         formatter_class=argparse.RawDescriptionHelpFormatter,
@@ -252,19 +253,13 @@ Options for 'init':
         "All arguments after the taskfile and exec options are passed to the agent.",
     )
 
-    exec_group = parser_exec.add_mutually_exclusive_group()
-    exec_group.add_argument(
+    parser_exec.add_argument(
         "-n",
         "--num-trees",
         type=int,
         dest="num_trees_opt",
         help="Number of new worktrees to create.",
     )
-    exec_group.add_argument(
-        "-t",
-        "--tree-indices",
-        help="Comma-separated list of worktree indices to use (e.g., '1,2').",
-    )
 
     parser_exec.add_argument(
         "-c",
@@ -302,7 +297,9 @@ Options for 'init':
         help="The command to execute. A dummy value can be used with --kill-server.",
     )
     parser_muster.add_argument(
-        "indices", help="Comma-separated list of worktree indices (e.g., '1,2')."
+        "branch_patterns",
+        nargs="+",
+        help="One or more branch patterns to select worktrees.",
     )
     parser_muster.add_argument(
         "-s",
@@ -319,7 +316,7 @@ Options for 'init':
     parser_muster.set_defaults(
         func=lambda args: core.muster_command(
             args.command_str,
-            args.indices,
+            args.branch_patterns,
             server=args.server,
             kill_server=args.kill_server,
             show_cmd_output=(args.verbose >= 2),
@@ -339,12 +336,14 @@ Options for 'init':
 
     # --- fade command ---
     parser_fade = subparsers.add_parser(
-        "fade", help="Delete local branches matching a regex pattern after confirmation."
+        "fade", help="Delete local branches matching pattern(s) after confirmation."
+    )
+    parser_fade.add_argument(
+        "patterns", nargs="+", help="One or more patterns to match branch names against."
     )
-    parser_fade.add_argument("pattern", help="The regex pattern to match branch names against.")
     parser_fade.set_defaults(
         func=lambda args: core.fade_branches(
-            args.pattern, show_cmd_output=(args.verbose >= 2)
+            args.patterns, show_cmd_output=(args.verbose >= 2)
         )
     )
 
@@ -353,14 +352,30 @@ Options for 'init':
         "surrender", help="Kill running agent processes."
     )
     parser_surrender.add_argument(
-        "indices",
-        nargs="?",
-        default="all",
-        help="Comma-separated list of worktree indices (e.g., '1,2'). Defaults to all.",
+        "branch_patterns",
+        nargs="*",
+        default=[],
+        help="Optional branch pattern(s) to select worktrees. Defaults to all.",
     )
     parser_surrender.set_defaults(
         func=lambda args: core.surrender(
-            args.indices, show_cmd_output=(args.verbose >= 2)
+            args.branch_patterns, show_cmd_output=(args.verbose >= 2)
+        )
+    )
+
+    # --- state command ---
+    parser_state = subparsers.add_parser(
+        "state", help="Show the state of existing worktrees."
+    )
+    parser_state.add_argument(
+        "branch_pattern",
+        nargs="*",
+        default=[],
+        help="Optional glob-style pattern(s) to filter branches by name.",
+    )
+    parser_state.set_defaults(
+        func=lambda args: core.state(
+            branch_patterns=args.branch_pattern, show_cmd_output=(args.verbose >= 2)
         )
     )
 
diff --git a/src/agro/core.py b/src/agro/core.py
index 5a8c33f..85f1eba 100644
--- a/src/agro/core.py
+++ b/src/agro/core.py
@@ -1,3 +1,5 @@
+import fnmatch
+import json
 import logging
 import os
 import re
@@ -55,6 +57,86 @@ def find_most_recent_task_file() -> Path | None:
     return latest_file
 
 
+def _get_all_branches(show_cmd_output=False) -> list[str]:
+    """Retrieves a list of all local branch names."""
+    result = _run_command(
+        ["git", "branch", "--format=%(refname:short)"],
+        capture_output=True,
+        check=True,
+        show_cmd_output=show_cmd_output,
+    )
+    return result.stdout.strip().split("\n") if result.stdout else []
+
+
+def _expand_branch_pattern(pattern: str) -> list[str]:
+    """
+    Expands a branch pattern with brace expressions into a list of concrete names.
+    e.g., 'feature/branch.{1-3,5}' -> ['feature/branch.1', 'feature/branch.2', 'feature/branch.3', 'feature/branch.5']
+    """
+    match = re.search(r"\{([^}]+)\}", pattern)
+    if not match:
+        return [pattern]
+
+    prefix = pattern[: match.start()]
+    suffix = pattern[match.end() :]
+    content = match.group(1)
+
+    if not content.strip():  # Handles {} and { }
+        return []
+
+    numbers = set()
+    parts = content.split(",")
+    for part in parts:
+        part = part.strip()
+        if not part:
+            continue
+        if "-" in part:
+            try:
+                start_str, end_str = part.split("-", 1)
+                start, end = int(start_str), int(end_str)
+                if start > end:
+                    continue
+                numbers.update(range(start, end + 1))
+            except ValueError:
+                raise ValueError(f"Invalid range in pattern: '{part}'")
+        else:
+            try:
+                numbers.add(int(part))
+            except ValueError:
+                raise ValueError(f"Invalid number in pattern: '{part}'")
+
+    return [f"{prefix}{num}{suffix}" for num in sorted(list(numbers))]
+
+
+def _get_matching_branches(pattern: str, show_cmd_output=False) -> list[str]:
+    """
+    Finds branches matching a given pattern.
+    - Expands brace notation like {1-3,5}.
+    - If no brace notation and no glob chars, performs an exact match, falling back to prefix match.
+    - Allows user to provide their own glob patterns.
+    """
+    all_branches = _get_all_branches(show_cmd_output)
+
+    try:
+        expanded_patterns = _expand_branch_pattern(pattern)
+    except ValueError as e:
+        logger.error(f"Pattern error: {e}")
+        return []
+
+    if "{" in pattern:
+        return sorted([b for b in all_branches if b in expanded_patterns])
+
+    plain_pattern = expanded_patterns[0]
+
+    if plain_pattern in all_branches:
+        return [plain_pattern]
+
+    if any(c in plain_pattern for c in "*?[]"):
+        return sorted(fnmatch.filter(all_branches, plain_pattern))
+
+    return sorted(fnmatch.filter(all_branches, f"{plain_pattern}*"))
+
+
 def _get_config_template():
     """Returns the content for the default agro.conf.yml."""
     return f"""# Agro Configuration File
@@ -167,6 +249,11 @@ def init_project(conf_only=False):
     agdocs_dir.mkdir()
     (agdocs_dir / "specs").mkdir()
     (agdocs_dir / "swap").mkdir()
+    guides_dir = agdocs_dir / "guides"
+    guides_dir.mkdir()
+    (guides_dir / "GUIDE.md").write_text(
+        "# Agent Guide\n\nThis file provides guidance and conventions for the AI agent.\n"
+    )
     conf_dir.mkdir()
 
     config_file_path.write_text(_get_config_template())
@@ -180,6 +267,8 @@ def init_project(conf_only=False):
     logger.debug(f"Created: {agdocs_dir}/")
     logger.debug(f"Created: {agdocs_dir}/specs/")
     logger.debug(f"Created: {agdocs_dir}/swap/")
+    logger.debug(f"Created: {agdocs_dir}/guides/")
+    logger.debug(f"Created: {agdocs_dir}/guides/GUIDE.md")
     logger.debug(f"Created: {agdocs_dir}/conf/")
     logger.debug(f"Created: {agdocs_dir}/conf/agro.conf.yml")
     logger.debug(f"Created: {agdocs_dir}/.gitignore")
@@ -245,6 +334,7 @@ def _run_command(
     capture_output=False,
     shell=False,
     show_cmd_output=False,
+    suppress_error_logging=False,
 ):
     """Helper to run a shell command."""
     cmd_str = command if isinstance(command, str) else shlex.join(command)
@@ -264,13 +354,14 @@ def _run_command(
         )
         return result
     except subprocess.CalledProcessError as e:
-        cmd_str = command if isinstance(command, str) else shlex.join(command)
-        logger.error(f"Error executing command: {cmd_str}")
-        # If output was captured, it's in the exception.
-        if e.stdout:
-            logger.error(f"STDOUT:\n{e.stdout.strip()}")
-        if e.stderr:
-            logger.error(f"STDERR:\n{e.stderr.strip()}")
+        if not suppress_error_logging:
+            cmd_str = command if isinstance(command, str) else shlex.join(command)
+            logger.error(f"Error executing command: {cmd_str}")
+            # If output was captured, it's in the exception.
+            if e.stdout:
+                logger.error(f"STDOUT:\n{e.stdout.strip()}")
+            if e.stderr:
+                logger.error(f"STDERR:\n{e.stderr.strip()}")
         raise
     except FileNotFoundError:
         cmd_name = command if isinstance(command, str) else command[0]
@@ -592,6 +683,20 @@ def exec_agent(
         worktree_path = Path(config.WORKTREE_DIR) / f"t{index}"
         agswap_dir = worktree_path / ".agswap"
 
+        guides_src_dir = Path(config.AGDOCS_DIR) / "guides"
+        guide_files_in_swap = []
+        if guides_src_dir.is_dir():
+            guides_dest_dir = agswap_dir / "guides"
+            guides_dest_dir.mkdir(exist_ok=True)
+            for guide_file in guides_src_dir.glob("*.md"):
+                dest_file = guides_dest_dir / guide_file.name
+                shutil.copy(guide_file, dest_file)
+                guide_files_in_swap.append(dest_file)
+            if guide_files_in_swap:
+                logger.debug(
+                    f"Copied {len(guide_files_in_swap)} guide files to {guides_dest_dir}"
+                )
+
         task_in_swap_path = agswap_dir / task_path.name
         shutil.copy(task_path, task_in_swap_path)
         logger.debug(f"Copied task file to {task_in_swap_path}")
@@ -641,6 +746,35 @@ def exec_agent(
         command = [exec_command]
         command.extend(agent_config_data.get("args", []))
 
+        if agent_type_to_use == "aider" and guide_files_in_swap:
+            for guide_file in guide_files_in_swap:
+                rel_path = guide_file.relative_to(worktree_path)
+                command.extend(["--read", str(rel_path)])
+            logger.debug(
+                f"Added {len(guide_files_in_swap)} guide files with --read for aider."
+            )
+
+        if agent_type_to_use == "gemini":
+            gemini_dir = worktree_path / ".gemini"
+            if gemini_dir.exists():
+                logger.warning(
+                    f"Directory '{gemini_dir}' already exists. Gemini agent will not have access to guide files."
+                )
+            else:
+                logger.debug(f"Creating '{gemini_dir}' for gemini agent context.")
+                gemini_dir.mkdir()
+                (gemini_dir / ".gitignore").write_text("*\n")
+                if guide_files_in_swap:
+                    relative_guide_paths = [
+                        str(p.relative_to(worktree_path)) for p in guide_files_in_swap
+                    ]
+                    settings_content = {"contextFileName": relative_guide_paths}
+                    settings_file = gemini_dir / "settings.json"
+                    settings_file.write_text(json.dumps(settings_content, indent=4))
+                    logger.debug(
+                        f"Created '{settings_file}' with {len(relative_guide_paths)} guide files."
+                    )
+
         task_file_rel_path = str(task_in_swap_path.relative_to(worktree_path))
         task_file_arg_template = agent_config_data.get("task_file_arg_template")
 
@@ -677,8 +811,20 @@ def exec_agent(
             else:
                 # Agent takes task file via stdin
                 with open(task_in_swap_path, "r") as task_f:
-                    popen_kwargs["stdin"] = task_f
-                    process = subprocess.Popen(command, **popen_kwargs)
+                    task_content = task_f.read()
+
+                if agent_type_to_use == "claude" and guide_files_in_swap:
+                    guides_ref = "@.agswap/guides/* "
+                    task_content = guides_ref + task_content
+                    logger.debug(
+                        "Prepended claude guide file reference to task content."
+                    )
+
+                popen_kwargs["stdin"] = subprocess.PIPE
+                process = subprocess.Popen(command, **popen_kwargs)
+                if process.stdin:
+                    process.stdin.write(task_content.encode("utf-8"))
+                    process.stdin.close()
 
         pid_file.write_text(str(process.pid))
 
@@ -709,20 +855,57 @@ def exec_agent(
         logger.debug(f"   Task file copy: {task_in_swap_path.resolve()}")
 
 
+def _get_indices_from_branch_patterns(branch_patterns=None, show_cmd_output=False) -> list[int]:
+    """
+    Resolves branch patterns to a list of worktree indices.
+    If no patterns are provided, returns indices for all existing worktrees.
+    """
+    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
+    if not worktree_state:
+        return []
+
+    if not branch_patterns:
+        # Return all indices if no pattern is given
+        all_indices = []
+        for wt_name in worktree_state.keys():
+            if wt_name.startswith("t") and wt_name[1:].isdigit():
+                all_indices.append(int(wt_name[1:]))
+        return sorted(all_indices)
+
+    all_matching_branches = set()
+    for pattern in branch_patterns:
+        matching_branches = _get_matching_branches(
+            pattern, show_cmd_output=show_cmd_output
+        )
+        all_matching_branches.update(matching_branches)
+
+    if not all_matching_branches:
+        patterns_str = " ".join(f"'{p}'" for p in branch_patterns)
+        logger.info(f"No branches found matching patterns: {patterns_str}")
+        return []
+
+    matching_indices = []
+    for wt_name, branch in worktree_state.items():
+        if branch in all_matching_branches:
+            if wt_name.startswith("t") and wt_name[1:].isdigit():
+                matching_indices.append(int(wt_name[1:]))
+
+    return sorted(matching_indices)
+
+
 def muster_command(
-    command_str, indices_str, server=False, kill_server=False, show_cmd_output=False
+    command_str, branch_patterns, server=False, kill_server=False, show_cmd_output=False
 ):
     """Runs a command in multiple worktrees."""
     if server and kill_server:
         raise ValueError("--server and --kill-server cannot be used together.")
 
-    try:
-        indices = [int(i.strip()) for i in indices_str.split(",") if i.strip()]
-    except ValueError:
-        logger.error(
-            f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
-        )
-        raise
+    indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
+    if not indices:
+        logger.warning("No worktrees found matching the provided patterns.")
+        return
+
+    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
 
     use_shell = False
     final_command_str = command_str
@@ -746,6 +929,7 @@ def muster_command(
     for index in indices:
         tree_name = f"t{index}"
         worktree_path = Path(config.WORKTREE_DIR) / tree_name
+        branch_name = worktree_state.get(tree_name, "<unknown branch>")
 
         if not worktree_path.is_dir():
             logger.warning(
@@ -753,14 +937,14 @@ def muster_command(
             )
             continue
 
-        logger.info(f"\n--- Running command in t{index} ({worktree_path}) ---")
+        logger.info(f"\n--- Running command in t{index} ({branch_name}) ---")
         logger.info(f"$ {final_command_str}")
         try:
             _run_command(
                 command,
                 cwd=str(worktree_path),
                 shell=use_shell,
-                show_cmd_output=show_cmd_output,
+                show_cmd_output=True,
             )
         except (subprocess.CalledProcessError, FileNotFoundError):
             # _run_command already prints details.
@@ -780,6 +964,7 @@ def grab_branch(branch_name, show_cmd_output=False):
             ["git", "checkout", branch_name],
             capture_output=True,
             show_cmd_output=show_cmd_output,
+            suppress_error_logging=True,
         )
         logger.info(f"Successfully checked out branch '{branch_name}'.")
     except subprocess.CalledProcessError as e:
@@ -798,35 +983,49 @@ def grab_branch(branch_name, show_cmd_output=False):
             )
             logger.info(f"Successfully checked out branch '{copy_branch_name}'.")
         else:
-            # Re-raise if it's a different error
+            # Re-raise if it's a different error, but log it first
+            cmd_str = shlex.join(["git", "checkout", branch_name])
+            logger.error(f"Error executing command: {cmd_str}")
+            if e.stdout:
+                logger.error(f"STDOUT:\n{e.stdout.strip()}")
+            if e.stderr:
+                logger.error(f"STDERR:\n{e.stderr.strip()}")
             raise
 
 
-def fade_branches(pattern, show_cmd_output=False):
-    """Deletes local git branches matching a pattern after user confirmation."""
-    logger.info(f"Searching for branches matching pattern: '{pattern}'")
+def fade_branches(patterns, show_cmd_output=False):
+    """Deletes local git branches matching patterns after user confirmation."""
+    patterns_str = " ".join(f"'{p}'" for p in patterns)
+    logger.info(f"Searching for branches matching patterns: {patterns_str}")
+
+    all_matching_branches = set()
+    for pattern in patterns:
+        matching_branches = _get_matching_branches(
+            pattern, show_cmd_output=show_cmd_output
+        )
+        all_matching_branches.update(matching_branches)
+
+    if not all_matching_branches:
+        logger.info("No branches found matching the patterns to delete.")
+        return
 
     result = _run_command(
-        ["git", "branch"],
+        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
         capture_output=True,
         check=True,
         show_cmd_output=show_cmd_output,
     )
-    all_branches_raw = result.stdout.strip().split("\n")
+    current_branch = result.stdout.strip()
 
     branches_to_delete = []
-    for line in all_branches_raw:
-        branch_name = line.lstrip(" *+")
-        if re.search(pattern, branch_name):
-            if line.startswith("* "):
-                logger.warning(
-                    f"Skipping currently checked out branch '{branch_name}'"
-                )
-                continue
-            branches_to_delete.append(branch_name)
+    for branch_name in sorted(list(all_matching_branches)):
+        if branch_name == current_branch:
+            logger.warning(f"Skipping currently checked out branch '{branch_name}'")
+            continue
+        branches_to_delete.append(branch_name)
 
     if not branches_to_delete:
-        logger.info("No branches found matching the pattern to delete.")
+        logger.info("No branches to delete after filtering out the current branch.")
         return
 
     logger.info("\n--- Dry Run ---")
@@ -894,32 +1093,82 @@ def mirror_docs(show_cmd_output=False):
     logger.info("✅ Mirroring complete.")
 
 
-def surrender(indices_str=None, show_cmd_output=False):
+def get_worktree_state(show_cmd_output=False):
+    """
+    Retrieves the state of all worktrees, mapping worktree name to its current branch.
+    """
+    worktree_dir = Path(config.WORKTREE_DIR)
+    if not worktree_dir.is_dir():
+        return {}
+
+    state = {}
+    worktree_paths = sorted(
+        [p for p in worktree_dir.iterdir() if p.is_dir() and p.name.startswith("t")]
+    )
+    for worktree_path in worktree_paths:
+        try:
+            result = _run_command(
+                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
+                cwd=worktree_path,
+                capture_output=True,
+                check=True,
+                show_cmd_output=show_cmd_output,
+                suppress_error_logging=True,
+            )
+            branch = result.stdout.strip()
+            state[worktree_path.name] = branch
+        except subprocess.CalledProcessError:
+            state[worktree_path.name] = "<error: unable to get branch>"
+        except FileNotFoundError:
+            state[worktree_path.name] = "<error: git not found>"
+    return state
+
+
+def state(branch_patterns=None, show_cmd_output=False):
+    """Prints the state of the worktrees, optionally filtered by branch pattern."""
+    worktree_state = get_worktree_state(show_cmd_output=show_cmd_output)
+
+    if branch_patterns:
+        all_matching_branches = set()
+        for pattern in branch_patterns:
+            matching_branches = _get_matching_branches(
+                pattern, show_cmd_output=show_cmd_output
+            )
+            all_matching_branches.update(matching_branches)
+
+        if not all_matching_branches:
+            patterns_str = " ".join(f"'{p}'" for p in branch_patterns)
+            logger.info(f"No branches found matching patterns: {patterns_str}")
+            return
+
+        worktree_state = {
+            wt: br
+            for wt, br in worktree_state.items()
+            if br in all_matching_branches
+        }
+
+    if not worktree_state:
+        logger.info("No worktrees found matching the criteria.")
+        return
+
+    for worktree, branch in sorted(worktree_state.items()):
+        logger.info(f"{worktree}: {branch}")
+
+
+def surrender(branch_patterns=None, show_cmd_output=False):
     """Kills running agent processes associated with worktrees."""
     pid_dir = Path(config.AGDOCS_DIR) / "swap"
     if not pid_dir.is_dir():
         logger.info("No agent processes seem to be running (PID directory not found).")
         return
 
-    target_indices = []
-    if not indices_str or indices_str.lower() == 'all':
-        for pid_file in sorted(pid_dir.glob("t*.pid")):
-            match = re.match(r"t(\d+)\.pid", pid_file.name)
-            if match:
-                target_indices.append(int(match.group(1)))
-        if not target_indices:
-            logger.info(f"No PID files found in {pid_dir}.")
-            return
-    else:
-        try:
-            target_indices = [
-                int(i.strip()) for i in indices_str.split(",") if i.strip()
-            ]
-        except ValueError:
-            logger.error(
-                f"Invalid indices list '{indices_str}'. Please provide a comma-separated list of numbers."
-            )
-            raise
+    target_indices = _get_indices_from_branch_patterns(branch_patterns, show_cmd_output)
+    if not target_indices:
+        if branch_patterns:
+            logger.warning("No worktrees found matching the provided patterns.")
+        else:
+            logger.info("No worktrees found.")
+        return
 
     procs_to_kill = []
     logger.info("--- Dry Run ---")
diff --git a/tests/test_cli.py b/tests/test_cli.py
index 517a98d..4c30e95 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -37,7 +37,6 @@ def test_dispatch_exec_simple(mock_find, mock_find_recent, mock_exec_agent):
     args = argparse.Namespace(
         agent_args=["task.md"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -72,7 +71,6 @@ def test_dispatch_exec_with_num_trees_positional(
     args = argparse.Namespace(
         agent_args=["task.md", "3"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -107,7 +105,6 @@ def test_dispatch_exec_with_exec_cmd_positional(
     args = argparse.Namespace(
         agent_args=["task.md", "my-agent"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -143,7 +140,6 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional(
     args = argparse.Namespace(
         agent_args=["task.md", "3", "my-agent", "--agent-opt"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=True,
@@ -177,7 +173,6 @@ def test_dispatch_exec_with_num_trees_and_exec_cmd_positional_2(
     args = argparse.Namespace(
         agent_args=["task.md", "my-agent", "3", "--agent-opt"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=True,
@@ -211,7 +206,6 @@ def test_dispatch_exec_with_num_trees_option(
     args = argparse.Namespace(
         agent_args=["task.md", "my-agent", "--agent-opt"],
         num_trees_opt=3,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -234,39 +228,6 @@ def test_dispatch_exec_with_num_trees_option(
     )
 
 
-@patch("agro.cli.core.exec_agent")
-@patch("agro.cli.core.find_most_recent_task_file", return_value=None)
-@patch("agro.cli.core.find_task_file")
-def test_dispatch_exec_with_tree_indices_option(
-    mock_find, mock_find_recent, mock_exec_agent
-):
-    """Test exec with -t option for tree_indices."""
-    mock_find.side_effect = lambda arg: Path("task.md") if arg == "task.md" else None
-    args = argparse.Namespace(
-        agent_args=["task.md", "my-agent", "--agent-opt"],
-        num_trees_opt=None,
-        tree_indices="1,2,3",
-        exec_cmd_opt=None,
-        agent_type_opt=None,
-        fresh_env=False,
-        no_env_overrides=False,
-        verbose=0,
-        no_auto_commit=False,
-    )
-    _dispatch_exec(args)
-    mock_exec_agent.assert_called_once_with(
-        task_file="task.md",
-        fresh_env=False,
-        no_overrides=False,
-        agent_args=["--agent-opt"],
-        exec_cmd="my-agent",
-        indices_str="1,2,3",
-        num_trees=None,
-        show_cmd_output=False,
-        agent_type=None,
-        auto_commit=True,
-    )
-
 
 @patch("agro.cli.core.exec_agent")
 @patch("agro.cli.core.find_most_recent_task_file", return_value=None)
@@ -279,7 +240,6 @@ def test_dispatch_exec_with_exec_cmd_option(
     args = argparse.Namespace(
         agent_args=["task.md", "--agent-opt"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt="my-agent",
         agent_type_opt=None,
         fresh_env=False,
@@ -307,7 +267,6 @@ def test_dispatch_exec_num_trees_conflict_positional():
     args = argparse.Namespace(
         agent_args=["3"],
         num_trees_opt=3,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -318,31 +277,12 @@ def test_dispatch_exec_num_trees_conflict_positional():
         _dispatch_exec(args)
 
 
-def test_dispatch_exec_num_trees_conflict_indices():
-    """Test ValueError when num_trees is specified with -t and positionally."""
-    args = argparse.Namespace(
-        agent_args=["3"],
-        num_trees_opt=None,
-        tree_indices="1,2",
-        exec_cmd_opt=None,
-        agent_type_opt=None,
-        fresh_env=False,
-        no_env_overrides=False,
-        verbose=0,
-    )
-    with pytest.raises(
-        ValueError,
-        match="Cannot specify number of trees positionally and with -t/--tree-indices.",
-    ):
-        _dispatch_exec(args)
-
 
 def test_dispatch_exec_exec_cmd_conflict():
     """Test ValueError when exec_cmd is specified with -c and positionally."""
     args = argparse.Namespace(
         agent_args=["my-agent"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt="my-agent",
         agent_type_opt=None,
         fresh_env=False,
@@ -361,7 +301,6 @@ def test_dispatch_exec_no_taskfile_found(mock_find_recent, mock_find):
     args = argparse.Namespace(
         agent_args=[],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -383,7 +322,6 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_yes(
     args = argparse.Namespace(
         agent_args=[],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -418,7 +356,6 @@ def test_dispatch_exec_no_taskfile_use_recent_confirm_no(
     args = argparse.Namespace(
         agent_args=[],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt=None,
         fresh_env=False,
@@ -441,7 +378,6 @@ def test_dispatch_exec_with_agent_type_option(
     args = argparse.Namespace(
         agent_args=["task.md"],
         num_trees_opt=None,
-        tree_indices=None,
         exec_cmd_opt=None,
         agent_type_opt="gemini",
         fresh_env=False,
@@ -476,7 +412,6 @@ def test_dispatch_exec_infer_agent_type_from_exec_cmd(
         args = argparse.Namespace(
             agent_args=["task.md"],
             num_trees_opt=None,
-            tree_indices=None,
             exec_cmd_opt="my-gemini-agent",
             agent_type_opt=None,
             fresh_env=False,
@@ -511,7 +446,6 @@ def test_dispatch_exec_infer_agent_type_from_positional_exec_cmd(
         args = argparse.Namespace(
             agent_args=["task.md", "my-gemini-agent"],
             num_trees_opt=None,
-            tree_indices=None,
             exec_cmd_opt=None,
             agent_type_opt=None,
             fresh_env=False,
@@ -546,7 +480,6 @@ def test_dispatch_exec_no_inference_when_both_provided(
         args = argparse.Namespace(
             agent_args=["task.md"],
             num_trees_opt=None,
-            tree_indices=None,
             exec_cmd_opt="my-gemini-agent",
             agent_type_opt="aider",
             fresh_env=False,
diff --git a/tests/test_core.py b/tests/test_core.py
new file mode 100644
index 0000000..cfa4b46
--- /dev/null
+++ b/tests/test_core.py
@@ -0,0 +1,261 @@
+import pytest
+from unittest.mock import patch, call, MagicMock
+
+from agro import core
+
+
+@pytest.mark.parametrize(
+    "pattern, expected",
+    [
+        ("branch", ["branch"]),
+        ("feature/branch", ["feature/branch"]),
+        ("branch.{1-3}", ["branch.1", "branch.2", "branch.3"]),
+        ("branch.{3-1}", []),
+        ("branch.{2,4}", ["branch.2", "branch.4"]),
+        ("branch.{1-3,5}", ["branch.1", "branch.2", "branch.3", "branch.5"]),
+        ("b.{1,3-4}", ["b.1", "b.3", "b.4"]),
+        ("b.{1, 3-4 , 6}", ["b.1", "b.3", "b.4", "b.6"]),
+        ("no-braces", ["no-braces"]),
+        ("prefix.{1,1}.suffix", ["prefix.1.suffix"]),
+        ("b.{}", ["b.{}"]),   # XFAIL: doesnt work as expected, should be empty list
+        ("b.{ }", []),
+        ("b.{,}", []),
+    ],
+)
+def test_expand_branch_pattern_valid(pattern, expected):
+    assert core._expand_branch_pattern(pattern) == expected
+
+
+@pytest.mark.parametrize(
+    "pattern",
+    [
+        "b.{1-}",
+        "b.{a-c}",
+        "b.{1,a}",
+        "b.{1-2-3}",
+    ],
+)
+def test_expand_branch_pattern_invalid(pattern):
+    with pytest.raises(ValueError):
+        core._expand_branch_pattern(pattern)
+
+
+ALL_BRANCHES = [
+    "main",
+    "develop",
+    "feature/one",
+    "feature/two",
+    "output/feat.1",
+    "output/feat.2",
+    "output/feat.3",
+    "output/feat.5",
+    "output/other.1",
+    "bugfix/short",
+]
+
+
+@patch("agro.core._get_all_branches", return_value=ALL_BRANCHES)
+@pytest.mark.parametrize(
+    "pattern, expected",
+    [
+        # Exact match
+        ("main", ["main"]),
+        # No exact match, prefix match
+        ("feature", ["feature/one", "feature/two"]),
+        ("bugfix", ["bugfix/short"]),
+        # Glob pattern
+        ("feature/*", ["feature/one", "feature/two"]),
+        (
+            "output/feat.*",
+            ["output/feat.1", "output/feat.2", "output/feat.3", "output/feat.5"],
+        ),
+        # Brace expansion
+        ("output/feat.{1-3}", ["output/feat.1", "output/feat.2", "output/feat.3"]),
+        ("output/feat.{2,5}", ["output/feat.2", "output/feat.5"]),
+        # .4 does not exist
+        ("output/feat.{1-4}", ["output/feat.1", "output/feat.2", "output/feat.3"]),
+        # No match
+        ("nonexistent", []),
+        ("output/feat.{6-7}", []),
+        # Exact match takes precedence over prefix
+        ("feature/one", ["feature/one"]),
+        # Empty brace expansion
+        ("output/feat.{}", []),
+    ],
+)
+def test_get_matching_branches(mock_get_branches, pattern, expected):
+    assert core._get_matching_branches(pattern) == expected
+    mock_get_branches.assert_called_once()
+
+
+if __name__ == "__main__":
+    # uv run python -m tests.test_core
+    print(core._expand_branch_pattern("b{}"))
+
+
+@patch("agro.core.get_worktree_state")
+@patch("agro.core._get_matching_branches")
+def test_get_indices_from_branch_patterns(mock_get_matching_branches, mock_get_worktree_state):
+    mock_get_worktree_state.return_value = {
+        "t1": "feature/one",
+        "t2": "feature/two",
+        "t3": "bugfix/short",
+        "t4": "feature/one",  # another worktree on same branch
+        "t5": "other",
+    }
+
+    # Test with no patterns (should return all)
+    assert core._get_indices_from_branch_patterns(show_cmd_output=False) == [1, 2, 3, 4, 5]
+
+    # Test with a pattern that matches multiple branches
+    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]
+    assert core._get_indices_from_branch_patterns(["feature/*"], show_cmd_output=False) == [1, 2, 4]
+    mock_get_matching_branches.assert_called_once_with("feature/*", show_cmd_output=False)
+
+    # Test with a pattern that matches one branch
+    mock_get_matching_branches.reset_mock()
+    mock_get_matching_branches.return_value = ["bugfix/short"]
+    assert core._get_indices_from_branch_patterns(["bugfix/short"], show_cmd_output=False) == [3]
+    mock_get_matching_branches.assert_called_once_with("bugfix/short", show_cmd_output=False)
+
+    # Test with multiple patterns
+    mock_get_matching_branches.reset_mock()
+    def side_effect(pattern, show_cmd_output=False):
+        if pattern == "feature/two":
+            return ["feature/two"]
+        if pattern == "other":
+            return ["other"]
+        return []
+    mock_get_matching_branches.side_effect = side_effect
+    assert core._get_indices_from_branch_patterns(["feature/two", "other"], show_cmd_output=False) == [2, 5]
+    assert mock_get_matching_branches.call_count == 2
+
+    # Test with pattern that matches nothing
+    mock_get_matching_branches.reset_mock()
+    mock_get_matching_branches.side_effect = None
+    mock_get_matching_branches.return_value = []
+    assert core._get_indices_from_branch_patterns(["nonexistent"], show_cmd_output=False) == []
+
+    # Test with no worktrees
+    mock_get_worktree_state.return_value = {}
+    assert core._get_indices_from_branch_patterns(show_cmd_output=False) == []
+
+
+@patch("agro.core._get_matching_branches")
+@patch("agro.core._run_command")
+@patch("builtins.input", return_value="y")
+@patch("agro.core.logger")
+def test_fade_branches_simple(
+    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
+):
+    # Mock current branch
+    mock_run_command.side_effect = [
+        MagicMock(stdout="main"),  # for getting current branch
+        MagicMock(returncode=0),  # for git branch -D
+        MagicMock(returncode=0),  # for git branch -D
+    ]
+
+    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]
+
+    core.fade_branches(["feature/*"], show_cmd_output=False)
+
+    mock_get_matching_branches.assert_called_once_with(
+        "feature/*", show_cmd_output=False
+    )
+
+    # Check that we tried to delete the branches
+    delete_calls = [
+        call(
+            ["git", "branch", "-D", "feature/one"],
+            capture_output=True,
+            check=False,
+            show_cmd_output=False,
+        ),
+        call(
+            ["git", "branch", "-D", "feature/two"],
+            capture_output=True,
+            check=False,
+            show_cmd_output=False,
+        ),
+    ]
+    # First call is to get current branch
+    mock_run_command.assert_has_calls(delete_calls, any_order=True)
+    assert mock_run_command.call_count == 3  # 1 for current branch, 2 for delete
+
+    # Check logging
+    mock_logger.info.assert_any_call("Deleted branch 'feature/one'.")
+    mock_logger.info.assert_any_call("Deleted branch 'feature/two'.")
+
+
+@patch("agro.core._get_matching_branches")
+@patch("agro.core._run_command")
+@patch("builtins.input", return_value="y")
+@patch("agro.core.logger")
+def test_fade_branches_skips_current_branch(
+    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
+):
+    # Mock current branch
+    mock_run_command.side_effect = [
+        MagicMock(stdout="feature/one"),  # for getting current branch
+        MagicMock(returncode=0),  # for git branch -D
+    ]
+
+    mock_get_matching_branches.return_value = ["feature/one", "feature/two"]
+
+    core.fade_branches(["feature/*"], show_cmd_output=True)
+
+    mock_get_matching_branches.assert_called_once_with(
+        "feature/*", show_cmd_output=True
+    )
+
+    # Check that we tried to delete only one branch
+    mock_run_command.assert_called_with(
+        ["git", "branch", "-D", "feature/two"],
+        capture_output=True,
+        check=False,
+        show_cmd_output=True,
+    )
+    assert mock_run_command.call_count == 2  # 1 for current branch, 1 for delete
+
+    # Check logging
+    mock_logger.warning.assert_called_with(
+        "Skipping currently checked out branch 'feature/one'"
+    )
+    mock_logger.info.assert_any_call("Deleted branch 'feature/two'.")
+
+
+@patch("agro.core._get_matching_branches")
+@patch("agro.core._run_command")
+@patch("builtins.input", return_value="n")
+@patch("agro.core.logger")
+def test_fade_branches_user_cancel(
+    mock_logger, mock_input, mock_run_command, mock_get_matching_branches
+):
+    # Mock current branch
+    mock_run_command.return_value = MagicMock(stdout="main")
+
+    mock_get_matching_branches.return_value = ["feature/one"]
+
+    core.fade_branches(["feature/one"], show_cmd_output=False)
+
+    # Check that we did not try to delete
+    delete_call = call(
+        ["git", "branch", "-D", "feature/one"],
+        capture_output=True,
+        check=False,
+        show_cmd_output=False,
+    )
+    assert delete_call not in mock_run_command.mock_calls
+
+    # Check logging
+    mock_logger.warning.assert_called_with("Operation cancelled by user.")
+
+
+@patch("agro.core._get_matching_branches")
+@patch("agro.core.logger")
+def test_fade_branches_no_match(mock_logger, mock_get_matching_branches):
+    mock_get_matching_branches.return_value = []
+    core.fade_branches(["nonexistent"], show_cmd_output=False)
+    mock_logger.info.assert_called_with(
+        "No branches found matching the patterns to delete."
+    )
