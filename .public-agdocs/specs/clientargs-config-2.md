factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type.

note that all agent_args should also be passed to the agent in addition to the built-ins.

setup the exec to run the following commands that replicate the behavior of the following commands for the launching the agent, note for claude and 

cat .agdocs/specs/add-var.md | gemini -y &> .agswap/agro-exec.log
cat .agdocs/specs/agent-var.md | claude -p --allowedTools "Write Edit MultiEdit" &> .agswap/agro-exec.log

Add an optional -a/--agent-type flag to exec for agent type to modify that config var set at workspace level. this is because the exec-cmd might differ from the agent-type, e.g.
> agro exec task.md 2 wrapper-gemini.sh -a gemini