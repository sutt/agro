# Contributing to Agro

> ⚠️ **Warning**: Everything in this section is ai-generated and not accurate. We'll refine later.

Thank you for your interest in contributing to Agro! This guide will help you get started with development and contribution.

## Quick Start for Contributors

### Prerequisites

- Python 3.9 or higher
- Git
- uv (recommended for dependency management)
- At least one AI coding agent (aider, claude-code, or gemini)

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/agro.git
cd agro

# 2. Set up development environment
uv venv
uv sync

# 3. Install in development mode
uv pip install -e .

# 4. Verify installation
agro --version

# 5. Run tests
uv run pytest
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes
# Edit code, add tests, update documentation

# 3. Run tests
uv run pytest

# 4. Run linting
uv run ruff check src/
uv run ruff format src/

# 5. Test CLI functionality
agro init
agro task test-feature
agro exec test-feature

# 6. Commit changes
git add .
git commit -m "Add your feature"

# 7. Push and create PR
git push origin feature/your-feature-name
gh pr create --title "Add your feature"
```

## Development Guidelines

### Code Style

Agro follows standard Python conventions:

- **PEP 8**: Standard Python style guide
- **Black/Ruff**: Automated code formatting
- **Type hints**: Use type annotations where possible
- **Docstrings**: Document all public functions and classes

### Code Formatting

```bash
# Format code
uv run ruff format src/ tests/

# Check formatting
uv run ruff check src/ tests/

# Fix formatting issues
uv run ruff check --fix src/ tests/
```

### Testing

#### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_core.py

# Run with coverage
uv run pytest --cov=agro --cov-report=html

# Run integration tests
uv run pytest tests/integration/
```

#### Writing Tests

```python
# tests/test_new_feature.py
import pytest
from agro.core import new_feature

def test_new_feature():
    """Test new feature functionality."""
    result = new_feature("input")
    assert result == "expected_output"

def test_new_feature_error():
    """Test new feature error handling."""
    with pytest.raises(ValueError):
        new_feature("invalid_input")
```

### Documentation

#### Updating Documentation

```bash
# Update docs in docs/ directory
edit docs/your-section.md

# Test documentation locally
# TODO: Add documentation testing commands

# Update CLI help text
edit src/agro/cli.py
# Update argument descriptions and help text
```

#### Documentation Style

- **Clear and concise**: Use simple language
- **Examples**: Include code examples for all features
- **Warnings**: Use warning blocks for important information
- **TODO markers**: Use TODO comments for incomplete sections

Example documentation format:
```markdown
# Feature Name

Brief description of the feature.

## Usage

```bash
agro command --option value
```

## Examples

```bash
# Basic usage
agro command example

# Advanced usage
agro command --advanced-option example
```

> ⚠️ **Warning**: Important information about limitations or gotchas.

> 💡 **Tip**: Helpful tips for users.
```

## Project Structure

### Directory Layout

```
agro/
├── src/
│   └── agro/
│       ├── __init__.py     # Package initialization
│       ├── cli.py          # Command-line interface
│       ├── core.py         # Core functionality
│       ├── config.py       # Configuration management
│       └── committer.py    # Git operations
├── tests/
│   ├── test_cli.py         # CLI tests
│   ├── test_core.py        # Core functionality tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
├── .agdocs/                # Agro project files
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── README.md               # Project overview
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `cli.py` | Command-line argument parsing and dispatch |
| `core.py` | Core worktree and agent management |
| `config.py` | Configuration file handling |
| `committer.py` | Git operations and commit management |

## Contributing Areas

### High Priority

1. **Agent Support**: Add support for new AI coding agents
2. **Configuration**: Improve configuration validation and error handling
3. **Documentation**: Expand and improve documentation
4. **Testing**: Add more comprehensive tests

### Medium Priority

1. **Performance**: Optimize worktree operations
2. **Error Handling**: Better error messages and recovery
3. **Logging**: Improved logging and debugging
4. **UI/UX**: Better command-line interface

### Low Priority

1. **Plugins**: Plugin system for extensibility
2. **Web Interface**: Web-based management interface
3. **CI/CD**: Better CI/CD integration
4. **Metrics**: Usage metrics and analytics

## Adding New Features

### Adding a New Agent

1. **Research the agent**: Understand its CLI interface
2. **Add configuration**: Update `config.py` with agent defaults
3. **Test integration**: Verify agent works with Agro
4. **Add documentation**: Update `agents.md`
5. **Add tests**: Create tests for the new agent

Example agent addition:
```python
# src/agro/config.py
AGENT_CONFIG = {
    "aider": {
        "command": "aider",
        "auto_commit": True,
        "args": []
    },
    "new_agent": {
        "command": "new-agent",
        "auto_commit": True,
        "args": ["--mode", "autonomous"]
    }
}
```

### Adding a New Command

1. **Define the command**: Add to `cli.py`
2. **Implement functionality**: Add to `core.py`
3. **Add tests**: Create test cases
4. **Update documentation**: Add to `commands.md`

Example command addition:
```python
# src/agro/cli.py
parser_new_cmd = subparsers.add_parser(
    "new-cmd",
    help="Description of new command"
)
parser_new_cmd.add_argument(
    "argument",
    help="Argument description"
)
parser_new_cmd.set_defaults(
    func=lambda args: core.new_command(args.argument)
)
```

### Adding Configuration Options

1. **Define the option**: Add to configuration schema
2. **Update parsing**: Handle the new option
3. **Add validation**: Ensure option is valid
4. **Update documentation**: Add to `configuration.md`

## Testing Guidelines

### Test Coverage

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test command-line interface
- **End-to-end tests**: Test complete workflows

### Test Categories

```python
# Unit tests
def test_parse_branch_pattern():
    """Test branch pattern parsing."""
    pass

# Integration tests
def test_exec_command_cli():
    """Test exec command via CLI."""
    pass

# End-to-end tests
def test_complete_workflow():
    """Test complete agro workflow."""
    pass
```

### Mock External Dependencies

```python
# tests/test_core.py
from unittest.mock import patch, MagicMock

@patch('agro.core.subprocess.run')
def test_git_operation(mock_run):
    """Test git operations with mocked subprocess."""
    mock_run.return_value = MagicMock(returncode=0)
    result = core.git_operation()
    assert result is True
```

## Code Review Process

### Pull Request Guidelines

1. **Clear description**: Explain what the PR does and why
2. **Small changes**: Keep PRs focused and reviewable
3. **Tests included**: Add tests for new functionality
4. **Documentation updated**: Update relevant documentation
5. **No breaking changes**: Avoid breaking existing functionality

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Documentation updated
- [ ] Examples added/updated
- [ ] Help text updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes
- [ ] Changelog updated (if needed)
```

## Release Process

### Version Management

Agro uses semantic versioning (SemVer):
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes, backwards compatible

### Release Steps

> **TODO**: Document complete release process

1. **Update version**: Update `pyproject.toml`
2. **Update changelog**: Add release notes
3. **Create tag**: `git tag v0.1.6`
4. **Push tag**: `git push origin v0.1.6`
5. **Build package**: `uv build`
6. **Upload to PyPI**: `uv publish`

## Development Tools

### Useful Commands

```bash
# Development environment
uv sync                 # Install dependencies
uv run pytest         # Run tests
uv run ruff check      # Check code style
uv run ruff format     # Format code

# Testing agro functionality
agro init              # Initialize test project
agro task test-feature # Create test task
agro exec test-feature # Test execution

# Local package testing
./redeploy             # Reinstall local package
```

### IDE Setup

#### VS Code

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black"
}
```

#### PyCharm

1. Set interpreter to `.venv/bin/python`
2. Configure pytest as test runner
3. Enable ruff for linting
4. Set up run configurations for common commands

## Community

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Code of Conduct

- **Be respectful**: Treat all contributors with respect
- **Be inclusive**: Welcome contributors from all backgrounds
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together to improve Agro

### Recognition

Contributors are recognized in:
- **README**: Major contributors listed
- **Changelog**: Contributors credited for each release
- **GitHub**: Contributor graphs and statistics

## Common Development Tasks

### Setting Up Test Environment

```bash
# Create test project
mkdir agro-test
cd agro-test
git init
echo "# Test Project" > README.md
git add README.md
git commit -m "Initial commit"

# Test agro functionality
agro init
agro task test-feature
echo "Add hello world to README" > .agdocs/specs/test-feature.md
agro exec test-feature
```

### Running Integration Tests

```bash
# Run full test suite
uv run pytest tests/

# Run specific integration test
uv run pytest tests/integration/test_exec.py -v

# Run tests with coverage
uv run pytest --cov=agro --cov-report=html
open htmlcov/index.html
```

### Building Documentation

```bash
# TODO: Add documentation build process
# Generate documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Getting Help

### Resources

- **Documentation**: Read the complete documentation
- **Examples**: Check `examples.md` for working patterns
- **Tests**: Look at existing tests for examples
- **Issues**: Search existing issues for similar problems

### Asking Questions

When asking for help:

1. **Search first**: Check existing issues and documentation
2. **Provide context**: Include relevant code and configuration
3. **Be specific**: Describe exactly what you're trying to do
4. **Include environment**: Share system information and versions

### Mentoring

New contributors can get help from:
- **Maintainers**: Core team members
- **Experienced contributors**: Previous contributors
- **Documentation**: Comprehensive guides and examples

---

## Next Steps

- **Start contributing**: Pick an issue and submit a PR
- **Join discussions**: Participate in GitHub discussions
- **Share feedback**: Help improve Agro for everyone

---

> 🤝 **Welcome**: We appreciate all contributions, no matter how small. Every improvement helps make Agro better for everyone!