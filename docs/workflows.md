# Workflows

Common development patterns and workflows using Agro for agent-based development.

## Overview

This guide covers proven workflows for different development scenarios, from simple feature development to complex multi-agent comparisons.

## Basic Workflows

### Single Agent Development

The simplest workflow for testing ideas quickly:

```bash
# 1. Create task specification
agro task add-login

# 2. Run single agent
agro exec add-login

# 3. Review results
cd trees/t1
git diff HEAD~1

# 4. Merge if satisfied
git checkout main
git merge output/add-login.1

# 5. Clean up
agro delete 1
```

**When to use**: Quick prototyping, simple features, learning Agro.

### Multi-Agent Comparison

Compare different agents on the same task:

```bash
# 1. Create task specification
agro task optimize-performance

# 2. Run multiple agents
agro exec optimize-performance aider   # Agent 1
agro exec optimize-performance claude  # Agent 2
agro exec optimize-performance gemini  # Agent 3

# 3. Compare results
agro state
agro muster 'npm test' 'output/optimize-performance'
agro muster 'npm run benchmark' 'output/optimize-performance'

# 4. Review each solution
agro grab output/optimize-performance.1
agro grab output/optimize-performance.2
agro grab output/optimize-performance.3

# 5. Merge the best solution
git checkout main
git merge output/optimize-performance.2

# 6. Clean up
agro fade 'output/optimize-performance.*'
```

**When to use**: Complex features, critical changes, exploring different approaches.

### Parallel Development

Run multiple agents simultaneously:

```bash
# 1. Create task specification
agro task refactor-api

# 2. Run 3 agents in parallel
agro exec refactor-api 3

# 3. Monitor progress
agro state
agro surrender  # Kill if needed

# 4. Compare when complete
agro muster 'git log --oneline -5' 'output/refactor-api'
agro muster 'python -m pytest tests/test_api.py' 'output/refactor-api'
```

**When to use**: Exploring multiple approaches, time-constrained development.

## Advanced Workflows

### Iterative Development

Refine solutions through multiple iterations:

```bash
# Iteration 1: Initial implementation
agro task add-auth
agro exec add-auth

# Review and refine task specification
edit .agdocs/specs/add-auth.md

# Iteration 2: Improved implementation
agro exec add-auth  # Creates new worktree

# Compare iterations
agro muster 'git diff HEAD~3..HEAD' 'output/add-auth'

# Select best approach
git checkout main
git merge output/add-auth.2
```

**When to use**: Complex features, learning from initial attempts, progressive refinement.

### Feature Branch Workflow

Integrate Agro with git flow:

```bash
# 1. Create feature branch
git checkout -b feature/user-dashboard

# 2. Create task specification
agro task user-dashboard

# 3. Run agents on feature branch
agro exec user-dashboard 2

# 4. Test and compare
agro muster 'npm test' 'output/user-dashboard'
agro muster 'npm run e2e' 'output/user-dashboard'

# 5. Merge best solution to feature branch
git merge output/user-dashboard.1

# 6. Create PR to main
git push origin feature/user-dashboard
gh pr create --title "Add user dashboard"

# 7. Clean up
agro delete --all
```

**When to use**: Team development, code review processes, CI/CD integration.

### Testing-Driven Development

Use agents to implement test-driven workflows:

```bash
# 1. Create task with tests first
agro task api-validation
# Task spec: "Write tests for API validation, then implement"

# 2. Run agent focused on testing
agro exec api-validation aider -- --model gpt-4

# 3. Review tests
cd trees/t1
npm test

# 4. Create implementation task
agro task implement-api-validation
# Task spec: "Implement API validation to pass the existing tests"

# 5. Run implementation
agro exec implement-api-validation

# 6. Verify implementation
cd trees/t2
npm test
```

**When to use**: Quality-focused development, complex business logic, regression prevention.

## Domain-Specific Workflows

### Web Development

Typical web development workflow:

```bash
# 1. Frontend component
agro task user-profile-component
agro exec user-profile-component claude

# 2. Backend API
agro task user-profile-api
agro exec user-profile-api aider

# 3. Integration tests
agro task user-profile-integration
agro exec user-profile-integration

# 4. Run all tests
agro muster 'npm run test:unit' 'output/user-profile-component'
agro muster 'npm run test:api' 'output/user-profile-api'
agro muster 'npm run test:integration' 'output/user-profile-integration'

# 5. Start development servers
agro muster --server 'npm run dev' 'output/user-profile'

# 6. Manual testing
open http://localhost:3001
open http://localhost:3002
open http://localhost:3003

# 7. Select best implementations
agro grab output/user-profile-component.1
agro grab output/user-profile-api.1
```

### Data Science

Data science and analysis workflow:

```bash
# 1. Data exploration
agro task explore-sales-data
agro exec explore-sales-data gemini

# 2. Model development
agro task sales-prediction-model
agro exec sales-prediction-model claude

# 3. Visualization
agro task sales-dashboard
agro exec sales-dashboard aider

# 4. Compare approaches
agro muster 'python -m pytest tests/test_model.py' 'output/sales'
agro muster 'python analysis.py' 'output/sales'

# 5. Start jupyter servers
agro muster --server 'jupyter lab --port=8888' 'output/sales'
```

### DevOps and Infrastructure

Infrastructure and configuration management:

```bash
# 1. Docker configuration
agro task containerize-app
agro exec containerize-app aider

# 2. CI/CD pipeline
agro task github-actions-ci
agro exec github-actions-ci claude

# 3. Monitoring setup
agro task monitoring-setup
agro exec monitoring-setup

# 4. Test configurations
agro muster 'docker build -t test-app .' 'output/containerize-app'
agro muster 'docker run --rm test-app npm test' 'output/containerize-app'
```

## Team Workflows

### Code Review Workflow

Systematic code review using agents:

```bash
# 1. Developer creates task
agro task payment-processing

# 2. Multiple developers run agents
# Developer A
agro exec payment-processing aider

# Developer B
agro exec payment-processing claude

# 3. Team review session
agro state
agro muster 'git log --oneline -10' 'output/payment-processing'

# 4. Collaborative selection
# Team discusses and selects best approach
git checkout main
git merge output/payment-processing.2

# 5. Share learnings
# Document insights in task specification
edit .agdocs/specs/payment-processing.md
```

### Learning and Experimentation

Use Agro for learning new technologies:

```bash
# 1. Learning task
agro task learn-graphql-subscriptions

# 2. Try different approaches
agro exec learn-graphql-subscriptions aider
agro exec learn-graphql-subscriptions claude
agro exec learn-graphql-subscriptions gemini

# 3. Compare learning outcomes
agro muster 'npm run demo' 'output/learn-graphql-subscriptions'
agro muster 'cat README.md' 'output/learn-graphql-subscriptions'

# 4. Create learning documentation
agro task document-graphql-learnings
echo "Document key insights from GraphQL experimentation" > .agdocs/specs/document-graphql-learnings.md
agro exec document-graphql-learnings claude
```

## Environment-Specific Workflows

### Development Environment

Local development with hot reload:

```bash
# 1. Development task
agro task add-user-settings

# 2. Run with development configuration
agro exec add-user-settings --fresh-env

# 3. Start development servers
agro muster --server 'npm run dev' 'output/add-user-settings'

# 4. Live testing
curl http://localhost:3001/api/health
curl http://localhost:3002/api/health
```

### Production Testing

Test production readiness:

```bash
# 1. Production deployment task
agro task production-deployment

# 2. Run with production configuration
agro exec production-deployment --no-env-overrides

# 3. Production testing
agro muster 'npm run build' 'output/production-deployment'
agro muster 'npm run test:production' 'output/production-deployment'
agro muster 'docker build -t prod-test .' 'output/production-deployment'
```

### Staging Environment

Staging deployment workflow:

```bash
# 1. Staging task
agro task staging-deployment

# 2. Run staging tests
agro exec staging-deployment

# 3. Deploy to staging
agro muster 'npm run deploy:staging' 'output/staging-deployment'

# 4. Smoke tests
agro muster 'npm run test:smoke' 'output/staging-deployment'
```

## Debugging Workflows

### Agent Debugging

Debug agent behavior:

```bash
# 1. Enable verbose logging
agro -vv exec debug-issue

# 2. Check agent logs
tail -f .agdocs/swap/logs/t1.log

# 3. Manual agent testing
cd trees/t1
aider --help
aider --model gpt-4 --message "Fix the authentication bug"

# 4. Compare manual vs automated
agro exec debug-issue aider
diff trees/t1/src/auth.py trees/t2/src/auth.py
```

### Task Specification Debugging

Refine task specifications:

```bash
# 1. Initial task (too vague)
agro task fix-performance
agro exec fix-performance

# 2. Review results
cd trees/t1
git diff HEAD~1

# 3. Refine task specification
edit .agdocs/specs/fix-performance.md
# Add specific performance metrics, test cases, constraints

# 4. Re-run with refined task
agro exec fix-performance

# 5. Compare results
agro muster 'npm run benchmark' 'output/fix-performance'
```

## Best Practices

### Task Specification Best Practices

1. **Be specific**: Clear requirements prevent ambiguous implementations
2. **Include tests**: Specify how success should be measured
3. **Provide context**: Help agents understand the codebase
4. **Set boundaries**: Define what should NOT be changed
5. **Iterate**: Refine specifications based on results

### Agent Selection Best Practices

1. **Match agents to tasks**: Use each agent's strengths
2. **Start simple**: Begin with single agents before multi-agent workflows
3. **Compare approaches**: Use multiple agents for critical features
4. **Document learnings**: Track which agents work best for different tasks

### Worktree Management Best Practices

1. **Clean up regularly**: Delete unused worktrees to save space
2. **Meaningful names**: Use descriptive task names
3. **Track progress**: Use `agro state` to monitor active work
4. **Backup critical work**: Merge important changes before cleanup

### Team Collaboration Best Practices

1. **Shared task specifications**: Use git to track task evolution
2. **Document decisions**: Record why certain solutions were chosen
3. **Knowledge sharing**: Share successful workflows and patterns
4. **Review together**: Collaborate on agent output review

---

## Workflow Templates

### Quick Start Template

```bash
# Copy this template for new features
agro task TASK_NAME
# Edit task specification
agro exec TASK_NAME
# Review and merge
cd trees/t1 && git diff HEAD~1
git checkout main && git merge output/TASK_NAME.1
agro delete 1
```

### Multi-Agent Template

```bash
# Copy this template for complex features
agro task TASK_NAME
agro exec TASK_NAME 3
agro muster 'npm test' 'output/TASK_NAME'
agro state
# Review each solution
agro grab output/TASK_NAME.1
agro grab output/TASK_NAME.2
agro grab output/TASK_NAME.3
# Merge best solution
git checkout main && git merge output/TASK_NAME.X
agro fade 'output/TASK_NAME.*'
```

---

## Next Steps

- [Examples](examples.md) - Real-world workflow examples
- [Troubleshooting](troubleshooting.md) - Common workflow issues
- [Contributing](contributing.md) - Share your workflow patterns

---

> 💡 **Tip**: Start with basic workflows and gradually adopt more complex patterns as you gain experience with Agro.