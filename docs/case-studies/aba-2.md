# Agro-builds-Agro pt 2
_July 9, 2025_

Here we present a an interactive mutli-prompt path.

We start from root: a0b6986

We broke the full edit we wanted into two specs, the first step **agent-var.md** will setup the fuller implementation in the second step **clientargs-config.md**.

```md
add a new config variable for agent type which accepts "aider", "gemini", "claude" or rejects as not found. It should default to "aider".
This is similiar to EXEC_CMD but exec command is about what command actually gets run .e.g "my-aider.sh", this variable will help establish which underlying agent is actually called by the exec_cmd, and this helps determines certain procedures that need to be run in exec flo  and which built-in flags (e.g. --yes) get passed to the script.
```

```md
factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type.

note that all agent_args should also be passed to the agent in addition to the built-ins.

setup the exec to run the following commands that replicate the behavior of the following commands for the launching the agent, note for claude and 

cat .agdocs/specs/add-var.md | gemini -y &> .agswap/agro-exec.log
cat .agdocs/specs/agent-var.md | claude -p --allowedTools "Write Edit MultiEdit" &> .agswap/agro-exec.log

Add an optional -a/--agent-type flag to exec for agent type to modify that config var set at workspace level. this is because the exec-cmd might differ from the agent-type, e.g.
> agro exec task.md 2 wrapper-gemini.sh -a gemini
```

 
We build the second solution "task2" off the succesful branch(es) on "task1". That means running `agro grab <good-branch-name>` before running the next `agro exec <task2>`

When running the second task, we found both models mis-interpreted the thus we created a second prompt, a copy with additional and reran the agents. When running this next round, we were able to select from the one of two agents that succesfully passed their pytests.

```diff
cat .agdocs/specs/add-var.md | gemini -y &> .agswap/agro-exec.log
cat .agdocs/specs/agent-var.md | claude -p --allowedTools "Write Edit MultiEdit" &> .agswap/agro-exec.log

+ however instead of catting the contents of that spec file within the shell command, read the contents in (exit status 1 if file empty) and then dump those to stdin with the command

Add an optional -a/--agent-type flag to exec for agent type to modify 
```

After finding a solution we are looking for manual testing made it clear the cli option was a little clunky, to call an agent that wasn't the default you either had to edit the config var or pass the same info twice on cli in `agent-type` and the `exec-cmd` args. Since these were undesirable it created the need for one more task **infer-model.md**, and the solution b3f7089.

```md
allow the agent_type parameter to be infered in the absence of -a flag. We infer the agent_type from exec-cmd if passed absed on the criterion is a recognized agenttype in the name of the exec-cmd, e.g. "gemini" is in "mgemini.sh"

likewise infer the exec command if not passed from cli based off the agent type supplied in the -a flag if passed.
```

Finally there's manual fixup at the end 0001b16.

### Specs & Outputs

- [agent-var.md](../../.public-agdocs/specs/agent-var.md)
    - output: 1692086
- [clientargs-config.md](../../.public-agdocs/specs/clientargs-config.md)
    - output: n/a this was revised to v2
- [clientargs-config.md](../../.public-agdocs/specs/clientargs-config.md)
    - output: 97677ff
- [infer-model.md](../../.public-agdocs/specs/infer-model.md)
    - output: b3f7089
- manual
    - output: 0001b16


### Path

This shows the agent creations, agent_type, and what branch they were built off. the happy path was `task1.3 -> task2-2.2 -> task3.1` which accepted aider every time.

```
- task1: agent-var
    .1 - gemini
    .2 - claude
    .3 - aider
    .4 - aider
- task2: clientargs-config
    .1      - claude v1 prompt           off task1.2
    .2      - aider, v1 prompt           off task1.3
    .3      - aider, v1 prompt           off task1.3
    -2.1    - aider, v2 prompt           off task1.3
    -2.2    - aider, v2 prompt           off task1.3
- task3: infer-model
    .1      - aider                      off task2-2.2
    .2      - claude                     off task2-2.2
```

This shows we can continue to attempt to bring other models into the development as we progress.

### Total Edits

```
 src/agro/cli.py    |  22 ++++++++
 src/agro/config.py |  36 +++++++++++++
 src/agro/core.py   |  58 ++++++++++++++------
 tests/test_cli.py  | 154 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 253 insertions(+), 17 deletions(-)

```

Tests: 24 before, after 28. 4 tests added.