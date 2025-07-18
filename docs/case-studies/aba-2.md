# Agro-builds-Agro pt 2
_July 9, 2025_

Here we present a an interactive mutli-prompt path:
- Full Task: _in this case adding an agent_type arg and business logic_
- Breaking up the task: _into multiple prompts_
- Workflow of: _generating, reviewing, accepting, generating next prompt ..._
- Tweaking: _after review of first draft_

### Setup

We start from commit: [a0b6986](https://github.com/sutt/agro/commit/a0b6986)

We broke the full task we wanted into two specs, the first step **agent-var.md** will setup the fuller implementation in the second step **clientargs-config.md**.

**agent-var.md**
>add a new config variable for agent type which accepts "aider", "gemini", "claude" or rejects as not found. It should default to "aider".
This is similiar to EXEC_CMD but exec command is about what command actually gets run .e.g "my-aider.sh", this variable will help establish which underlying agent is actually called by the exec_cmd, and this helps determines certain procedures that need to be run in exec flo  and which built-in flags (e.g. --yes) get passed to the script.

**clientargs-config.md**
>factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type.
note that all agent_args should also be passed to the agent in addition to the built-ins.
setup the exec to run the following commands that replicate the behavior of the following commands for the launching the agent, note for claude and 
cat .agdocs/specs/add-var.md | gemini -y &> .agswap/agro-exec.log
cat .agdocs/specs/agent-var.md | claude -p --allowedTools "Write Edit MultiEdit" &> .agswap/agro-exec.log
Add an optional -a/--agent-type flag to exec for agent type to modify that config var set at workspace level. this is because the exec-cmd might differ from the agent-type, e.g.
> agro exec task.md 2 wrapper-gemini.sh -a gemini

### Workflow for Generation
 
We build the second solution "task2" off the succesful branch(es) on "task1". That means running `agro grab <good-branch-name>` before running the next `agro exec <task2>`

When running the second task, we found both models mis-interpreted the thus we created a second prompt, a copy with additional and reran the agents. When running this next round, we were able to select from the one of two agents that succesfully passed their pytests.

**clientargs-config-v2.md**
```diff
cat .agdocs/specs/add-var.md | gemini -y &> .agswap/agro-exec.log
cat .agdocs/specs/agent-var.md | claude -p --allowedTools "Write Edit MultiEdit" &> .agswap/agro-exec.log

+ however instead of catting the contents of that spec file within the shell command, read the contents in (exit status 1 if file empty) and then dump those to stdin with the command

Add an optional -a/--agent-type flag to exec for agent type to modify 
```

**nota bene -** this got swapped in my records and the addition was actually added to v1 instead of v2.

### Tweaks on Top

After finding a solution we are looking for manual testing made it clear the cli option was a little clunky, to call an agent that wasn't the default you either had to edit the config var or pass the same info twice on cli in `agent-type` and the `exec-cmd` args. Since these were undesirable it created the need for one more task 

**infer-model.md**

>allow the agent_type parameter to be infered in the absence of -a flag. We infer the agent_type from exec-cmd if passed absed on the criterion is a recognized agenttype in the name of the exec-cmd, e.g. "gemini" is in "mgemini.sh"
likewise infer the exec command if not passed from cli based off the agent type supplied in the -a flag if passed.



### Specs & Outputs


| Task File | Contents (truncated) | Accepted SHA |
|------|-------------|---------|
| [infer-model.md](../.public-agdocs/specs/infer-model.md) | allow the agent_type parameter to be infered in the absence of -a flag. We infer the agent_type from exec-cmd if passed... | [8b83ff6](https://github.com/sutt/agro/commit/8b83ff6) |
| [fix-tests.md](../.public-agdocs/specs/fix-tests.md) | (empty file) | [89eed93](https://github.com/sutt/agro/commit/89eed93) |
| [clientargs-config.md](../.public-agdocs/specs/clientargs-config.md) | factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type. | [e2dea27](https://github.com/sutt/agro/commit/e2dea27) |
| [clientargs-config-2.md](../.public-agdocs/specs/clientargs-config-2.md) | factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type. | [e2dea27](https://github.com/sutt/agro/commit/e2dea27) |
| [agent-var.md](../.public-agdocs/specs/agent-var.md) | add a new config variable for agent type which accepts "aider", "gemini", "claude" or rejects as not found. It should default to "aider". | [75e4614](https://github.com/sutt/agro/commit/75e4614) |


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


So this is the pattern of:
- `agro task task-1`
- `agro task task-2`
- `agro exec task-1`
- `agro grab task-1-solution`
- `agro exec task-2 (off task-1-solution branch)`
- `agro task task-2-v2`
- `agro exec task-2-v2 (off task-1-solution branch)` 
- `agro grab task-2-v2-solution`
- manual fix for tests
- `agro task tweak-1`
- `agro exec tweak-1 (off task-2-v2-solution branch)`
- `agro grab tweak-1-solution`
- full manual testing before acepting

**finally:** `git checkout dev && git merge tweak-1-solution`


### Total Edits

```
 src/agro/cli.py    |  22 ++++++++
 src/agro/config.py |  36 +++++++++++++
 src/agro/core.py   |  58 ++++++++++++++------
 tests/test_cli.py  | 154 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 253 insertions(+), 17 deletions(-)
```

**Tests:** 
- before: 24
- after: 28
- added: 4

### Conclusion

We know that the weakness of _vide coding_ is trying to produce too large of a solution because it can approach the problem in a way that is wrong - either the intent is incorrect or the solution has bugs. The solution workflow here is to:
- Break one task into multiple smaller specs
    - review the first spec solutions and accept the solution before launching the second spec by checking out the branch of the accepted solution.
- Change your prompt instead of changing the solution when the first generation misses intent.
    - We saw this by changing `clientargs-config.md -> clientargs-config-v2.md`
- Once the manual fixes are minimal, that's when we perform coding manually and modify the behavior after testing as we did with `infer-model.md`.

Happy Coding :)