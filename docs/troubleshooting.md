# Troubleshooting

Common issues and solutions when using Agro for agent-based development.

## Quick Diagnostics

### Check System Status

```bash
# Check Agro installation
agro --version

# Check agent installations
which aider
which claude-code
which gemini

# Check git repository
git status
git branch -a

# Check worktree status
agro state
```

### Common Commands for Debugging

```bash
# Verbose output
agro -vv exec task-name

# Check configuration
cat .agdocs/conf/agro.conf.yml

# View logs
tail -f .agdocs/swap/logs/t1.log

# Kill all agents
agro surrender

# Clean up all worktrees
agro delete --all
```

---

## Installation Issues

### Agro Installation Failed

**Error**: `pip install agro` fails

**Common Causes**:
- Python version too old
- Missing dependencies
- Network connectivity issues

**Solutions**:
```bash
# Check Python version
python --version  # Should be 3.9+

# Update pip
pip install --upgrade pip

# Install with verbose output
pip install -v agro

# Try uv instead
uv tool install agro
```

### Agent Installation Issues

**Error**: `Command 'aider' not found`

**Solutions**:
```bash
# Install aider
pip install aider-chat

# Add to PATH if needed
export PATH=$PATH:~/.local/bin

# Check installation
aider --version
```

**Error**: `Command 'claude-code' not found`

**Solutions**:
```bash
# TODO: Add correct claude-code installation
pip install anthropic-tools

# Verify installation
claude-code --version
```

---

## Configuration Issues

### Configuration File Not Found

**Error**: `Configuration file not found`

**Solutions**:
```bash
# Create configuration
agro init --conf

# Check configuration location
ls .agdocs/conf/agro.conf.yml

# Use custom configuration
export AGRO_CONFIG=/path/to/custom/config.yml
```

### Invalid Configuration

**Error**: `Invalid configuration: agent 'xyz' not found`

**Solutions**:
```bash
# Check available agents
agro --help

# Verify agent is installed
which aider
which claude-code
which gemini

# Fix configuration
edit .agdocs/conf/agro.conf.yml
```

### Environment Variables Not Set

**Error**: `API key not found`

**Solutions**:
```bash
# Set API keys
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"

# Add to shell profile
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Verify environment
echo $OPENAI_API_KEY
```

---

## Git and Worktree Issues

### Git Repository Not Found

**Error**: `Not a git repository`

**Solutions**:
```bash
# Initialize git repository
git init

# Check git status
git status

# Make initial commit
git add .
git commit -m "Initial commit"
```

### Worktree Creation Failed

**Error**: `Failed to create worktree`

**Common Causes**:
- Insufficient disk space
- Permission issues
- Branch already exists

**Solutions**:
```bash
# Check disk space
df -h

# Check permissions
ls -la trees/

# Clean up existing worktrees
agro delete --all

# Force clean git worktrees
git worktree prune
```

### Branch Already Exists

**Error**: `Branch 'output/task-name.1' already exists`

**Solutions**:
```bash
# List existing branches
git branch -a

# Delete existing branch
git branch -d output/task-name.1

# Or use fade command
agro fade 'output/task-name.*'

# Force delete if needed
git branch -D output/task-name.1
```

---

## Agent Execution Issues

### Agent Process Failed

**Error**: `Agent process exited with code 1`

**Solutions**:
```bash
# Check agent logs
tail -f .agdocs/swap/logs/t1.log

# Test agent manually
cd trees/t1
aider --help

# Check task specification
cat .agdocs/specs/task-name.md

# Run with verbose output
agro -vv exec task-name
```

### Agent Timeout

**Error**: `Agent process timed out`

**Solutions**:
```bash
# Increase timeout in configuration
edit .agdocs/conf/agro.conf.yml
# Add: timeout: 1800  # 30 minutes

# Simplify task specification
edit .agdocs/specs/task-name.md

# Kill stuck processes
agro surrender
```

### Agent Permission Denied

**Error**: `Permission denied`

**Solutions**:
```bash
# Check file permissions
ls -la trees/t1/

# Fix permissions
chmod -R 755 trees/

# Check user ownership
sudo chown -R $(whoami) trees/
```

---

## Network and API Issues

### API Rate Limits

**Error**: `API rate limit exceeded`

**Solutions**:
```bash
# Wait for rate limit reset
sleep 60

# Use different model
agro exec task-name aider -- --model gpt-3.5-turbo

# Configure rate limiting
edit .agdocs/conf/agro.conf.yml
# Add rate limiting configuration
```

### Network Connectivity

**Error**: `Failed to connect to API`

**Solutions**:
```bash
# Check internet connectivity
ping api.openai.com
ping api.anthropic.com

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Test API directly
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

### Invalid API Keys

**Error**: `Invalid API key`

**Solutions**:
```bash
# Check API key format
echo $OPENAI_API_KEY | wc -c  # Should be ~51 characters

# Regenerate API key
# Visit https://platform.openai.com/api-keys

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

---

## Performance Issues

### Slow Agent Execution

**Symptoms**: Agents taking too long to complete tasks

**Solutions**:
```bash
# Use faster models
agro exec task-name aider -- --model gpt-3.5-turbo
agro exec task-name gemini -- --model gemini-1.5-flash

# Simplify task specifications
edit .agdocs/specs/task-name.md
# Make requirements more specific and focused

# Check system resources
top
df -h
```

### High Memory Usage

**Symptoms**: System running out of memory

**Solutions**:
```bash
# Limit concurrent agents
agro exec task-name 1  # Instead of 3

# Clean up unused worktrees
agro delete --all

# Check memory usage
free -h
ps aux | grep aider
```

### Disk Space Issues

**Error**: `No space left on device`

**Solutions**:
```bash
# Check disk usage
df -h
du -sh trees/

# Clean up worktrees
agro delete --all

# Clean up git objects
git gc --aggressive

# Clean up temporary files
rm -rf .agdocs/swap/logs/*
```

---

## Task Specification Issues

### Vague Task Specifications

**Problem**: Agents producing unexpected results

**Solutions**:
```bash
# Review task specification
cat .agdocs/specs/task-name.md

# Add specific requirements
edit .agdocs/specs/task-name.md
# Add:
# - Specific acceptance criteria
# - File paths to modify
# - Test requirements
# - Constraints

# Example improvement:
# Before: "Add authentication"
# After: "Add JWT authentication to /api/auth endpoint with login/logout routes"
```

### Conflicting Requirements

**Problem**: Agents unable to complete tasks

**Solutions**:
```bash
# Simplify task
edit .agdocs/specs/task-name.md
# Remove conflicting requirements
# Break into smaller tasks

# Create separate tasks
agro task auth-backend
agro task auth-frontend
agro task auth-tests
```

---

## Environment Issues

### Port Conflicts

**Error**: `Port 8001 already in use`

**Solutions**:
```bash
# Check port usage
lsof -i :8001
netstat -tlnp | grep 8001

# Kill processes using port
kill $(lsof -t -i:8001)

# Configure different port range
edit .agdocs/conf/agro.conf.yml
# Change port_start: 9000

# Kill all servers
agro muster --kill-server '' 'output/*'
```

### Virtual Environment Issues

**Error**: `Virtual environment not found`

**Solutions**:
```bash
# Check virtual environment
ls -la .venv/

# Recreate virtual environment
rm -rf .venv/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Use uv instead
uv venv
uv sync
```

### Environment Variable Conflicts

**Problem**: Incorrect environment variables in worktrees

**Solutions**:
```bash
# Check environment files
agro muster 'cat .env' 'output/task-name'

# Reset environment
agro delete --all
agro make 1 --fresh-env

# Check environment override
cat .agdocs/conf/agro.conf.yml
# Look for environment section
```

---

## Recovery Procedures

### Complete Reset

When everything is broken:

```bash
# 1. Stop all agents
agro surrender

# 2. Delete all worktrees
agro delete --all

# 3. Clean up git
git worktree prune
git gc

# 4. Reset configuration
rm -rf .agdocs/
agro init

# 5. Verify installation
agro --version
which aider
```

### Partial Reset

When only some components are broken:

```bash
# Reset specific worktrees
agro delete 1,2,3

# Reset specific branches
agro fade 'output/problematic-task.*'

# Reset configuration
rm .agdocs/conf/agro.conf.yml
agro init --conf
```

### Emergency Stop

When agents are misbehaving:

```bash
# Kill all agent processes
agro surrender

# Force kill if needed
pkill -f aider
pkill -f claude-code
pkill -f gemini

# Clean up background servers
agro muster --kill-server '' 'output/*'
```

---

## Debugging Tools

### Enable Debug Logging

```bash
# Verbose output
agro -vv exec task-name

# Environment variable
export AGRO_VERBOSE=1
agro exec task-name

# Configuration file
edit .agdocs/conf/agro.conf.yml
# Add: verbose: true
```

### Check System State

```bash
# Agro state
agro state

# Git state
git status
git branch -a
git worktree list

# Process state
ps aux | grep -E '(aider|claude|gemini)'

# Network state
ss -tlnp | grep -E '(8001|8002|8003)'
```

### Log Analysis

```bash
# View agent logs
tail -f .agdocs/swap/logs/t1.log

# View all logs
ls -la .agdocs/swap/logs/

# Search logs for errors
grep -i error .agdocs/swap/logs/*.log

# View system logs
journalctl -u agro  # If running as service
```

---

## Getting Help

### Community Resources

- **GitHub Issues**: https://github.com/sutt/agro/issues
- **Documentation**: Check this troubleshooting guide
- **Examples**: See [examples.md](examples.md) for working patterns

### Reporting Issues

When reporting issues, include:

1. **System information**:
   ```bash
   agro --version
   python --version
   git --version
   uname -a
   ```

2. **Error messages**:
   ```bash
   agro -vv exec task-name 2>&1 | tee error.log
   ```

3. **Configuration**:
   ```bash
   cat .agdocs/conf/agro.conf.yml
   ```

4. **Reproduction steps**:
   - Clear steps to reproduce the issue
   - Task specification content
   - Expected vs actual behavior

### Creating Minimal Examples

```bash
# Create minimal reproduction
mkdir agro-issue-reproduction
cd agro-issue-reproduction
git init
echo "# Test" > README.md
git add README.md
git commit -m "Initial commit"

# Initialize agro
agro init

# Create minimal task
echo "Add hello world to README" > .agdocs/specs/test-task.md

# Try to reproduce issue
agro exec test-task
```

---

## Prevention Tips

### Regular Maintenance

```bash
# Weekly cleanup
agro delete --all
git worktree prune

# Update agents
pip install --upgrade aider-chat
pip install --upgrade anthropic-tools

# Check configuration
agro init --conf --validate  # TODO: Add validation
```

### Best Practices

1. **Start simple**: Begin with basic workflows
2. **Test locally**: Verify agents work manually first
3. **Monitor resources**: Keep an eye on disk space and memory
4. **Regular backups**: Commit important changes frequently
5. **Document issues**: Keep notes on problems and solutions

---

## Next Steps

- [Examples](examples.md) - See working examples
- [Contributing](contributing.md) - Help improve Agro
- [Workflows](workflows.md) - Learn effective patterns

---

> 🆘 **Emergency**: If you're completely stuck, try the [Complete Reset](#complete-reset) procedure and start fresh.