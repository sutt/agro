# Agro Documentation

Welcome to the Agro documentation! Agro is a powerful CLI tool for managing git worktrees and orchestrating multiple AI coding agents in parallel development workflows.

## Table of Contents

### Getting Started
- [📚 Getting Started](getting-started.md) - Installation, setup, and your first agro workflow
- [🧠 Core Concepts](core-concepts.md) - Understanding worktrees, agents, and task specifications

### Usage & Commands
- [⚡ Commands Reference](commands.md) - Complete CLI command documentation
- [⚙️ Configuration](configuration.md) - Setting up agro.conf.yml and environment variables
- [🤖 Agents](agents.md) - Supported agents and their configuration

### Advanced Usage
- [🔄 Workflows](workflows.md) - Common development patterns and best practices
- [📝 Examples](examples.md) - Practical use cases and code samples

### Reference
- [🔧 Troubleshooting](troubleshooting.md) - Common issues and solutions
- [🤝 Contributing](contributing.md) - Development guidelines and contribution process

---

## What is Agro?

Agro is a CLI wrapper that enables you to:

- **Run multiple AI coding agents in parallel** across isolated git worktrees
- **Compare different agent outputs** side-by-side for the same task
- **Manage complex development workflows** with git branches and worktrees
- **Orchestrate agent-based development** with markdown task specifications

### Key Features

- 🏗️ **Worktree Management**: Automatic creation and cleanup of git worktrees
- 🤖 **Multi-Agent Support**: Works with aider, claude-code, gemini, and more
- 📋 **Task-Based**: Markdown files define development tasks
- 🔄 **Environment Isolation**: Each worktree gets its own environment configuration
- 🌐 **Parallel Execution**: Run multiple agents simultaneously
- 📊 **Easy Comparison**: Compare results across different agents and models

### Supported Agents

| Agent | Description | Status |
|-------|-------------|---------|
| **aider** | AI pair programming assistant | ✅ Fully supported |
| **claude-code** | Anthropic's Claude CLI | ✅ Fully supported |
| **gemini** | Google's Gemini CLI | ✅ Fully supported |

### Quick Example

```bash
# Initialize agro in your project
agro init

# Create a task specification
agro task add-feature
# Edit the task file with your requirements

# Run 3 agents in parallel
agro exec add-feature 3

# Compare results across worktrees
agro state
agro muster 'npm test' output/add-feature
```

---

## Philosophy

Agro embraces the principle of **"no magic"** - it's built on standard git operations and shell commands. This means:

- ✅ **Transparency**: All operations are visible and understandable
- ✅ **Interoperability**: Works with existing git workflows and tools
- ✅ **Reliability**: Based on proven, stable technologies
- ✅ **Flexibility**: Can be customized and extended as needed

> **Note**: Agro is not an AI agent itself. It's a micro-framework that orchestrates other AI agents and simplifies the workflow for dispatching, reviewing, and comparing their outputs.

---

## Need Help?

- Check the [troubleshooting guide](troubleshooting.md) for common issues
- Review the [examples](examples.md) for practical use cases
- See the [contributing guide](contributing.md) to help improve Agro

---

> ⚠️ **Warning**: This documentation is under active development. Some sections may contain TODO markers where additional information is needed.