# Configuration

Configure Agro to match your development workflow and preferences.

## Configuration File

### Location

Agro currently looks for the  configuration in `.agdocs/conf/agro.conf.yml` and if not found falls back to all defaults.

### Create Config

Create a configuration file with `agro init --conf`. Or `agro init` will create this file along with all the other directories in and files in `.agdocs`

This will create a config file that is completely commented out which you can un-comment sections to override the defaults.

## Main Config Options

### Default Agent

To chose what agent run by default configure these commands.

```yaml
# maider.sh: local script to source the api keys and run aider
EXEC_CMD_DEFAULT: maider.sh   

# The type of agent being used. Determines how built-in flags are passed.
# Supported values: "aider", "claude", "gemini".
AGENT_TYPE: aider
```

### Agent-Specific Settings

Configure each agent individually. All the strings in `args` property will be passed to the specific agent.

```yaml
AGENT_CONFIG:
  aider:
    args: ["--yes", "--no-check-update", "--no-attribute-author", "--no-attribute-committer", "--no-attribute-co-authored-by"]
  claude:
    args: ["-d", "--allowedTools", "Write Edit MultiEdit", "--max-turns", "30", "-p"]
  gemini:
    args: ["-y"]
```

These allow you to timeout if the run is going over 10 minutes. You can turn this setting off if you set to 0.

```yaml
Agent-specific timeout settings in seconds.
A value of 0 means no timeout is applied, overriding any default.
AGENT_TIMEOUTS:
  aider: 0
  claude: 600
  gemini: 600
```

### Muster Common Commands

Define reusable commands for the `agro muster -c` functionality:

```yaml
# Default timeout in seconds for commands run with 'agro muster'.
# A value of 0 or null means no timeout.
MUSTER_DEFAULT_TIMEOUT: 20

MUSTER_COMMON_CMDS:
  testq:
    cmd: 'uv run pytest --tb=no -q'
  server-start:
    cmd: 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid'
    timeout: null  # No timeout for this command
  server-kill:
    cmd: 'kill $(cat server.pid) && rm -f server.pid server.log'
  build:
    cmd: 'npm run build'
    timeout: 300  # 5 minute timeout
  lint:
    cmd: 'npm run lint'
```

These commands can then be executed across worktrees using:

```bash
# Run quick tests in all output branches
agro muster -c testq

# Start servers in specific branches  
agro muster -c server-start output/api

# Custom build command
agro muster -c build output/frontend.{1,2}

# Override timeout for a specific run
agro muster -c testq --timeout 60 output/
```

#### Timeout Configuration

Commands can have timeouts configured at three levels (in order of precedence):

1. **CLI flag**: `--timeout <seconds>` overrides all other settings
2. **Common command config**: Individual `timeout` setting per command
3. **Global default**: `MUSTER_DEFAULT_TIMEOUT` applies to all commands without specific timeouts

Set timeout to `0` or `null` to disable timeouts entirely.

> **Tip**: Common commands support shell features like pipes, redirects, and background processes. Agro automatically detects when shell execution is needed.

### Env & Port Management

Configure how ports are assigned to worktrees:

```yaml
BASE_API_PORT: 8000   # this will be deprecated
```

Otherwise cli flags are your friend here:

```
Common options for 'make' and 'exec':
  --fresh-env         Use .env.example as the base instead of .env.
  --no-env-overrides  Do not add port overrides to the .env file.
```

### Virtual Environment Cloning

By default, aider does `uv` setup but you can add any number of commands in for the `ENV_SETUP_CMDS` that will execute after the code has been cloned in the worktree.

```yaml
ENV_SETUP_CMDS:
  - 'uv venv'
  - 'uv sync --quiet --all-extras'
```

## Git Configuration

### Branch and Worktree Naming

Customize branch and worktree naming conventions:

```yaml
WORKTREE_DIR: ./trees
WORKTREE_BRANCH_PREFIX: tree/t
WORKTREE_OUTPUT_BRANCH_PREFIX: output/
```

### Upgrading Configuration

When upgrading Agro, your configuration may need updates:

```bash
# Backup current configuration
mv .agdocs/conf/agro.conf.yml .agdocs/conf/agro.conf.yml.bak

# Generate new configuration with current settings
# if the file already exists it won't be created
agro init --conf
```

---

## Next Steps

- [Agents](agents.md) - Detailed agent configuration
- [Workflows](workflows.md) - Configuration-based workflows
- [Troubleshooting](troubleshooting.md) - Configuration issues

