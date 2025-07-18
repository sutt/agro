# Configuration

Configure Agro to match your development workflow and preferences.

## Configuration File

### Location

Agro looks for configuration in this order:
1. `.agdocs/conf/agro.conf.yml` (project-specific)
2. `~/.agro/agro.conf.yml` (user-specific)
3. Built-in defaults

### Basic Configuration

Create a configuration file with `agro init --conf`:

```yaml
# .agdocs/conf/agro.conf.yml
default_agent: aider
auto_commit: true
verbose: false

agents:
  aider:
    command: "aider"
    auto_commit: true
    args: []
  claude:
    command: "claude-code"
    auto_commit: true
    args: []
  gemini:
    command: "gemini"
    auto_commit: false
    args: []

environment:
  port_start: 8000
  port_increment: 1
  env_file: ".env"
  env_example: ".env.example"

git:
  branch_prefix: "output/"
  commit_message_template: "agro: {task_name} - {agent_type}"
```

## Agent Configuration

### Default Agent

Set your preferred default agent:

```yaml
default_agent: claude  # Options: aider, claude, gemini
```

### Agent-Specific Settings

Configure each agent individually:

```yaml
agents:
  aider:
    command: "aider"
    auto_commit: true
    args: 
      - "--model"
      - "gpt-4"
      - "--no-auto-commits"
    environment:
      AIDER_NO_AUTO_COMMITS: "1"
  
  claude:
    command: "claude-code"
    auto_commit: true
    args: []
    environment:
      CLAUDE_API_KEY: "${CLAUDE_API_KEY}"
  
  gemini:
    command: "gemini"
    auto_commit: false
    args:
      - "--model"
      - "gemini-1.5-pro"
    environment:
      GEMINI_API_KEY: "${GEMINI_API_KEY}"
```

### Agent Command Resolution

When you run `agro exec task-name agent-name`, Agro:

1. Looks up the agent in the configuration
2. Uses the configured `command` and `args`
3. Applies agent-specific environment variables
4. Executes in the worktree

## Environment Configuration

### Port Management

Configure how ports are assigned to worktrees:

```yaml
environment:
  port_start: 8000      # First port number
  port_increment: 1     # Increment for each worktree
  port_override_vars:   # Environment variables to override
    - API_PORT
    - SERVER_PORT
    - PORT
```

### Environment Files

Configure how environment files are handled:

```yaml
environment:
  env_file: ".env"              # Source environment file
  env_example: ".env.example"   # Template for fresh environments
  copy_env_files:               # Additional files to copy
    - ".env.local"
    - "config.json"
```

### Virtual Environment Cloning

> **TODO**: Document virtual environment configuration

```yaml
environment:
  clone_venv: true          # Clone virtual environments
  venv_managers:            # Supported package managers
    - uv
    - pip
    - npm
    - yarn
```

## Git Configuration

### Branch Naming

Customize branch naming conventions:

```yaml
git:
  branch_prefix: "output/"      # Prefix for agent branches
  branch_template: "{prefix}{task_name}.{index}"
  # Results in: output/add-feature.1
```

### Commit Behavior

Configure automatic commits:

```yaml
git:
  auto_commit: true             # Enable auto-commits
  commit_message_template: "agro: {task_name} - {agent_type} - {timestamp}"
  commit_include_stats: true    # Include file change stats
```

### Worktree Configuration

```yaml
git:
  worktree_dir: "trees"         # Directory for worktrees
  cleanup_on_exit: true         # Clean up on process exit
  preserve_failed_runs: false   # Keep worktrees on agent failure
```

## Task Configuration

### Task File Settings

```yaml
tasks:
  specs_dir: ".agdocs/specs"    # Task specification directory
  template_file: "task-template.md"  # Template for new tasks
  editor: "${EDITOR}"           # Editor for task files
  auto_open: true               # Open task files after creation
```

### Task Templates

Create custom task templates:

```yaml
tasks:
  template_file: "custom-template.md"
```

Create `.agdocs/specs/custom-template.md`:

```markdown
# {task_name}

## Overview
Brief description of the task.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Context
Project context and constraints.

## Acceptance Criteria
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] Documentation updated

## Out of Scope
What should NOT be changed.
```

## Logging Configuration

### Verbosity Levels

```yaml
logging:
  level: INFO                   # DEBUG, INFO, WARNING, ERROR
  file: ".agdocs/swap/agro.log" # Log file location
  max_size: 10MB               # Maximum log file size
  backup_count: 5              # Number of backup log files
```

### Command Output

```yaml
logging:
  show_command_output: false    # Show agent command output
  capture_agent_logs: true      # Capture agent logs
  agent_log_dir: ".agdocs/swap/logs"
```

## Advanced Configuration

### Custom Commands

Define custom commands for specific workflows:

```yaml
custom_commands:
  test:
    command: "pytest tests/ -v"
    description: "Run project tests"
  
  lint:
    command: "ruff check src/"
    description: "Run code linting"
  
  serve:
    command: "uvicorn app:app --reload"
    description: "Start development server"
```

Use with `agro muster`:

```bash
agro muster 'pytest tests/ -v' output/add-feature
```

### Hooks

> **TODO**: Document hook configuration

Configure hooks for lifecycle events:

```yaml
hooks:
  pre_exec:
    - "echo 'Starting agent execution'"
  post_exec:
    - "echo 'Agent execution complete'"
  pre_commit:
    - "ruff check src/"
    - "pytest tests/"
  post_commit:
    - "echo 'Changes committed'"
```

## Environment Variables

### Agro-Specific Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AGRO_CONFIG` | Path to configuration file | `.agdocs/conf/agro.conf.yml` |
| `AGRO_VERBOSE` | Enable verbose output | `false` |
| `AGRO_EDITOR` | Editor for task files | `$EDITOR` |
| `AGRO_NO_AUTO_COMMIT` | Disable auto-commits | `false` |

### Agent Environment Variables

Configure agent-specific environment variables:

```yaml
agents:
  aider:
    environment:
      AIDER_MODEL: "gpt-4"
      AIDER_NO_AUTO_COMMITS: "1"
  
  claude:
    environment:
      CLAUDE_API_KEY: "${CLAUDE_API_KEY}"
      CLAUDE_MODEL: "claude-3-sonnet"
```

## Configuration Examples

### Minimal Configuration

```yaml
# Minimal setup
default_agent: claude
auto_commit: true
```

### Development Team Configuration

```yaml
# Team configuration
default_agent: aider
auto_commit: true
verbose: true

agents:
  aider:
    command: "aider"
    args: 
      - "--model"
      - "gpt-4"
      - "--no-auto-commits"
  
  claude:
    command: "claude-code"
    args: []

environment:
  port_start: 3000
  port_increment: 10

git:
  branch_prefix: "feature/"
  commit_message_template: "[{agent_type}] {task_name}: automated changes"

logging:
  level: DEBUG
  show_command_output: true
```

### Production Configuration

```yaml
# Production-ready setup
default_agent: claude
auto_commit: false
verbose: false

agents:
  claude:
    command: "claude-code"
    auto_commit: false
    args: []

environment:
  port_start: 8000
  cleanup_on_exit: true

git:
  branch_prefix: "agro/"
  preserve_failed_runs: true

logging:
  level: WARNING
  file: "/var/log/agro.log"
```

## Configuration Validation

### Validate Configuration

```bash
# Check configuration validity
agro init --conf --validate

# Show current configuration
agro config show

# Show configuration sources
agro config sources
```

> **TODO**: Add configuration validation commands

### Common Configuration Errors

| Error | Solution |
|-------|----------|
| `Invalid agent type` | Check agent name spelling in config |
| `Command not found` | Ensure agent CLI is installed |
| `Port already in use` | Adjust `port_start` or `port_increment` |
| `Permission denied` | Check file permissions on config file |

## Configuration Migration

### Upgrading Configuration

When upgrading Agro, your configuration may need updates:

```bash
# Backup current configuration
cp .agdocs/conf/agro.conf.yml .agdocs/conf/agro.conf.yml.bak

# Generate new configuration with current settings
agro init --conf --upgrade
```

> **TODO**: Document configuration migration process

---

## Next Steps

- [Agents](agents.md) - Detailed agent configuration
- [Workflows](workflows.md) - Configuration-based workflows
- [Troubleshooting](troubleshooting.md) - Configuration issues

---

> 💡 **Tip**: Start with a minimal configuration and add settings as needed. Too many options can make debugging difficult.