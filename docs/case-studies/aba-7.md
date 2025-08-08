# Agro-builds-Agro pt 7
_August 8, 2025_

Quick post today, let's look at interesting generation: two very different proposals that are both _mostly correct_ under **their own assumptions** for the prompt.

### The Prompt

[safetest-cmd.md](../../.public-agdocs/specs/safetest-cmd.md)

> add a command template to the muster common commands called "safetest" which similiar to testq calls pytest with uv runner. But this command is launched with a 20 second timeout, so that if a test function "gets stuck" the background process does not jam up the computer indefinetly.

(The need for this prompt was discovered in user testing as duscussed [here](./aba-vidstr-2.md#motivation-for-agro-muster--c-safetest))

### The Generations
We'll generate two solutions with an **aider + Gemini-2.5-Pro** via `agro exec safetest-cmd 2` which puts our git owrktrees in the following state:
```
* master
+ output/safetest-cmd.1
+ output/safetest-cmd.2
  tree/t2
  tree/t3
```

The `diff --stat` for each show one solution is a one-liner change, and the other solution is ~100 lines across several modules.

```bash
--- Diff for t2 (output/safetest-cmd.1) ---
$ git diff --stat tree/t2 HEAD
 src/agro/config.py | 1 +
 1 file changed, 1 insertion(+)

--- Diff for t3 (output/safetest-cmd.2) ---
$ git diff --stat tree/t3 HEAD
 .public-agdocs/conf/agro.conf.yml | 15 +++++++++----
 src/agro/config.py                |  7 ++++---
 src/agro/core.py                  | 35 ++++++++++++++++++++++++++-----
 tests/test_core.py                | 44 ++++++++++++++++++++++++++++++++++++---
 4 files changed, 86 insertions(+), 15 deletions(-)
```

How could one prompt generate such a difference in output? Let's take a look at the full diffs:

**For the one-line change:**

```diff
--- Diff for t2 (output/safetest-cmd.1) ---
$ git diff tree/t2 HEAD
diff --git a/src/agro/config.py b/src/agro/config.py
index 470953d..65996f0 100644
--- a/src/agro/config.py
+++ b/src/agro/config.py
@@ -47,6 +47,7 @@ DEFAULTS = {
     },
     'MUSTER_COMMON_CMDS': {
         'testq': 'uv run pytest --tb=no -q',
+        'safetest': 'timeout 20 uv run pytest --tb=no -q',
         'server-start': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
         'server-kill': 'kill $(cat server.pid) && rm -f server.pid server.log',
     },
```

**For the 100-line change:**

```diff
--- Diff for t3 (output/safetest-cmd.2) ---
$ git diff tree/t3 HEAD
diff --git a/.public-agdocs/conf/agro.conf.yml b/.public-agdocs/conf/agro.conf.yml
index af9f0ab..f2e53c4 100644
--- a/.public-agdocs/conf/agro.conf.yml
+++ b/.public-agdocs/conf/agro.conf.yml
@@ -74,7 +74,14 @@ EXEC_CMD_DEFAULT: maider.sh
 
 # Pre-defined commands for 'agro muster -c'.
 MUSTER_COMMON_CMDS:
-  testq: "uv run pytest --tb=no -q"
-  server-start: "uv run python app/main.py > server.log 2>&1 & echo $! > server.pid"
-  server-kill: "kill $(cat server.pid) && rm -f server.pid server.log"
-  gitone: "git log -n 1 --oneline"
+  testq:
+    cmd: "uv run pytest --tb=no -q"
+  safetest:
+    cmd: "uv run pytest --tb=no -q"
+    timeout: 20
+  server-start:
+    cmd: "uv run python app/main.py > server.log 2>&1 & echo $! > server.pid"
+  server-kill:
+    cmd: "kill $(cat server.pid) && rm -f server.pid server.log"
+  gitone:
+    cmd: "git log -n 1 --oneline"
diff --git a/src/agro/config.py b/src/agro/config.py
index 470953d..8c65937 100644
--- a/src/agro/config.py
+++ b/src/agro/config.py
@@ -46,9 +46,10 @@ DEFAULTS = {
         'gemini': 600,  # 10 minutes timeout for gemini calls
     },
     'MUSTER_COMMON_CMDS': {
-        'testq': 'uv run pytest --tb=no -q',
-        'server-start': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
-        'server-kill': 'kill $(cat server.pid) && rm -f server.pid server.log',
+        'testq': {'cmd': 'uv run pytest --tb=no -q'},
+        'safetest': {'cmd': 'uv run pytest --tb=no -q', 'timeout': 20},
+        'server-start': {'cmd': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid'},
+        'server-kill': {'cmd': 'kill $(cat server.pid) && rm -f server.pid server.log'},
     },
     'AGRO_EDITOR_CMD': 'code',
     'ENV_SETUP_CMDS': [
diff --git a/src/agro/core.py b/src/agro/core.py
index c94d0df..5617dc1 100644
--- a/src/agro/core.py
+++ b/src/agro/core.py
@@ -162,8 +162,10 @@ def _get_config_template():
 
     # Format MUSTER_COMMON_CMDS
     muster_common_cmds_lines = ["# MUSTER_COMMON_CMDS:"]
-    for key, cmd in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
-        muster_common_cmds_lines.append(f"#   {key}: {json.dumps(cmd)}")
+    for key, data in config.DEFAULTS.get("MUSTER_COMMON_CMDS", {}).items():
+        muster_common_cmds_lines.append(f"#   {key}:")
+        for sub_key, sub_value in data.items():
+            muster_common_cmds_lines.append(f"#     {sub_key}: {json.dumps(sub_value)}")
     muster_common_cmds_str = "\n".join(muster_common_cmds_lines)
 
     return f"""# Agro Configuration File
@@ -357,6 +359,7 @@ def _run_command(
     shell=False,
     show_cmd_output=False,
     suppress_error_logging=False,
+    timeout=None,
 ):
     """Helper to run a shell command."""
     cmd_str = command if isinstance(command, str) else shlex.join(command)
@@ -373,8 +376,18 @@ def _run_command(
             text=True,
             capture_output=do_capture,
             shell=shell,
+            timeout=timeout,
         )
         return result
+    except subprocess.TimeoutExpired as e:
+        if not suppress_error_logging:
+            cmd_str = command if isinstance(command, str) else shlex.join(command)
+            logger.error(f"Command timed out after {timeout} seconds: {cmd_str}")
+            if e.stdout:
+                logger.error(f"STDOUT:\n{e.stdout.strip()}")
+            if e.stderr:
+                logger.error(f"STDERR:\n{e.stderr.strip()}")
+        raise
     except subprocess.CalledProcessError as e:
         if not suppress_error_logging:
             cmd_str = command if isinstance(command, str) else shlex.join(command)
@@ -965,9 +978,10 @@ def muster_command(
     common_cmd_key=None,
 ):
     """Runs a command in multiple worktrees."""
+    timeout = None
     if common_cmd_key:
-        final_command_str = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
-        if not final_command_str:
+        cmd_config = config.MUSTER_COMMON_CMDS.get(common_cmd_key)
+        if not cmd_config:
             config_path = Path(config.AGDOCS_DIR) / "conf" / "agro.conf.yml"
             msg = f"Common command '{common_cmd_key}' not found in 'MUSTER_COMMON_CMDS'."
             if config_path.is_file():
@@ -980,6 +994,16 @@ def muster_command(
                 msg += f" Available commands are: {available_cmds}."
 
             raise ValueError(msg)
+
+        if isinstance(cmd_config, dict):
+            final_command_str = cmd_config.get("cmd")
+            timeout = cmd_config.get("timeout")
+        elif isinstance(cmd_config, str):
+            final_command_str = cmd_config
+        else:
+            raise TypeError(
+                f"Unsupported type for muster command '{common_cmd_key}': {type(cmd_config)}"
+            )
     else:
         final_command_str = command_str
 
@@ -1031,8 +1055,9 @@ def muster_command(
                 cwd=str(worktree_path),
                 shell=use_shell,
                 show_cmd_output=True,
+                timeout=timeout,
             )
-        except (subprocess.CalledProcessError, FileNotFoundError):
+        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
             # _run_command already prints details.
             logger.error(f"--- Command failed in t{index}. Continuing... ---")
             continue

```

**Then we have the diffs on the tests on this generation...**

<details>
    <summary>
    See full diffs on tests
    </summary>

```diff
diff --git a/tests/test_core.py b/tests/test_core.py
index 0450065..9149629 100644
--- a/tests/test_core.py
+++ b/tests/test_core.py
@@ -535,9 +535,11 @@ def test_muster_command(
     mock_get_worktree_state.return_value = {"t1": "output/branch.1"}
     mock_path.return_value.is_dir.return_value = True
     mock_config.MUSTER_COMMON_CMDS = {
-        "testq": "uv run pytest -q",
-        "server-start": "my-app --daemon > server.log 2>&1 &",
-        "server-kill": "kill $(cat server.pid)",
+        "testq": {"cmd": "uv run pytest -q"},
+        "safetest": {"cmd": "uv run pytest -q", "timeout": 20},
+        "server-start": {"cmd": "my-app --daemon > server.log 2>&1 &"},
+        "server-kill": {"cmd": "kill $(cat server.pid)"},
+        "old-style": "echo 'hello'",
     }
     mock_config.WORKTREE_OUTPUT_BRANCH_PREFIX = "output/"
     mock_config.AGDOCS_DIR = ".agdocs"
@@ -554,6 +556,39 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=False,
         show_cmd_output=True,
+        timeout=None,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with common command with timeout (no shell)
+    core.muster_command(
+        command_str=None,
+        branch_patterns=["output/branch.1"],
+        common_cmd_key="safetest",
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        ["uv", "run", "pytest", "-q"],
+        cwd=str(mock_path.return_value / "t1"),
+        shell=False,
+        show_cmd_output=True,
+        timeout=20,
+    )
+    mock_run_command.reset_mock()
+
+    # Test with old-style string common command
+    core.muster_command(
+        command_str=None,
+        branch_patterns=["output/branch.1"],
+        common_cmd_key="old-style",
+        show_cmd_output=True,
+    )
+    mock_run_command.assert_called_once_with(
+        ["echo", "hello"],
+        cwd=str(mock_path.return_value / "t1"),
+        shell=False,
+        show_cmd_output=True,
+        timeout=None,
     )
     mock_run_command.reset_mock()
 
@@ -568,6 +603,7 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=False,
         show_cmd_output=True,
+        timeout=None,
     )
     mock_run_command.reset_mock()
 
@@ -583,6 +619,7 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=True,
         show_cmd_output=True,
+        timeout=None,
     )
     mock_run_command.reset_mock()
 
@@ -598,6 +635,7 @@ def test_muster_command(
         cwd=str(mock_path.return_value / "t1"),
         shell=True,
         show_cmd_output=True,
+        timeout=None,
     )
     mock_run_command.reset_mock()
 
```
</details>

### Outcome

So it looks like the second solution adds **functionality for generalizability of the feature**, where as the first solution just directly answers the question. It would appear its a matter of taste and priorities of which one to select...

But reality is a little messier and turns out the simple solution doesn't actually work: if you call `agro muster 'timeout 5 ls'` it works, but calling `agro muster 'timeout 5 uv run pytest'` leads to the pytests never actually printing out, so the simple solution does not work here. 

The complex solution does work by attaching the timeout as an argument to `subprocess.run` instead of using the `timeout` utility directly.

### Conclusion

This shows how AI-assisted coding can suggest solutions to questions you haven't even thought of yet. Now ultimately what this showed was that _timeout functionality could be handled spearately from the command string being passed in_. Considering the use-case (as discussed [here](./aba-vidstr-2.md#motivation-for-agro-muster--c-safetest)), it seems that almost all muster commands should have to have timeout so we'll we-write the spec to include this:

[muster-timeout.md](../../.public-agdocs/specs/muster-timeout.md)
>add a default timeout of 20 seconds to all commands run by muster, that will pass this through to subprocess.run.
Config and Args:
- add config and command lines options that can override the default value
- create a config var for this timeout amount in agro.conf.yml: MUSTER_DEFAULT_TIMEOUT which takes an integer value in seconds. Setting to null or 0 
- modify MUSTER_COMMON_CMDS to refactor the command string in a "cmd" key, and have an optional param "timeout" which overrides the MUSTER_DEFAULT_TIMEOUT value with the same convention of null or 0 maening no timeout. 
    - For "sever-start" command add a "timeout: null" entry as the default config + what will be written into the default agro.conf.yml 
- create a cli flag for agro muster "--timeout" that overrides the config and default values, that will use seconds and input value and use the value 0 to have no timeout.

Ultimately this shows the process of development and specification is a looping and iterative process, where AI generation can be used not only to complete the code but add better thinking to specify the desired behavior of new behavior.

## Navigation

- [← Previous: ABA-Vidstr-2: External Packages + Agentic Commands](aba-vidstr-2.md)
- [Case Studies Index](index.md)

