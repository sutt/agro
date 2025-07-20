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


## aider

### Overview

Aider is an AI pair programming tool that works directly with git repositories. It excels at making targeted code changes while maintaining git history.

### Installation

```bash
pip install aider-chat
```

or 

```bash
uv tool install aider-chat
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
| `--yes` | Auto-accept add any file in repo to chat | `--yes` |
| `--no-attribute-co-authored-by` | don't add "aider" as author on git commit | `--yes` |

## claude-code

### Overview

Claude Code is Anthropic's CLI interface for code generation and editing. It excels at complex reasoning tasks and generating comprehensive documentation.

### Installation

Follow the instruction here ot install with npm: https://docs.anthropic.com/en/docs/claude-code/setup

### Common Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--allowedTools` | Specify Claude model | `--allowedTools", "Write Edit MultiEdit"` |
| `--max-turns` | Maximum amount of reasoning steps | `--max-turns 30` |
| `--dangerously-skip-permissions` | total YOLO mode | `--dangerously-skip-permissions` |

---

## gemini

### Overview

Google's Gemini CLI provides access to Google's advanced AI models with strong multi-modal capabilities.

### Installation

Follow insturctions here to install with npm: https://github.com/google-gemini/gemini-cli?tab=readme-ov-file#quickstart


### Common Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-y` | YOLO mode | `--model gemini-1.5-pro` |

---

## Agent Comparison

### Performance Characteristics

> These are ai-generated, not sure we totally vouch for it 

| Feature | aider | claude-code | gemini |
|---------|-------|-------------|--------|
| **Code editing** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Git integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Complex reasoning** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Multi-modal** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### Use Case Recommendations

> These are ai-generated, not sure we totally vouch for it 

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



### Version Compatibility

Agro is tested with these agent versions:
- aider: 0.85.1+
- claude-code: 1.0.53+
- gemini: 0.1.7+

---

## Next Steps

- [Workflows](workflows.md) - Agent-specific workflow patterns
- [Examples](examples.md) - Real-world agent usage examples
- [Troubleshooting](troubleshooting.md) - Solving agent-related issues

---

