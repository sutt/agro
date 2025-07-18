# Supported Agents

Agro supports multiple AI coding agents, each with unique strengths and configuration options.

## Overview

| Agent | Description | Best For | Status |
|-------|-------------|----------|--------|
| [**aider**](#aider) | AI pair programming with git integration | Code editing, refactoring | ✅ Full support |
| [**claude-code**](#claude-code) | Anthropic's CLI interface | Complex reasoning, documentation | ✅ Full support |
| [**gemini**](#gemini) | Google's coding assistant | Multi-modal tasks, analysis | ✅ Full support |

## Agent Installation

### Prerequisites

Before using any agent, ensure you have:
- Python 3.9+ installed
- Git configured
- API keys for your chosen agents

### Installation Commands

```bash
# Install aider
pip install aider-chat

# Install claude-code
pip install anthropic-tools

# Install gemini CLI
pip install google-generativeai
```

> **TODO**: Verify exact installation commands for each agent

## aider

### Overview

Aider is an AI pair programming tool that works directly with git repositories. It excels at making targeted code changes while maintaining git history.

### Installation

```bash
pip install aider-chat
```

### Configuration

```yaml
# .agdocs/conf/agro.conf.yml
agents:
  aider:
    command: "aider"
    auto_commit: true
    args:
      - "--model"
      - "gpt-4"
      - "--no-auto-commits"
    environment:
      OPENAI_API_KEY: "${OPENAI_API_KEY}"
      AIDER_NO_AUTO_COMMITS: "1"
```

### Supported Models

| Model | Provider | Configuration |
|-------|----------|---------------|
| GPT-4 | OpenAI | `--model gpt-4` |
| GPT-3.5 | OpenAI | `--model gpt-3.5-turbo` |
| Claude | Anthropic | `--model claude-3-sonnet` |
| Gemini | Google | `--model gemini-1.5-pro` |

### Common Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--model` | Specify model to use | `--model gpt-4` |
| `--no-auto-commits` | Disable automatic commits | `--no-auto-commits` |
| `--yes` | Auto-accept all changes | `--yes` |
| `--message` | Custom commit message | `--message "Add feature"` |
| `--files` | Specify files to edit | `--files src/main.py` |

### Example Configuration

```yaml
agents:
  aider:
    command: "aider"
    auto_commit: true
    args:
      - "--model"
      - "gpt-4"
      - "--no-auto-commits"
      - "--yes"
    environment:
      OPENAI_API_KEY: "${OPENAI_API_KEY}"
```

### Best Practices

- **Use with git**: Aider works best in git repositories
- **Specify files**: Use `--files` to focus on specific files
- **Review changes**: Always review aider's changes before accepting
- **Model selection**: GPT-4 generally provides better results than GPT-3.5

---

## claude-code

### Overview

Claude Code is Anthropic's CLI interface for code generation and editing. It excels at complex reasoning tasks and generating comprehensive documentation.

### Installation

```bash
# TODO: Add correct installation command
pip install anthropic-tools
```

### Configuration

```yaml
# .agdocs/conf/agro.conf.yml
agents:
  claude:
    command: "claude-code"
    auto_commit: true
    args: []
    environment:
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
```

### Supported Models

| Model | Description | Configuration |
|-------|-------------|---------------|
| Claude 3 Sonnet | Balanced performance | Default |
| Claude 3 Opus | Highest capability | `--model claude-3-opus` |
| Claude 3 Haiku | Fastest responses | `--model claude-3-haiku` |

### Common Arguments

> **TODO**: Document claude-code specific arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--model` | Specify Claude model | `--model claude-3-opus` |
| `--max-tokens` | Maximum response length | `--max-tokens 4000` |
| `--temperature` | Response creativity | `--temperature 0.7` |

### Example Configuration

```yaml
agents:
  claude:
    command: "claude-code"
    auto_commit: true
    args:
      - "--model"
      - "claude-3-sonnet"
      - "--max-tokens"
      - "4000"
    environment:
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
```

### Best Practices

- **Complex tasks**: Use Claude for complex reasoning and analysis
- **Documentation**: Excellent for generating comprehensive docs
- **Code review**: Good for explaining and reviewing code changes
- **Multi-step tasks**: Handles complex multi-step workflows well

---

## gemini

### Overview

Google's Gemini CLI provides access to Google's advanced AI models with strong multi-modal capabilities.

### Installation

```bash
# TODO: Add correct installation command
pip install google-generativeai
```

### Configuration

```yaml
# .agdocs/conf/agro.conf.yml
agents:
  gemini:
    command: "gemini"
    auto_commit: false
    args:
      - "--model"
      - "gemini-1.5-pro"
    environment:
      GOOGLE_API_KEY: "${GOOGLE_API_KEY}"
```

### Supported Models

| Model | Description | Configuration |
|-------|-------------|---------------|
| Gemini 1.5 Pro | Advanced reasoning | `--model gemini-1.5-pro` |
| Gemini 1.5 Flash | Fast responses | `--model gemini-1.5-flash` |
| Gemini 1.0 Pro | Stable version | `--model gemini-1.0-pro` |

### Common Arguments

> **TODO**: Document gemini CLI specific arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--model` | Specify Gemini model | `--model gemini-1.5-pro` |
| `--temperature` | Response creativity | `--temperature 0.7` |
| `--max-output-tokens` | Maximum response length | `--max-output-tokens 2048` |

### Example Configuration

```yaml
agents:
  gemini:
    command: "gemini"
    auto_commit: false
    args:
      - "--model"
      - "gemini-1.5-pro"
      - "--temperature"
      - "0.3"
    environment:
      GOOGLE_API_KEY: "${GOOGLE_API_KEY}"
```

### Best Practices

- **Multi-modal tasks**: Use for tasks involving images or complex data
- **Analysis**: Good for code analysis and explanation
- **Fast iteration**: Gemini Flash is good for quick iterations
- **Complex reasoning**: Gemini Pro handles complex logical tasks well

---

## Custom Agents

### Adding New Agents

You can add support for custom agents by configuring them in `agro.conf.yml`:

```yaml
agents:
  custom_agent:
    command: "my-custom-agent"
    auto_commit: true
    args:
      - "--task-file"
      - "{task_file}"
      - "--output-dir"
      - "{worktree_path}"
    environment:
      CUSTOM_API_KEY: "${CUSTOM_API_KEY}"
```

### Agent Requirements

For an agent to work with Agro, it must:

1. **Accept file input**: Read task specifications from files
2. **Work in directories**: Operate within the worktree directory
3. **Exit cleanly**: Exit with appropriate status codes
4. **Respect file permissions**: Not modify files outside the worktree

### Template Variables

Agro provides these template variables for agent configuration:

| Variable | Description | Example |
|----------|-------------|---------|
| `{task_file}` | Path to task specification | `.agdocs/specs/add-feature.md` |
| `{worktree_path}` | Path to worktree | `trees/t1` |
| `{branch_name}` | Current branch name | `output/add-feature.1` |
| `{agent_type}` | Agent type | `aider` |
| `{index}` | Worktree index | `1` |

---

## Agent Comparison

### Performance Characteristics

| Feature | aider | claude-code | gemini |
|---------|-------|-------------|--------|
| **Code editing** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Git integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Complex reasoning** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Multi-modal** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### Use Case Recommendations

| Use Case | Recommended Agent | Rationale |
|----------|-------------------|-----------|
| **Code refactoring** | aider | Excellent git integration and code editing |
| **Documentation** | claude-code | Superior reasoning and writing capabilities |
| **Bug fixing** | aider | Focused code editing with git history |
| **Architecture design** | claude-code | Complex reasoning and planning |
| **Quick prototypes** | gemini | Fast iteration and broad capabilities |
| **Multi-modal tasks** | gemini | Image analysis and complex data handling |

---

## Troubleshooting Agents

### Common Issues

#### Agent Not Found

```bash
Error: Command 'aider' not found
```

**Solution**: Install the agent CLI:
```bash
pip install aider-chat
```

#### API Key Issues

```bash
Error: Invalid API key
```

**Solution**: Set environment variables:
```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
```

#### Permission Denied

```bash
Error: Permission denied accessing file
```

**Solution**: Check file permissions and ensure the agent has access to the worktree directory.

#### Agent Timeouts

```bash
Error: Agent process timed out
```

**Solution**: Increase timeout or simplify the task specification.

### Debugging Agent Issues

1. **Check agent installation**:
   ```bash
   which aider
   aider --version
   ```

2. **Test agent manually**:
   ```bash
   cd trees/t1
   aider --help
   ```

3. **Check environment variables**:
   ```bash
   echo $OPENAI_API_KEY
   echo $ANTHROPIC_API_KEY
   ```

4. **Enable verbose logging**:
   ```bash
   agro -vv exec task-name
   ```

---

## Agent Updates

### Keeping Agents Updated

```bash
# Update aider
pip install --upgrade aider-chat

# Update claude-code
pip install --upgrade anthropic-tools

# Update gemini
pip install --upgrade google-generativeai
```

### Version Compatibility

> **TODO**: Document version compatibility matrix

Agro is tested with these agent versions:
- aider: 0.35.0+
- claude-code: 1.0.0+
- gemini: 1.5.0+

---

## Next Steps

- [Workflows](workflows.md) - Agent-specific workflow patterns
- [Examples](examples.md) - Real-world agent usage examples
- [Troubleshooting](troubleshooting.md) - Solving agent-related issues

---

> 💡 **Tip**: Start with one agent and gradually experiment with others as you become comfortable with the workflow.