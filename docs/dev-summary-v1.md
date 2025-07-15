# Dev Summary
Looks at tasks and associated commit solutions generated each release.

## v0.1.6

| File | Description | Git SHA |
|------|-------------|---------|
| [changelog-1.5.md](../.public-agdocs/specs/changelog-1.5.md) | Below is a diff from v0.1.4 to v0.1.5. Add entries to docs/CHANGELOG.md to describe the change | [ffffff](https://github.com/repo/commit/ffffff) |
| [changelog-1.6.md](../.public-agdocs/specs/changelog-1.6.md) | Below is a diff from v0.1.5 to v0.1.6. Add entries to docs/CHANGELOG.md to describe the change | [ffffff](https://github.com/repo/commit/ffffff) |
| [clean-help.md](../.public-agdocs/specs/clean-help.md) | tasks: - drop support the for the flag: agro exec -t - update help for agro cli: - document agro state command - document -a option to exec | [ffffff](https://github.com/repo/commit/ffffff) |
| [fade-pattern.md](../.public-agdocs/specs/fade-pattern.md) | apply the same branch pattern matching logic to the <pattern> arg in "agro fade" as is used in surrender and muster. fix any tests as nec. | [ffffff](https://github.com/repo/commit/ffffff) |
| [gemini-guide.md](../.public-agdocs/specs/gemini-guide.md) | when launching a gemini agent from exec: - check if a .gemini directory exists in at the root of the git worktree when you go to launch | [ffffff](https://github.com/repo/commit/ffffff) |
| [muster-brachname.md](../.public-agdocs/specs/muster-brachname.md) | when running muster i get printout from: f"\n--- Running command in t{index} ({worktree_path}) ---" which i want to change to f"\n--- Running command in t{index} ({branch_name}) ---" | [ffffff](https://github.com/repo/commit/ffffff) |
| [muster-vv.md](../.public-agdocs/specs/muster-vv.md) | when running "agro muster" tasks I want the commands dispatched to the trees to be run in full -vv mode (so that I can see the full output of the commands) | [ffffff](https://github.com/repo/commit/ffffff) |
| [clean-indices.md](../.public-agdocs/specs/clean-indices.md) | - drop support for -t arg in agro exec - port the branch pattern matching logic from "agro state" to "agro fade" - update the cli help text as nec. | [ffffff](https://github.com/repo/commit/ffffff) |
| [indices-to-branches.md](../.public-agdocs/specs/indices-to-branches.md) | refactor the following commands to use branch-patterns for an arg instead of index / indices: - agro surrender - agro muster | [ffffff](https://github.com/repo/commit/ffffff) |
| [fixup-1.md](../.public-agdocs/specs/fixup-1.md) | Below are bash output for various commands: We can see that: - works: agro state output/index-to-branch.{1-2} - fails: agro state output/index-to-branch.{1,2} | [ffffff](https://github.com/repo/commit/ffffff) |
| [branch-patterns.md](../.public-agdocs/specs/branch-patterns.md) | add an optional argument to "agro state" command that accepts glob like patterns for matching against a subset of existing branches: agro state [branch-pattern] | [ffffff](https://github.com/repo/commit/ffffff) |
| [index-to-branch.md](../.public-agdocs/specs/index-to-branch.md) | build a command "agro state" which prints out the branch name (output/xxx.N) connected each existing working tree currently. | [ffffff](https://github.com/repo/commit/ffffff) |
| [guide-files.md](../.public-agdocs/specs/guide-files.md) | we're adding functionality for guide files: - by default these are .agdocs/guides/.md files - these files provide guides and conventions for the coding agents | [ffffff](https://github.com/repo/commit/ffffff) |
| [do-docs-1.md](../.public-agdocs/specs/do-docs-1.md) | Create 3 - 10 pages of markdown docs for this project. - Add to the docs/ section - Structure with an: - index page linking to each page | [ffffff](https://github.com/repo/commit/ffffff) |

## v0.1.5

TODO - add table