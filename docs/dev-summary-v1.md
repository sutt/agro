# Dev Summary
Looks at tasks and associated commit solutions generated each release.

## v0.1.6

| Task File | Contents (truncated) | Accepted SHA |
|------|-------------|---------|
| [changelog-1.5.md](../.public-agdocs/specs/changelog-1.5.md) | Below is a diff from v0.1.4 to v0.1.5. Add entries to docs/CHANGELOG.md to describe the change | [d0f95f1](https://github.com/sutt/agro/commit/d0f95f1) |
| [changelog-1.6.md](../.public-agdocs/specs/changelog-1.6.md) | Below is a diff from v0.1.5 to v0.1.6. Add entries to docs/CHANGELOG.md to describe the change | [a8d0ef4](https://github.com/sutt/agro/commit/a8d0ef4) |
| [clean-help.md](../.public-agdocs/specs/clean-help.md) | tasks: - drop support the for the flag: agro exec -t - update help for agro cli: - document agro state command - document -a option to exec | [8990066](https://github.com/sutt/agro/commit/8990066) |
| [fade-pattern.md](../.public-agdocs/specs/fade-pattern.md) | apply the same branch pattern matching logic to the <pattern> arg in "agro fade" as is used in surrender and muster. fix any tests as nec. | [2cacd2e](https://github.com/sutt/agro/commit/2cacd2e) |
| [gemini-guide.md](../.public-agdocs/specs/gemini-guide.md) | when launching a gemini agent from exec: - check if a .gemini directory exists in at the root of the git worktree when you go to launch | [b01a152](https://github.com/sutt/agro/commit/b01a152) |
| [muster-brachname.md](../.public-agdocs/specs/muster-brachname.md) | when running muster i get printout from: f"\n--- Running command in t{index} ({worktree_path}) ---" which i want to change to f"\n--- Running command in t{index} ({branch_name}) ---" | [78fd4df](https://github.com/sutt/agro/commit/78fd4df) |
| [muster-vv.md](../.public-agdocs/specs/muster-vv.md) | when running "agro muster" tasks I want the commands dispatched to the trees to be run in full -vv mode (so that I can see the full output of the commands) | [f7f3c4d](https://github.com/sutt/agro/commit/f7f3c4d) |
| [clean-indices.md](../.public-agdocs/specs/clean-indices.md) | - drop support for -t arg in agro exec - port the branch pattern matching logic from "agro state" to "agro fade" - update the cli help text as nec. | [5f8a542](https://github.com/sutt/agro/commit/5f8a542) |
| [indices-to-branches.md](../.public-agdocs/specs/indices-to-branches.md) | refactor the following commands to use branch-patterns for an arg instead of index / indices: - agro surrender - agro muster | [bbb73df](https://github.com/sutt/agro/commit/bbb73df) |
| [fixup-1.md](../.public-agdocs/specs/fixup-1.md) | Below are bash output for various commands: We can see that: - works: agro state output/index-to-branch.{1-2} - fails: agro state output/index-to-branch.{1,2} | [4770390](https://github.com/sutt/agro/commit/4770390) |
| [branch-patterns.md](../.public-agdocs/specs/branch-patterns.md) | add an optional argument to "agro state" command that accepts glob like patterns for matching against a subset of existing branches: agro state [branch-pattern] | [5352b0d](https://github.com/sutt/agro/commit/5352b0d) |
| [index-to-branch.md](../.public-agdocs/specs/index-to-branch.md) | build a command "agro state" which prints out the branch name (output/xxx.N) connected each existing working tree currently. | [7996eec](https://github.com/sutt/agro/commit/7996eec) |
| [guide-files.md](../.public-agdocs/specs/guide-files.md) | we're adding functionality for guide files: - by default these are .agdocs/guides/.md files - these files provide guides and conventions for the coding agents | [404c793](https://github.com/sutt/agro/commit/404c793) |
| [do-docs-1.md](../.public-agdocs/specs/do-docs-1.md) | Create 3 - 10 pages of markdown docs for this project. - Add to the docs/ section - Structure with an: - index page linking to each page | n/a |


```
6bfdd22 docs: add dev-summary-v1
a2bf5ca release: v0.1.6
d0f95f1 feat: impl changelog-1.5 with claude (agro auto-commit)
a8d0ef4 feat: impl changelog-1.6 with claude (agro auto-commit)
497108c docs: add changelog template
8990066 refactor: major update to CLI help text
b01a152 feat: add gemini agent context via .gemini directory
5f8a542 refactor: remove -t flag and update CLI help
2cacd2e feat: align fade to support multiple glob patterns
78fd4df feat: show branch name in muster command output
f7f3c4d feat: Always show command output in muster
bbb73df refactor: update muster and surrender to use branch patterns
6cbc074 tests: benchmark cornercase branch-pattern test
4770390 fix: support multiple branch patterns in state command
5352b0d feat: add branch pattern matching to state command
7996eec feat: add 'state' command to show current branch for each worktree
148e017 fix: Simplify grab output for already checked out branch
d109172 fix: remove guides dir from configs
404c793 feat: Add agent guide file functionality
85915a6 specs: v0.1.6

```

## v0.1.5

| Task File | Contents (truncated) | Accepted SHA |
|------|-------------|---------|
| [commit-after-v2.md](../.public-agdocs/specs/commit-after-v2.md) | when the agent_type aider runs, it finishes by leaving a git commit on the worktrees branch. but when gemini and claude run they don't do a commit... | [a86fd35](https://github.com/sutt/agro/commit/a86fd35) |
| [improve-help.md](../.public-agdocs/specs/improve-help.md) | Currently copied below is what prints for help. Update this to reflect more concise and more informative and utilize best practices. | n/a |
| [commit-after.md](../.public-agdocs/specs/commit-after.md) | when the agent_Type aider runs, it finishes by leaving a git commit on the worktrees branch. but when gemini and calude run they don't do a commit... | [a86fd35](https://github.com/sutt/agro/commit/a86fd35) |
| [infer-model.md](../.public-agdocs/specs/infer-model.md) | allow the agent_type parameter to be infered in the absence of -a flag. We infer the agent_type from exec-cmd if passed... | [8b83ff6](https://github.com/sutt/agro/commit/8b83ff6) |
| [fix-tests.md](../.public-agdocs/specs/fix-tests.md) | (empty file) | [89eed93](https://github.com/sutt/agro/commit/89eed93) |
| [clientargs-config.md](../.public-agdocs/specs/clientargs-config.md) | factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type. | [e2dea27](https://github.com/sutt/agro/commit/e2dea27) |
| [clientargs-config-2.md](../.public-agdocs/specs/clientargs-config-2.md) | factor out the built-ins extra args passed to aider to a config var and setup exec to pass different arg structure for each known agent type. | [e2dea27](https://github.com/sutt/agro/commit/e2dea27) |
| [agent-var.md](../.public-agdocs/specs/agent-var.md) | add a new config variable for agent type which accepts "aider", "gemini", "claude" or rejects as not found. It should default to "aider". | [75e4614](https://github.com/sutt/agro/commit/75e4614) |
| [docker-testenv-setup.md](../.public-agdocs/specs/docker-testenv-setup.md) | add a feature for tests: launch a docker container that will execute a series of tests of an install of the current agro worktree. | n/a |
| [claude-flags.md](../.public-agdocs/specs/claude-flags.md) | allow all agent_types to be configured to have a timeout preprended to their launch command have claude be configured for a 600 s timeout default... | [d0c5a19](https://github.com/sutt/agro/commit/d0c5a19) |
| [mod-committer.md](../.public-agdocs/specs/mod-committer.md) | modify the commit message left by commiter:git_commit_changes to be of the form: "feat: impl {taskfile} with {agent_type} (agro auto-commit)" | [c1e60f1](https://github.com/sutt/agro/commit/c1e60f1) |
| [pkg-sync.md](../.public-agdocs/specs/pkg-sync.md) | currently we run which works for this project but fails for other simple 'uv sync --quiet --group test' which works for this project but fails... | [8d16b99](https://github.com/sutt/agro/commit/8d16b99) |
| [test-fail.md](../.public-agdocs/specs/test-fail.md) | Fix the tests: Here's the debug log ============================= test session starts ============================== platform linux -- Python 3.12.11... | [89eed93](https://github.com/sutt/agro/commit/89eed93) |
| [timeout-bug.md](../.public-agdocs/specs/timeout-bug.md) | when the user uncomments the AGENT_CONFIG.gemini.timeout in their conf.yml, this overrides the -y param being passed to the gemini. refactor how timeout... | [ecfe36a](https://github.com/sutt/agro/commit/ecfe36a) |

```
0f36416 release: v0.1.5
d0c5a19 fix: keep -p as last arg to claude + --max-tries fix
90defa9 feat: Add configurable agent timeouts and default args
b55530f chore: add debugging line
ecfe36a refactor: Separate agent timeouts from agent args config
8d16b99 fix: uv sync default cmd
fd215a3 fix: PEP 621
f31813a chore: Use --all-extras for default uv sync
89eed93 test: Fix _dispatch_exec tests for auto_commit handling
fa319df docs: fix ups on case studies
c69c2be fix: agent_type was None in logs
c1e60f1 feat: pass task/agent info to committer and log pid
f696247 fix: tmp workaround for commiter log
a86fd35 feat: Implement auto-commit for non-aider agents; add --no-auto-commit
696f1bc fix: re-arrange claude default args
2ad3842 feat: timeout for gemini on exec
7ab7388 docs: update case studies
1b84fd8 fix: log the agent_type on exec
8b83ff6 feat: Allow inferring agent type and exec command
e2dea27 feat: Configurable agent execution via AGENT_CONFIG and --agent-type
75e4614 feat: Add AGENT_TYPE config and use it to pass flags in exec_agent
1d75f5f specs: v0.1.5
```