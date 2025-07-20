# Agro-builds-Agro pt 1
_July 8, 2025_


### Introduction

We're prsenting a case study of using agent based workflow to create a feature. In this case we're using `agro` to actually build features on `agro`. 

We'll default to using `aider` as our agent with `gemini-2.5-pro-preview-06-05` for our model api.

#### tl;dr
- We use multiple agents to generate potential solutions to [task](https://github.com/sutt/agro/blob/example/implicit-arg/.public-agdocs/specs/implicit-taskfile.md).
- We compare the solutions at a high-level with `git` and `pytest`.
- We test the best solution and accept it, generated code corresponding to commits:[`4bbfa5`](https://github.com/sutt/agro/commit/4bbfa54d239d1aa06bb2337f06e40d6c9b36b78f) [`fc514b`](https://github.com/sutt/agro/commit/fc514bdea08d1f0f51908e6a0da29bd8542c3107).
- Brief look at other not-accepted soltuions for how they differed and problems they ran into. 

### Feature for Case-Study

Here is the file [implicit-taskfile.md](../../.public-agdocs/specs/implicit-taskfile.md) and here are the contents:

```md
Update the cli logic to allow taskfile to be an optional and positional argument. 

Update the args to have a -c as an alias for exec-cmd.

- Remember taskfile is always a str, num-trees is always int, exec-cmd is always a str. 
- Num-tree and exec-cmd can swap places positionally

the new docs are
  exec [args] [taskfile] [num-trees] [exec-cmd]
                                
        Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees to create.
          -t <indices>          Specified worktree indice(s) (e.g., '1,2,3').
          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree
          ...others             See below.


In the case when taskfile is not passed it will be searched for:

- if found the user will get a Prompt to confirm before proceeding with the full command
- if not found the user will be notified, with expected vs actual message and command terminated
(When taskfile is passed explicitly the user should not a prompt confirm)

The takfile that will be selected to pass onto the main command is the most recently modified .md file in ./.agdocs/specs/ directory (or whatever the config points to).

In the case where the taskfile is pass explicitly:

- The taskfile can be searched to match:
    - in .agdocs/specs/ by default (although use config vars)
    - or possibly at root or the path specified

- The taskfile will be a fuzzy match here since taskfiles are .md's and the taskfile might or might not be passed with this extension, and a full relative path might be specified or not in the case assuming you'll look in the default directory. Also the files could be at root, don't worry about the case of collisiosn other than just ignore the user.
    - user could say: agro exec add-db # which will search for .agdocs/specs/add-db.md or ./add-db.md 
    - user could say: agro exec make-readme.md # which will search for .agdocs/specs/make-readme.md or ./make-readme.md
    - user could say: agro exec .agdocs/specs/add-db.md # which will search for only .agdocs/specs/add-db.md
    This functionality of fuzzy matching the taskfile input string to possible existing files in the repo should be include both 

Update and refactor cli tests as needed for these updates, and add new tests for this functionality.
```

#### Context for feature
It helps to understand a little context around the reason for this feature and the development history leading up to it.

The **main rationale** is designed to make the cli command `agro exec` very simple to invoke by eliminating all required arguments while keeping the power and composability. In other words, these will multiple valid ways to call the command, which are appealing to different types of users.

```bash
# this is valid and very easy to show for quickstart
agro exec

# this is valid; and works for explicit scripting and complex use
agro exec .agdocs/specs/my-feature.md -n 3 -c gemini  

# this is valid; and equivalent to line above, but more ergonomic
agro exec my-feature 3 gemini  
```

#### Evolution of the feature

We can see this feature continues to evolve as we can see previous version documentation. This happens in iterative development so new specs are often updates/modifications on previous requests.

```bash
# v0.1.2 
exec <taskfile> [num-trees] 
# v0.1.3
exec [args] <taskfile> [num-trees] [exec-cmd] 
```

#### Spec file context

Note that this is an unusally complex and well formatted prompt compared to the others that have been run so far. For some other examples see all the specs of 

- **agswap-dir.md**
```md
add a .agswap directory on worktree creation with a .gitignore inside this log directory (contents=*).
If running from exec_agent:
- write the prompt-file into the log directory with the same filename as the src.
- pipe the stdout / stderr from maider into this directory.
```

- **config-yaml.md**
```md
add an optional yaml config for agro.
the default place to look to load it is .agdocs/conf/agro.conf.yml
add all the variables from the current expected .env, and change config to load from yaml instead.
also:
create a template config on "agro init" command. the template file will have comments explaining what the config does and a commented to out default version.
```


### Create a solution

Now that we've discussed the tasks, let's walk through how the solutions were developed.

##### Preview

The generated code on the three runs have been push to branches here (and sneak peak at the accepted status):
- [tree/example/implicit-arg.output.1](https://github.com/sutt/agro/tree/example/implicit-arg.output.1)  (accepted: 🏆)
- [tree/example/implicit-arg.output.2](https://github.com/sutt/agro/tree/example/implicit-arg.output.2)  (accepted: 👎)
- [tree/example/implicit-arg.output.3](https://github.com/sutt/agro/tree/example/implicit-arg.output.3)  (accepted: 👎)


These were all performed with `aider` as the agent, `gemini2.5-pro-06-05` as the model and off the commit 

##### Follow Along
If you want to follow this tutorial, you can start from the git checkpoint where this feature was run, and 

```bash
# have agro installed
agro --version 
# agro v0.1.4

# clone the branch
git clone --branch implicit-arg git@github.com:sutt/agro.git example-agro
cd example-agro

# copy the spec file into internal agdocs
agro init
cp .public-agdocs/specs/implicit-taskfile.cmd .agdocs/specs/
```

Now you should be ready to run the same commands

### Start the Agents: `agro exec`
#### Run
Run three separate agents on the task:
```
agro exec .agdocs/specs/implicit-taskfile.md 3
```
### Examine the git history
View a summary of the  first agent's changes
##### Run
```
git diff --stat tree/t1 output/implicit-taskfile.1
```
##### Output
```bash
src/agro/cli.py   |  77 ++++++++---
src/agro/core.py  |  42 ++++++
tests/test_cli.py | 394 ++++++++++++++++++++++++++++++++++++++----------------
3 files changed, 376 insertions(+), 137 deletions(-)
```
##### Run
```
git diff --stat tree/t2 output/implicit-taskfile.2
git diff --stat tree/t3 output/implicit-taskfile.3
```
##### Output
```bash
src/agro/cli.py   |  76 ++++++++++++----
src/agro/core.py  |  50 ++++++++++
tests/test_cli.py | 267 ++++++++++++++++++++++++------------------------------
3 files changed, 225 insertions(+), 168 deletions(-)

src/agro/cli.py   |  92 +++++++++++++----
src/agro/core.py  |  46 +++++++++
tests/test_cli.py | 297 +++++++++++++++++++++++++++++++-----------------------
3 files changed, 288 insertions(+), 147 deletions(-)

```
So each solution changed the same files, roughly the same amount. This is generally a good sign as it means the model is handling it well. For simple tasks (or even long-winded tasks that have an easy solution), you'll often see almost exact changes across multiple agent runs which is a signal either the task is a) straightforwardly solved b) mis-specified or was mis-understood by the agent.
 

### Check Tests

We can see that agent1 has all passing tests, and added new tests. The other agents (2 and 3) have a few tests failing after their edits.

<details>
    <summary>
    We started we started with 19 tests by running pytest on feature branch
    </summary>

We can see the original branch had 19 tests

```uv run pytest```

```bash
=========================================== test session starts ===========================================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 19 items                                                                                        

tests/test_cli.py ...................                                                               [100%]

=========================================== 19 passed in 0.08s ============================================
```
</details>

#### Run
```agro -vv muster 'uv run pytest -q --tb=no' 1,2,3```

- Notice the `agro -vv` mode allows all-tests-pass suites to print confirmation.
- Notice the `-q --tb=no` args passed to pytest prevent failed tests from overwhelming the output; but still see how many failed.

##### Results
```bash

--- Running command in t1 (trees/t1) ---
$ uv run pytest -q --tb=no
Running command in 'trees/t1': $ uv run pytest -q --tb=no
........................                                                 [100%]
24 passed in 0.06s

--- Running command in t2 (trees/t2) ---
$ uv run pytest -q --tb=no
Running command in 'trees/t2': $ uv run pytest -q --tb=no
............F.....                                                       [100%]
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_dispatch_exec_auto_detect_taskfile - Assertion...
1 failed, 17 passed in 0.05s

--- Running command in t3 (trees/t3) ---
$ uv run pytest -q --tb=no
Running command in 'trees/t3': $ uv run pytest -q --tb=no
...........FF......F                                                     [100%]
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_dispatch_exec_explicit_taskfile - AssertionErr...
FAILED tests/test_cli.py::test_dispatch_exec_taskfile_and_num_trees - Asserti...
FAILED tests/test_cli.py::test_dispatch_exec_explicit_taskfile_not_found - As...
3 failed, 17 passed in 0.06s

```


### Manually test solution

Let's go with agent1's solution since it passed all its tests (and added the most new tests).

Let's get this with the command

```
agro grab output/implicit-taskfile.1
```

We should now have the edits from the agent and be on branc `output/implicit-taskfile.1.copy` and we'll run `./redeploy` to the `uv tool` uninstall/install on this repo. Now that we have the updated code, and the changes active in package itself  the system, we'll test it on another repo to test


#### Check the cli help to see it was updated
Looks like both on both counts:
- `taskfile` is denoted as optional
- `-c` alias documented
##### Run
```agro -h```
##### Output
```bash
usage: agro [-h] [--version] [-v] [-q]
...
Main command:
  exec [args] [taskfile] [num-trees] [exec-cmd]   
                                
        Run an agent in new worktree(s)
        args:
          -n <num-trees>        Number of worktrees to create.
          -t <indices>          Specified worktree indice(s) (e.g., '1,2,3').
          -c <exec-cmd>         Run the exec-cmd to launch agent on worktree
          ...others             See below.

Other Commands:
  ...
```

## Get Testing Repo

We'll head over to another test repo to make testing surface area smaller (and less tied into the package development itself). This will help us assess some manual testing with quick agent completions and with minimal code diffs.

```bash
git clone git@github.com:sutt/agro-demo.git
cd agro-demo
```

Now run commands in here with the prebuilt specs on this demo / testing repo.

### Manual Testing

Having a manual tsting plan in-mind when you develop the spec is important for considering how to scope them. 

We don't want to examine the full changes before:
- running the immediately testable core functionality
- running any easily runnable, and easily thought of edge cases

This way we can accelerate the time to declaring a solution kaput, and switching solutions, or refining the task and regenerating a solution. It's important to not get too invested in details of the actual code updates immediately.


### Understanding the changes
Now that this looks like a winning solution, let's take a look at how it was implemented:

##### `src` changes
- parsing logic in `_dispatch_exec`
- updates to argparse setup and help text
- task file match logic: fuzzy name and most-recent
- **Overall:** it's on the verbose and clunky side but still seems to work

##### `tests` changes
- There needs to be a refactoring of the existing tests structure
    - this is accomplished with:
        - adding patching existing tests with on find_task_files functionality (in addition to existing mock on actual exec_cmd).
        - move `testfile` arg input to an item within `agent_args` for input.
- Do these tests still check the same conditions?
    - largely, yes (You can see more discussion below). This is important because we don't want the agent to simply change the business logic of the test for it to pass, but simply change the structure of test setup to deal with the updated src logic.
    - there are even some additional checks within the existing tests like find_match function has been asserted to be called once.
    - there's some nice work with stub lambda expression and terminal prompt bypass patches that help these tests refactor smoothly with the additional mocks.
- What do the new tests do?
    - some look at whether shell exits before the main function is called
    - lots of unimportant tests around mutually_exclusive property of calling the same arg positionally  + and with an alias flag.
    - missing the things i'd really check like permutation of the three optional positional args in different orders.
    - one key property they are missing: they don't really check the filesystem logic, the mocks just help bypass any need to do this.
      - This is OK and maybe the correct way to write these unittests, but means that the functionality might not be fully functional when we go to use it on an actual filesystem.
- **Overall: We don't usually read all the AI's tests** but they help the agents reason and check if this future changes impact assumption made in this solution.

### Repeated commits from aider

When we examine the git log of the correct solution we see **two commits** were made by the agent:

```
commit c2e787d00c14a16be0067c7f7972a5e35e268ed3
Author: sutt <wsutton17@gmail.com>
Date:   Tue Jul 8 19:03:09 2025 -0400

    fix: Make logger module-level to fix undefined name errors

commit 1c5bb98bda55248c4baf9dde70de3368205bfebd
Author: sutt <wsutton17@gmail.com>
Date:   Tue Jul 8 19:02:27 2025 -0400

    feat: Make exec taskfile optional/positional, add discovery & -c alias
```

If we examine the aider chat history we see what happend: After the first commit was made, a commit hook ran `flake8` which surfaced several `F821 - undefined name` error with a line number, which allowed the agent to generate new edits which fixed it producing working app with the second commit.

```
+> Commit 1c5bb98 feat: Make exec taskfile optional/positional, add discovery & -c alias  
+>  
+> # Fix any errors below, if possible.  
+>  
+> ## Running: /home/user/.local/share/uv/tools/aider-chat/bin/python -m flake8 --select=E9,F821,F823,F831,F406,F407,F701,F702,F704,F706 --show-source --isolated src/agro/cli.py  
+>  
+> src/agro/cli.py:67:13: F821 undefined name 'logger'  
+> logger.info(f"No task file specified. Using most recent: {found_path}")  
+> ^  
+> src/agro/cli.py:71:21: F821 undefined name 'logger'  
+> logger.info("Operation cancelled.")  
+> ^  
+> src/agro/cli.py:74:17: F821 undefined name 'logger'  
+> logger.warning("\nOperation cancelled.")  
+> ^  
+>  
+> ## See relevant lines below marked with █.  
+>  
+> src/agro/cli.py:  
+> ...⋮...  
+> 19│def _dispatch_exec(args):  
+> 20│    """Helper to dispatch exec command with complex argument parsing."""  
+> ...⋮...  

...

+
+```python
+src/agro/cli.py
+<<<<<<< SEARCH
+    except Exception as e:
+        logging.getLogger("agro").error(f"Error: {e}")
+        sys.exit(1)
+=======
+    except Exception as e:
+        logger.error(f"Error: {e}")
+        sys.exit(1)
+>>>>>>> REPLACE
+```
+
+These changes define the logger at the module level, then have `main()` configure it before it's used. This resolves the errors.
+
+> Tokens: 24k sent, 327 received. Cost: $0.03 message, $0.12 session.  
+> Applied edit to src/agro/cli.py  
+> Commit c2e787d fix: Make logger module-level to fix undefined name errors  
+> pytest tests/test_cli.py  
+> Run shell command? (Y)es/(N)o/(D)on't ask again [Yes]: n  
```

This shows the power of giving the agent the ability to run commands on the repo, in this case linting.



### Other Agent Runs: Self fixing pytest

One interesting one was Agent3 had pytest initially fail, but when the output text from the pytest result was passed in it was able to fix itself.

This shows the importance of allowing agents full ability to execute and read the result of commands. And it's currently a limitation of aider in `--yes` mode that it doesn't allow shell commands to run.

**State of pytest after round1**

```bash
user@DESKTOP-1EB4G00:~/dev/agro/agro$ uv run pytest --tb=no
      Built agro @ file:///home/user/dev/agro/agro
Uninstalled 1 package in 12ms
Installed 1 package in 9ms
======================================= test session starts =======================================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/agro/agro
configfile: pyproject.toml
testpaths: tests
collected 20 items                                                                                

tests/test_cli.py ...........FF......F                                                      [100%]

===================================== short test summary info =====================================
FAILED tests/test_cli.py::test_dispatch_exec_explicit_taskfile - AssertionError: Expected 'find_task_file' to be called once. Called 2 times.
FAILED tests/test_cli.py::test_dispatch_exec_taskfile_and_num_trees - AssertionError: Expected 'find_task_file' to be called once. Called 2 times.
FAILED tests/test_cli.py::test_dispatch_exec_explicit_taskfile_not_found - AssertionError: Regex pattern did not match.
================================== 3 failed, 17 passed in 0.17s ===================================
```

**Conversation round2 with aider**

```md

> Git repo: ../../.git/worktrees/t3 with 46 files  
> Repo-map: using 4096 tokens, auto refresh  

#### /run uv run pytest  
> Add 7.4k tokens of command output to the chat? (Y)es/(N)o [Yes]: y  
> Added 220 lines of output to the chat.  

#### What's wrong? Fix  

The test failures indicate a logic issue in how the `exec` command arguments are parsed in `_dispatch_exec`.

Specifically, `core.find_task_file` is being called twice in some scenarios, causing the first two test failures. The third failure is because a non-existent task file (like `nonexistent.md`) is being misinterpreted as an `exec_cmd`, leading to the wrong error message.

To fix this, I need to modify the `_dispatch_exec` function in `src/agro/cli.py`.

Please add `src/agro/cli.py` to the chat so I can provide the necessary changes.

> Tokens: 12k sent, 122 received. Cost: $0.02 message, $0.02 session.  
> src/agro/cli.py  
> Add file to the chat? (Y)es/(N)o/(D)on't ask again [Yes]: y  
>  
>  
> ^C again to exit  

#### What's wrong? Fix  

The test failures you're seeing are due to issues in the argument parsing logic within the `_dispatch_exec` function in `src/agro/cli.py`.

Here's a breakdown of the problems:
1.  `core.find_task_file` is called twice for some execution paths, causing two of the tests to fail their mock call assertions.
2.  When a non-existent task file is provided (e.g., `nonexistent.md`), the logic incorrectly assumes it's an `exec-cmd` instead of a missing task file. This leads to the wrong error message and the third test failure.

I will refactor `_dispatch_exec` to fix these issues by:
1.  Ensuring `core.find_task_file` is called only once by caching its result.
2.  Using a heuristic (checking for a `.md` extension) to better distinguish between a task file argument and an `exec-cmd` argument when only one is provided.

Here are the changes for `src/agro/cli.py`:

```python
src/agro/cli.py
<<<<<<< SEARCH
def _dispatch_exec(args):
    """Helper to dispatch exec command with complex argument parsing."""
    agent_args = args.agent_args.copy()


    core.exec_agent(
        task_file=str(task_file),
        fresh_env=args.fresh_env,
        no_overrides=args.no_env_overrides,
        agent_args=agent_args,
        exec_cmd=exec_cmd,
        indices_str=args.tree_indices,
        num_trees=num_trees,
        show_cmd_output=(args.verbose >= 2),
    )
=======

    core.exec_agent(
        task_file=str(task_file),
        fresh_env=args.fresh_env,
        no_overrides=args.no_env_overrides,
        agent_args=agent_args,
        exec_cmd=exec_cmd,
        indices_str=args.tree_indices,
        num_trees=num_trees,
        show_cmd_output=(args.verbose >= 2),
    )
>>>>>>> REPLACE
```

After applying these changes, you can run the tests again to confirm the fix.

```bash
uv run pytest
```

> Tokens: 15k sent, 1.7k received. Cost: $0.04 message, $0.05 session.  
> Applied edit to src/agro/cli.py  
> Commit 27f1b68 fix: Refactor exec arg parsing to fix task file lookup  
> uv run pytest  
> Run shell command? (Y)es/(N)o/(D)on't ask again [Yes]: n  
> You can use /undo to undo and discard each aider commit.  

```

This shows a shortcoming of aider: that it doesn't truly run in "yolo" mode with ability to run arbitrary bash commands; it can run linting hooks on commit but not shell out to pytest in agent mode. So this will need to be an improvement.

**The end of case study #1.**

---

## Navigation

- [← Case Studies Index](index.md)
- [Next: ABA-2 - Interactive Multi-prompt Development →](aba-2.md)

