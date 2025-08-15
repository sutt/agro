# Commands Reference

Complete reference for all Agro CLI commands and their options.

## Quick Reference

| Command | Description |
|---------|-------------|
| [`agro init`](#agro-init) | Initialize project structure |
| [`agro task`](#agro-task) | Create task specifications |
| [`agro exec`](#agro-exec) | Run agents in worktrees |
| [`agro state`](#agro-state) | Show worktree status |
| [`agro muster`](#agro-muster) | Run commands in worktrees |
| [`agro diff`](#agro-diff) | Show git diffs for worktrees |
| [`agro grab`](#agro-grab) | Switch to a branch |
| [`agro fade`](#agro-fade) | Delete branches |
| [`agro clean`](#agro-clean) | Delete worktrees and branches |
| [`agro surrender`](#agro-surrender) | Kill running agents |
| [`agro make`](#agro-make) | Create worktrees |
| [`agro delete`](#agro-delete) | Delete worktrees |
| [`agro mirror`](#agro-mirror) | Mirror internal .agdocs |

## Global Options

All commands support these global options:

```bash
agro [global-options] <command> [command-options]
```

### Global Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message |
| `--version` | Show version number |
| `-v, --verbose` | Increase verbosity (-v for debug, -vv for command output) |
| `-q, --quiet` | Suppress output except warnings and errors |

---

## agro init

Initialize the Agro project structure in the current directory.

### Usage

```bash
agro init [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--conf` | Only create configuration file, skip other initialization |
| `--completions [mode]` | Setup shell completions. Use 'perm' for permanent setup via .bashrc |

### Behavior

Creates the following directory structure:

```
.agdocs/
├── specs/          # Task specification files
├── conf/           # Configuration files
│   └── agro.conf.yml
├── guides/         # Development guides
│   └── GUIDE.md
└── swap/           # Temporary files (gitignored)
```

Also updates `.gitignore` to exclude `trees/` and `.agdocs/swap/`.

### Examples

```bash
# Full initialization (includes current session completion setup)
agro init

# Only create configuration file
agro init --conf

# Setup shell completions for current session only
agro init --completions

# Setup permanent shell completions
agro init --completions perm
```

---

## agro task

Create and manage task specification files.

### Usage

```bash
agro task [task-name]
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `task-name` | Name of the task file (without .md extension) |

### Behavior

1. Creates `.agdocs/specs/task-name.md` if it doesn't exist
2. Opens the file in your default editor
3. If no task name provided, prompts for one

### Examples

```bash
# Create a new task
agro task add-feature

# Create task with specific name
agro task fix-authentication-bug
```

---

## agro exec

Execute AI agents in isolated worktrees.

### Usage

```bash
agro exec [options] [taskfile] [num-trees] [exec-cmd] [agent-args...]
```

### Options

| Option | Description |
|--------|-------------|
| `-n, --num-trees <N>` | Number of worktrees to create |
| `-c, --exec-cmd <cmd>` | Custom command to launch agent |
| `-a, --agent-type <type>` | Agent type (aider, claude, gemini) |
| `--fresh-env` | Use .env.example instead of .env |
| `--no-env-overrides` | Don't add port overrides |
| `--no-auto-commit` | Disable automatic commits |

### Parameters

| Parameter | Description |
|-----------|-------------|
| `taskfile` | Task specification file (without .md extension) |
| `num-trees` | Number of worktrees (can be positional or flag) |
| `exec-cmd` | Agent command to execute |
| `agent-args` | Additional arguments passed to the agent |

### Argument Resolution

Agro resolves arguments in this order:
1. **Task file**: First non-numeric, non-agent string
2. **Number of trees**: Any numeric argument or `-n` flag
3. **Agent command**: Remaining string argument or `-c` flag
4. **Agent type**: `-a` flag or inferred from exec-cmd

> 💡 **Tip**: If you don't specify a task-file argument, aider will ask you if you want to run the most recently modified spec file you and you can press Enter to run it.

### Examples

```bash
# Basic execution
agro exec add-feature

# Multiple agents
agro exec add-feature 3

# Specific agent
agro exec add-feature claude

# Custom command
agro exec add-feature -c "aider --model gpt-4"

# With agent arguments
agro exec add-feature --model gpt-4 --no-auto-commits

# All options
agro exec add-feature -n 2 -a claude --fresh-env
```


---

## agro state

Show the current state of worktrees and branches.

### Usage

```bash
agro state [branch-patterns...]
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `branch-patterns` | Optional patterns to filter branches |

### Output

Displays:
- Worktree index and path
- Associated branch name
- Branch commit information
- Agent process status (if running)

### Examples

```bash
# Show all worktrees
agro state

# Show specific pattern
agro state output/add-feature

# Show multiple patterns
agro state output/feature output/bugfix
```

---

## agro muster

Run commands across multiple worktrees.

### Usage

```bash
agro muster [options] [command] [branch-patterns...]
```

### Options

| Option | Description |
|--------|-------------|
| `-c, --common-cmd <key>` | Run a pre-defined command from configuration |
| `--timeout <seconds>` | Override command timeout. Use 0 for no timeout |

### Parameters

| Parameter | Description |
|-----------|-------------|
| `command` | Command to execute in each worktree (optional if using -c) |
| `branch-patterns` | Patterns to match worktrees (defaults to output branches) |

### Branch Patterns

| Pattern | Matches |
|---------|---------|
| `output/task` | `output/task*` |
| `output/task.{1,3}` | `output/task.1`, `output/task.3` |
| `output/task.{1-4}` | `output/task.1` through `output/task.4` |

### Examples

```bash
# Run tests in all feature branches
agro muster 'npm test' 'output/add-feature'

# Check git status
agro muster 'git status' output

# Run quick tests using common command
agro muster -c testq output/add-feature

# Start servers using common command
agro muster -c server-start output/api

# Kill servers using common command  
agro muster -c server-kill output/api

# Run specific command in selected worktrees
agro muster 'pytest tests/test_auth.py' output/auth.{1,2}

# Run command in all output branches (default pattern)
agro muster 'git status'

# Override timeout for long-running command
agro muster --timeout 300 'npm run build' output/

# Disable timeout completely
agro muster --timeout 0 'npm run dev' output/
```

### Common Commands

Use `-c` flag to run pre-defined commands from your configuration:

| Key | Default Command | Description |
|-----|-----------------|-------------|
| `testq` | `uv run pytest --tb=no -q` | Run quick tests |
| `server-start` | `uv run python app/main.py > server.log 2>&1 & echo $! > server.pid` | Start server in background |
| `server-kill` | `kill $(cat server.pid) && rm -f server.pid server.log` | Kill server and cleanup |

> **Note**: Common commands can be customized in your `.agdocs/conf/agro.conf.yml` configuration file.

---

## agro diff

Show git diff for specified worktrees.

### Usage

```bash
agro diff [branch-patterns] [diff-opts] [-- pathspec]
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `branch-patterns` | Optional patterns to filter worktrees (defaults to output branches) |
| `diff-opts` | Git diff options (e.g., --stat, --name-only, --cached) |
| `pathspec` | File paths to limit diff to (after --) |

### Behavior

Shows the git diff between the original worktree branch (tree/tN) and the current HEAD for each matching worktree. This allows you to see what changes each agent made.

### Examples

```bash
# Show diff for all output worktrees (default)
agro diff

# Show diffstat for specific pattern
agro diff output/add-feature --stat

# Show diff for multiple patterns
agro diff output/feature output/bugfix

# Show diff for specific worktrees
agro diff output/add-feature.{1,3}

# Show only changed file names
agro diff output/ --name-only

# Show diff for specific files only
agro diff output/add-feature -- src/auth.py tests/test_auth.py

# Combine options with pathspec
agro diff output/ --stat -- src/
```

---

## agro grab

Checkout a branch, creating a copy if it's in use by another worktree.

### Usage

```bash
agro grab <branch-name>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `branch-name` | Name of the branch to checkout |

### Behavior

1. If branch exists and is not in use: checkout directly
2. If branch is in use by a worktree: create a copy with `.copy` suffix
3. If branch doesn't exist: error

### Examples

```bash
# Checkout available branch
agro grab output/add-feature.1

# Checkout branch in use (creates copy)
agro grab main
# Creates main.copy if main is in use
```

---

## agro fade

Delete local branches matching patterns.

### Usage

```bash
agro fade <patterns...>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `patterns` | Regex patterns to match branch names |

### Behavior

1. Lists all branches matching the patterns
2. Prompts for confirmation
3. Deletes confirmed branches
4. Skips branches currently in use by worktrees

### Examples

```bash
# Delete all feature branches
agro fade output/add-feature.

# Delete specific branches
agro fade output/add-feature.{1,3}

# Delete multiple patterns
agro fade output/feature.
```

---

## agro clean

Delete worktrees and/or associated branches matching patterns.

### Usage

```bash
agro clean [options] [branch-patterns...]
```

### Options

| Option | Description |
|--------|-------------|
| `--soft` | Only delete worktrees, not the branches |
| `--hard` | Delete both worktrees and branches (default) |

### Parameters

| Parameter | Description |
|-----------|-------------|
| `branch-patterns` | Optional patterns to select what to clean (defaults to output branches) |

### Behavior

1. Shows a dry run preview of what will be deleted
2. Prompts for confirmation  
3. Deletes matching worktrees
4. In hard mode (default), also deletes the associated branches
5. Skips branches currently checked out

### Examples

```bash
# Clean all output branches (hard delete - both worktrees and branches)
agro clean

# Clean specific feature branches
agro clean output/add-feature

# Only delete worktrees, keep branches
agro clean --soft output/feature

# Clean multiple patterns
agro clean output/feature output/bugfix

# Clean specific worktrees
agro clean output/add-feature.{1,3}
```

---

## agro surrender

Kill running agent processes.

### Usage

```bash
agro surrender [branch-patterns...]
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `branch-patterns` | Patterns to select which agents to kill |

### Behavior

1. Finds running agent processes
2. Terminates processes gracefully
3. If no patterns specified, kills all agents

### Examples

```bash
# Kill all running agents
agro surrender

# Kill agents for specific branches
agro surrender output/add-feature

# Kill multiple patterns
agro surrender output/feature output/bugfix
```

---

## agro make

Create a new worktree without running an agent.

### Usage

```bash
agro make [options] <index>
```

### Options

| Option | Description |
|--------|-------------|
| `--fresh-env` | Use .env.example instead of .env |
| `--no-env-overrides` | Don't add port overrides |

### Parameters

| Parameter | Description |
|-----------|-------------|
| `index` | Index number for the worktree |

### Examples

```bash
# Create worktree t5
agro make 5

# Create with fresh environment
agro make 6 --fresh-env

# Create without port overrides
agro make 7 --no-env-overrides
```

---

## agro delete

Delete worktrees and their associated branches.

### Usage

```bash
agro delete (<indices> | --all)
```

### Options

| Option | Description |
|--------|-------------|
| `--all` | Delete all worktrees |

### Parameters

| Parameter | Description |
|-----------|-------------|
| `indices` | Comma-separated list of worktree indices |

### Behavior

1. Removes worktree directories
2. Deletes associated branches
3. Kills any running processes in the worktrees

### Examples

```bash
# Delete specific worktrees
agro delete 1,3,5

# Delete all worktrees
agro delete --all

# Delete single worktree
agro delete 2
```

---

## agro mirror

Mirror internal documentation to the public docs directory.

### Usage

```bash
agro mirror
```

### Behavior

Copies documentation from `.agdocs/` to `.public-agdocs/` directory for public access.

By default, the .agdocs directory is added to .gitignore to keep your spec files detached from your source code and enable easier branch switching in the process of editing specs. But there are benefits to posting your spec files like this [one created for agro](https://github.com/sutt/agro/blob/master/docs/dev-summary-v1.md) for a reflection of your developer momentum.

The mirror command runs rsync to create copies of the specs. The practice on the agro project is run this before each version release as can be seen [here](https://github.com/sutt/agro/commit/85915a6c281f7a0756e3118cf79354ca50e185c7).

---

### Workflow Examples

```bash
# Complete workflow
agro init                                   # Initialize agro project
agro task add-auth                          # Create task
agro exec add-auth 2                        # Run 2 agents
agro muster -c testq output/add-auth        # Test results using common command
agro diff --stat output/add-auth            # Review changes made by agents
agro grab output/add-auth.1                 # Switch to best solution
git merge output/add-auth.1                 # Merge to main
agro clean output/add-auth                  # Clean up worktrees and branches
```

---

> 💡 **Tip**: Use `agro <command> --help` to see command-specific help and examples.

## Next Steps

- [Configuration](configuration.md) - Customize command behavior
- [Workflows](workflows.md) - Common command patterns
- [Examples](examples.md) - Real-world usage scenarios