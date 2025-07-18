# Getting Started with Agro

This guide will walk you through installing Agro and running your first agent-based development workflow.

## Installation

### Prerequisites

- Python 3.9 or higher
- Git (for worktree management)
- At least one AI coding agent installed (aider, claude-code, or gemini)

### Install Agro

Choose one of the following installation methods:

#### Option 1: Install with pip
```bash
pip install agro
```

#### Option 2: Install with uv (recommended)
```bash
uv tool install agro
```

#### Option 3: Local Development Install
```bash
git clone https://github.com/sutt/agro.git
cd agro
uv tool install . --no-cache
```

For local development, use the `./redeploy` script to reinstall after making changes.

### Verify Installation

```bash
agro --version
```

## Quick Start

### 1. Initialize Your Project

Navigate to your project directory and initialize Agro:

```bash
cd your-project
agro init
```

This creates the `.agdocs/` directory structure:
```
.agdocs/
├── specs/          # Task specification files
├── conf/           # Configuration files
├── guides/         # Development guides
└── swap/           # Temporary files (gitignored)
```

### 2. Create Your First Task

Create a task specification file:

```bash
agro task hello-world
```

This opens a new file `.agdocs/specs/hello-world.md` in your editor. Add your task description:

```markdown
# Hello World Task

Add a "Hello, World!" message to the main README.md file.

## Requirements
- Add the message as a new section
- Include proper markdown formatting
- Ensure the existing content is preserved
```

### 3. Run Your First Agent

Execute the task with a single agent:

```bash
agro exec hello-world
```

Agro will:
1. Create a new git worktree in `trees/t1/`
2. Create a branch `output/hello-world.1`
3. Launch your configured agent (aider by default)
4. Execute the task specification

### 4. Review the Results

Check the agent's progress:

```bash
# View worktree status
agro state

# Check the changes
cd trees/t1
git diff HEAD~1
```

## Your First Multi-Agent Workflow

### 1. Run Multiple Agents in Parallel

Run the same task with 3 agents:

```bash
agro exec hello-world 3
```

This creates:
- `trees/t1/` → `output/hello-world.1`
- `trees/t2/` → `output/hello-world.2`
- `trees/t3/` → `output/hello-world.3`

### 2. Compare Agent Outputs

Use the `muster` command to run commands across all worktrees:

```bash
# Run tests in all worktrees
agro muster 'npm test' 'output/hello-world'

# Check git status in all worktrees
agro muster 'git status' 'output/hello-world'

# Compare the README files
agro muster 'head -20 README.md' 'output/hello-world'
```

### 3. Select the Best Solution

After reviewing the outputs, you can:

1. **Merge the best solution**:
   ```bash
   # Switch to the best branch
   agro grab output/hello-world.2
   
   # Merge to main
   git checkout main
   git merge output/hello-world.2
   ```

2. **Clean up branches**:
   ```bash
   # Delete specific branches
   agro fade 'output/hello-world.{1,3}'
   
   # Or delete all worktrees
   agro delete --all
   ```

## Demo Project

For a more comprehensive example, try the demo project:

```bash
git clone https://github.com/sutt/agro-demo.git
cd agro-demo
uv sync

# Launch multiple agents
agro exec add-about 2        # 2 aider agents
agro exec add-about claude   # 1 claude agent
agro exec add-about gemini   # 1 gemini agent

# Run servers in parallel
agro muster --server 'uv run python app/main.py' output

# Test the results
curl http://localhost:8001/about
curl http://localhost:8002/about
curl http://localhost:8003/about
curl http://localhost:8004/about

# Clean up
agro muster --kill-server '' output
```

## Common Commands

| Command | Description |
|---------|-------------|
| `agro init` | Initialize project structure |
| `agro task <name>` | Create a new task specification |
| `agro exec <task> [count]` | Run agents on a task |
| `agro state` | Show worktree status |
| `agro muster '<cmd>' <pattern>` | Run command in matching worktrees |
| `agro grab <branch>` | Switch to a branch |
| `agro fade <pattern>` | Delete branches matching pattern |
| `agro delete --all` | Delete all worktrees |

## Environment Setup

### Agent Configuration

> **TODO**: Add specific configuration examples for each agent type

Agro supports multiple agents. Configure your preferred agent in `.agdocs/conf/agro.conf.yml`:

```yaml
# Example configuration
default_agent: aider
agents:
  aider:
    command: "aider"
    auto_commit: true
  claude:
    command: "claude-code"
    auto_commit: true
```

### Environment Variables

Agro automatically manages environment variables for parallel execution:

- **Port isolation**: Each worktree gets unique port assignments
- **Environment cloning**: Virtual environments are cloned per worktree
- **Configuration overrides**: `.env` files are customized per worktree

## Next Steps

Now that you have Agro running, explore:

- [Core Concepts](core-concepts.md) - Understand worktrees, agents, and tasks
- [Commands Reference](commands.md) - Complete CLI documentation
- [Configuration](configuration.md) - Customize Agro for your workflow
- [Workflows](workflows.md) - Advanced development patterns

---

> ⚠️ **Warning**: If you encounter issues, check the [troubleshooting guide](troubleshooting.md) for common solutions.