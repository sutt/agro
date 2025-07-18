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

> ⚠️ **Important**: Worktrees are temporary. Always merge valuable changes back to your main branch before cleanup.

## AI Agents

### Supported Agents

| Agent | Description | Command |
|-------|-------------|---------|
| **aider** | AI pair programming with git integration | `aider` |
| **claude-code** | Anthropic's Claude CLI interface | `claude-code` |
| **gemini** | Google's Gemini CLI interface | `gemini` |

### Agent Execution

Agents run in **non-interactive mode** within worktrees:

```bash
# Agent reads task specification
# Agent modifies code files
# Agent commits changes (if auto-commit enabled)
# Agent exits when task is complete
```

### Agent Configuration

> **TODO**: Add specific configuration examples for each agent

Agents can be configured via:
- Command-line arguments
- Environment variables
- Configuration files (`.agdocs/conf/agro.conf.yml`)

### Agent Selection

Agro determines which agent to use based on:

1. **Explicit specification**: `agro exec task-name claude`
2. **Configuration file**: Default agent in `agro.conf.yml`
3. **Auto-detection**: Inferred from available commands
4. **Fallback**: `aider` (default)

## Task Specifications

### What are Task Specifications?

Task specifications are markdown files that describe development tasks for AI agents. They live in `.agdocs/specs/`.

### Task File Structure

```markdown
# Task Title

Brief description of what needs to be done.

## Requirements
- Specific requirement 1
- Specific requirement 2
- Testing requirements

## Context
Additional context about the codebase, constraints, or preferences.

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] All tests pass
```

### Task File Naming

- **Filename**: `task-name.md` (kebab-case recommended)
- **Location**: `.agdocs/specs/task-name.md`
- **Branch**: Creates `output/task-name.N` branches

### Best Practices for Task Specifications

1. **Be Specific**: Clear, actionable requirements
2. **Include Tests**: Specify how to verify success
3. **Provide Context**: Help agents understand the codebase
4. **Set Boundaries**: Define what should NOT be changed

#### Example: Good Task Specification

```markdown
# Add User Authentication

Implement basic user authentication for the web application.

## Requirements
- Add login/logout routes to the FastAPI application
- Use JWT tokens for session management
- Hash passwords with bcrypt
- Add authentication middleware
- Create user model with SQLAlchemy

## Context
- The app uses FastAPI with SQLAlchemy ORM
- Database models are in `app/models.py`
- Routes are in `app/routes.py`
- Dependencies are managed with `requirements.txt`

## Acceptance Criteria
- [ ] Users can register with email/password
- [ ] Users can login and receive JWT token
- [ ] Protected routes require valid token
- [ ] Passwords are properly hashed
- [ ] All existing tests pass
- [ ] New tests added for auth functionality

## Out of Scope
- Do not modify the database schema for existing tables
- Do not add OAuth/social login
- Do not implement password reset functionality
```

## Environment Management

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
- `output/fix-bug.2`
- `output/refactor-code.3`

### Branch Lifecycle

1. **Creation**: Branch created from current HEAD
2. **Development**: Agent makes commits to the branch
3. **Review**: Compare branches using `agro muster`
4. **Selection**: Choose the best solution
5. **Merge**: Integrate chosen solution to main branch
6. **Cleanup**: Delete unused branches

### Branch Operations

```bash
# View all branches
agro state

# Switch to a branch
agro grab output/task-name.1

# Compare branches
agro muster 'git log --oneline -5' 'output/task-name'

# Delete branches
agro fade 'output/task-name.{2,3}'
```

## Workflow Patterns

### Sequential Development

```bash
# Run single agent
agro exec add-feature

# Review results
cd trees/t1
git diff HEAD~1

# Merge if satisfied
git checkout main
git merge output/add-feature.1
```

### Parallel Development

```bash
# Run multiple agents
agro exec add-feature 3

# Compare results
agro muster 'npm test' 'output/add-feature'

# Review each solution
agro grab output/add-feature.1
agro grab output/add-feature.2
agro grab output/add-feature.3

# Merge the best one
git checkout main
git merge output/add-feature.2
```

### Iterative Development

```bash
# First iteration
agro exec add-feature

# Refine task specification
edit .agdocs/specs/add-feature.md

# Second iteration
agro exec add-feature

# Compare iterations
agro muster 'git log --oneline -5' 'output/add-feature'
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