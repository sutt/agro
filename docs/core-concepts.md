# Core Concepts

Understanding Agro's core concepts will help you effectively use the tool for agent-based development workflows.

## Overview

Agro orchestrates three key elements:
1. **Git Worktrees** - Isolated working directories
2. **AI Agents** - Coding assistants (aider, claude-code, gemini)
3. **Task Specifications** - Markdown files describing development tasks

## Git Worktrees

### What are Worktrees?

Git worktrees allow you to have multiple working directories from the same repository. Each worktree can be on a different branch, enabling parallel development without conflicts.

### Agro's Worktree Management

Agro creates worktrees in the `trees/` directory:

```
your-project/
├── trees/
│   ├── t1/         # First worktree
│   ├── t2/         # Second worktree
│   └── t3/         # Third worktree
├── .agdocs/        # Agro configuration
└── <your-code>     # Main project files
```

Each worktree:
- Has its own branch (e.g., `output/task-name.1`)
- Contains a complete copy of your project
- Has isolated environment configuration
- Runs independently from other worktrees

### Worktree Lifecycle

1. **Creation**: `agro exec` creates worktrees automatically
2. **Usage**: Agents work in isolated environments
3. **Comparison**: Use `agro muster` to compare results
4. **Cleanup**: `agro delete` removes worktrees when done

> ⚠️ **Important**: Worktrees are temporary. Always merge valuable changes back to your main branch before deleting the branch

## AI Agents

### Supported Agents

| Agent | Description | Command / AgentType |
|-------|-------------|---------|
| **aider** | Open-source AI pair programming; multi-model capable | `aider` |
| **claude-code** | Anthropic's Claude CLI interface | `claude` |
| **gemini-cli** | Google's Gemini CLI interface | `gemini` |

### Agent Execution

Agents run in **non-interactive mode** within worktrees:

```bash
# Agent reads task specification
# Agent modifies code files
# Agent commits changes (if auto-commit enabled)
# Agent exits when task is complete
```

> 🗒️ **Note**: This doesn't mean agents run in "YOLO" mode where they can run any command. That can be enabled with cli flags or in the configs but the default is  to allow the agents to be able to edit the files in the repo but not truly YOLO

### Agent Configuration

Agents can be configured via:
- Command-line arguments: every argument pass at the end of an agro exec command is passed along to the agent
- Environment variables
- Configuration files (`.agdocs/conf/agro.conf.yml`) under `AGENT_CONFIG:` settings.

### Agent Selection

Agro determines which agent to use based on:

1. **Explicit specification**: `agro exec task-name claude`
    - or with `-a/--agent` flag `agro exec -a claude task-name`
2. **Configuration file**: Default agent in `agro.conf.yml`
3. **Auto-detection**: Inferred from the optional `[exec-cmd]` or `-c` argument if the there is a string subset match. For example running `agro exec my-task wrapper-claude.sh` will run the claude agent type because "claude" is in the exec-cmd.
4. **Fallback**: `aider` (default)

### Agent Guide Documents

Add instructions and best-practices for your repo you want to pass to your agents in `.agdocs/guides/GUIDE.md`. Or add any other markdown files (with the `.md` extension) to the `.agdocs/guides/` directory.

Agro has functionality to pass this information into either aider, claude or gemini when you leaunch the ganet

## Task Specifications

### What are Task Specifications?

Task specifications are markdown files that describe development tasks for AI agents. They live in `.agdocs/specs/` be default.

A task can most easily be created by running `agro task <task-name>` which will create a `.md` in `.agdocs/specs`

You don't need to use agro's `.agdocs` directory specifically; you could just create a file at root like this:

```bash
touch demo.txt
echo "add a hello world console log" > demo.txt
agro exec demo.txt
```

However if you use the .agdocs/specs, you won't need to specify .md extension or the relative path to the specs directory when calling the exec command, for example:

```bash
agro exec my-feature
# equivalent to 
agro exec .agdocs/specs/my-feature.md
```

### Task File Naming

- **Filename**: `task-name.md` (kebab-case recommended)
- **Location**: `.agdocs/specs/task-name.md`
- **Branch**: Creates `output/task-name.N` branches

It is recommended to keep task file name short (1-3 words).

### Best Practices for Task Specifications

This is still an evolving art/science to it but we have some actual examples and case studies:
- See the tasks and prompts that were used to build this software in [.public-agdocs/specs](../.public-agdocs/specs/)
- Or view this information summarized in [Dev-Log](./dev-summary-v1.md).
- And review the [case studies](./case-studies/) for how to split prompts, do multi-step prompts, use yolo mode etc. 

One thing you can do is to add pipe useful information into the task file that will supplement your specifications. For example

```bash
agro task fix-tests
echo "fix the tests that are failing: " > .agdocs/specs/fix-tests.md
uv run pytest >> .agdocs/specs/fix-tests.md
agro exec fix-tests
```

So now when this task is run, the agent already has access to the full prinout of how the tests are failing.

### Environment Isolation

Each worktree gets its own environment configuration:

```
trees/t1/
├── .env                # Environment variables
├── .venv/             # Virtual environment (if using uv)
├── package.json       # Dependencies
└── <project-files>
```

### Automatic Environment Setup

Agro automatically:
1. **Copies environment files** (`.env`, `package.json`, etc.)
2. **Installs dependencies** (`uv sync`, `npm install`)
3. **Configures port overrides** (e.g., `PORT=8001`, `PORT=8002`)
4. **Isolates virtual environments**

### Port Management

To prevent conflicts when running servers in parallel:

```bash
# Main project
PORT=8000
# Worktree t1
PORT=8001
# Worktree t2
PORT=8002
# Worktree t3
PORT=8003
```

## Branch Management

### Branch Naming Convention

Agro uses a consistent naming pattern:

```
output/<task-name>.<index>
```

Examples:
- `output/add-feature.1`
- `output/add-feature.2`
- `output/fix-bug.1`
- `output/fix-bug.2`

The prefix `output` can be configured in conf.yml with `WORKTREE_OUTPUT_BRANCH_PREFIX` variable.

When running `agro grab` the suffix `.copy` will be added to the branch name. This is purposeful behavior since git will prevent the user from checking out a branch on existing worktree, so it makes

Example: `agro grab output/add-feature.2` will checkout a branch named `output/add-feature.2.copy`.

### Branch Lifecycle

1. **Creation**: Branch created from current HEAD
2. **Development**: Agent makes commits to the branch
3. **Review**: Compare branches using `agro muster`
4. **Selection**: Choose the best solution
5. **Merge**: Integrate chosen solution to main branch
6. **Cleanup**: Delete unused branches and worktrees

### Branch Patterns

Several commands use the same cli argument type `<branch-pattern>` and the same processing for including: muster, surrender, fade, state. This is a regexp-like matching to enable high-level and fine-grain control of operations on multiple branches.

You can you braces with commas or dashes to select multiple indexes:

```
  output/add-thing              Match output/add-thing*
  output/add-thing.{2,5}        Match output/add-thing.2, output/add-thing.5
  output/add-thing.{1-4}        Match output/add-thing.1, ... output/add-thing.4
```

> 🚚 **In development**: In future versions, you likely won't need to specify the "output/" prefix.

### Branch Operations

```bash
# View all branches and the worktree they are connected to
agro state

# Switch to a branch: will checkout "output/task-name.1.copy"
agro grab output/task-name.1

# Compare the git logs of all branches for task-name
agro muster 'git log --oneline -5' 'output/task-name'

# Delete worktrees (you can't delete branches until worktrees are destroyed)
agro delete --all

# Delete branches associated with 2,3
agro fade 'output/task-name.{2,3}'

# Delete branches associated with 2,3,4
agro fade 'output/task-name.{2-4}'
```
> 💡 **Tip**: Branches can be heavy if they do lots of development setup which is why `uv` is recommended for python development since the setup occurs quickly, and uses symlinks instead of duplicating package files.

> 🚚 **In development**: In future versions, you'll be able to cleanup with one command instead of two separate commands.

## Workflow Patterns

### Sequential Development

It's prefereable to view code changes in your editor on the main git worktree instead of any the subtrees. So it is recommended you checkout each agent solution to the main work worktree branch as shown below rather than cd-ing into or opening the subtrees in your editor.

```bash
# Run single agent
agro exec add-feature

# Dont't do this: 
cd trees/t1
git diff HEAD~1

# Instead do this:
agro grab output/add-feature.1
git diff HEAD~1
# equivalent to:
# git checkout -b output/add-feature.1.copy output/add-feature.1

# Dont't do this: 
cd trees/t1
uv run pytest

# Instead do this:
agro muster 'uv run pytest' output/add-feature

# Finally, merge if satisfied
git checkout dev
git merge output/add-feature.1
```

### Parallel Development

```bash
# Run multiple agents
agro exec add-feature 3

# Compare the overall edits
agro muster 'git show --stat HEAD' output/add-feature

# Review each solution
agro grab output/add-feature.1
agro grab output/add-feature.2
agro grab output/add-feature.3

# Merge the best one
git checkout main
git merge output/add-feature.2
```

## Directory Structure

### Complete Project Layout

```
your-project/
├── .agdocs/                    # Agro configuration
│   ├── specs/                  # Task specifications
│   │   ├── task1.md
│   │   └── task2.md
│   ├── conf/                   # Configuration files
│   │   └── agro.conf.yml
│   ├── guides/                 # Development guides
│   │   └── GUIDE.md
│   └── swap/                   # Temporary files (gitignored)
├── trees/                      # Worktrees (gitignored)
│   ├── t1/                     # First worktree
│   ├── t2/                     # Second worktree
│   └── t3/                     # Third worktree
├── docs/                       # Project documentation
├── src/                        # Source code
├── tests/                      # Test files
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # Python project config
└── README.md                   # Project overview
```

---

## Key Takeaways

1. **Worktrees enable parallel development** without conflicts
2. **Task specifications guide AI agents** with clear requirements
3. **Environment isolation prevents conflicts** between parallel executions
4. **Branch naming conventions** make it easy to track and compare results
5. **Agro orchestrates the workflow** but doesn't replace good development practices

## Next Steps

- [Commands Reference](commands.md) - Learn all available commands
- [Configuration](configuration.md) - Customize Agro for your needs
- [Workflows](workflows.md) - Advanced development patterns
- [Examples](examples.md) - Practical use cases

---

> 💡 **Tip**: Start with simple tasks to understand the workflow before attempting complex multi-agent scenarios.