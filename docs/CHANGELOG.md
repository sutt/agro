# Changelog

## [0.1.6]

- **BREAKING**: Removed `-t/--tree-indices` flag from `exec` command - use branch patterns with other commands instead
- **BREAKING**: Changed `muster` and `surrender` commands to use branch patterns instead of indices
- **BREAKING**: Changed `fade` command to accept multiple patterns instead of single regex pattern
- Enhanced CLI help text with better formatting, examples, and branch pattern documentation
- Added `state` command to show worktree-to-branch mappings with optional filtering
- Added support for brace expansion in branch patterns (e.g., `output/feat.{1-3}`, `branch.{2,5}`)
- Added automatic guide file integration for all agent types:
  - Aider: adds guide files with `--read` flag
  - Claude: prepends `@.agswap/guides/*` reference to task content
  - Gemini: creates `.gemini/settings.json` with guide file references
- Added `guides/` directory creation during `agro init` with default `GUIDE.md`
- Improved error handling with `suppress_error_logging` parameter for cleaner output
- Updated command signatures to use more descriptive parameter names

## [0.1.5]

- **BREAKING**: Changed `dependency-groups` to `project.optional-dependencies` in `pyproject.toml` for better compatibility
- Added `-a/--agent-type` flag to `exec` command for specifying agent type (aider, claude, gemini)
- Added `--no-auto-commit` flag to `exec` command to disable automatic commits
- Added automatic agent type inference from command name when not explicitly specified
- Added agent-specific configuration support with `AGENT_CONFIG` setting
- Added timeout support for agents with `AGENT_TIMEOUTS` configuration
- Added automatic commit functionality for non-aider agents via background committer process
- Added new `committer.py` module for handling background auto-commits
- Enhanced `exec_agent` function to support different agent types with proper argument handling
- Updated environment setup to use `--all-extras` instead of `--group test` for uv sync
- Improved agent command construction with support for stdin vs command-line task file passing