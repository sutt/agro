# Examples

> ⚠️ **Warning**: Everything in this section is ai-generated and not accurate. We'll refine later.

Real-world examples demonstrating Agro's capabilities across different development scenarios.

## Basic Examples

### Hello World Example

The simplest possible Agro workflow:

```bash
# Initialize project
mkdir hello-agro
cd hello-agro
git init
echo "# Hello Agro" > README.md
git add README.md
git commit -m "Initial commit"

# Initialize Agro
agro init

# Create task
agro task hello-world
```

**Task specification** (`.agdocs/specs/hello-world.md`):
```markdown
# Hello World Task

Add a "Hello, World!" message to the README.md file.

## Requirements
- Add a new section titled "Hello World"
- Include a friendly greeting message
- Preserve existing content
- Use proper markdown formatting

## Expected Output
The README should include:
```
# Hello Agro

## Hello World
Hello, World! Welcome to Agro - your AI-powered development assistant.
```

**Execute the task**:
```bash
# Run with default agent
agro exec hello-world

# Check results
cd trees/t1
cat README.md
git diff HEAD~1
```

### Multi-Agent Comparison

Compare how different agents handle the same task:

```bash
# Create task
agro task add-calculator

# Run three different agents
agro exec add-calculator aider
agro exec add-calculator claude  
agro exec add-calculator gemini

# Compare results
agro muster 'python calculator.py' 'output/add-calculator'
agro muster 'python -m pytest test_calculator.py' 'output/add-calculator'
```

**Task specification** (`.agdocs/specs/add-calculator.md`):
```markdown
# Calculator Implementation

Create a simple calculator module with basic arithmetic operations.

## Requirements
- File: `calculator.py`
- Functions: `add()`, `subtract()`, `multiply()`, `divide()`
- Handle division by zero
- Include docstrings for all functions
- Create `test_calculator.py` with comprehensive tests

## Example Usage
```python
from calculator import add, subtract, multiply, divide

result = add(5, 3)  # Returns 8
result = divide(10, 2)  # Returns 5.0
result = divide(10, 0)  # Raises ValueError
```

## Acceptance Criteria
- [ ] All functions implemented
- [ ] Error handling for edge cases
- [ ] Tests pass with 100% coverage
- [ ] Code follows PEP 8 style guide
```

## Web Development Examples

### FastAPI REST API

Create a REST API with authentication:

```bash
# Project setup
mkdir agro-api
cd agro-api
git init
echo "fastapi>=0.104.1\nuvicorn>=0.24.0\npyjwt>=2.8.0\npasslib>=1.7.4" > requirements.txt
git add requirements.txt
git commit -m "Add dependencies"

# Initialize Agro
agro init

# Create API task
agro task api-with-auth
```

**Task specification** (`.agdocs/specs/api-with-auth.md`):
```markdown
# FastAPI with Authentication

Create a REST API with JWT authentication.

## Requirements
- FastAPI application in `main.py`
- JWT token authentication
- User registration and login endpoints
- Protected routes requiring authentication
- Password hashing with bcrypt
- In-memory user storage (for demo)

## Endpoints
- POST `/register` - User registration
- POST `/login` - User authentication
- GET `/profile` - Get user profile (protected)
- GET `/health` - Health check (public)

## Testing
- Include test file `test_api.py`
- Test all endpoints
- Test authentication flow
- Test error cases

## Run Instructions
```bash
uvicorn main:app --reload --port 8000
```

## Acceptance Criteria
- [ ] All endpoints implemented
- [ ] JWT authentication working
- [ ] Passwords properly hashed
- [ ] Tests pass
- [ ] API documentation auto-generated
```

**Execute and test**:
```bash
# Run multiple agents
agro exec api-with-auth 2

# Test the APIs
agro muster --server 'uvicorn main:app --reload' 'output/api-with-auth'

# Test endpoints
curl -X POST http://localhost:8001/register -H "Content-Type: application/json" -d '{"username": "test", "password": "secret123"}'
curl -X POST http://localhost:8001/login -H "Content-Type: application/json" -d '{"username": "test", "password": "secret123"}'

# Compare implementations
agro muster 'python -m pytest test_api.py -v' 'output/api-with-auth'

# Clean up
agro muster --kill-server '' 'output/api-with-auth'
```

### React Component Library

Create a React component library:

```bash
# Project setup
mkdir agro-components
cd agro-components
npm init -y
npm install react react-dom @types/react @types/react-dom typescript
git init
git add .
git commit -m "Initial setup"

# Initialize Agro
agro init

# Create component task
agro task ui-components
```

**Task specification** (`.agdocs/specs/ui-components.md`):
```markdown
# React UI Components

Create a set of reusable React components with TypeScript.

## Requirements
- Button component with variants (primary, secondary, danger)
- Input component with validation
- Card component for content display
- TypeScript definitions for all components
- Storybook for component documentation
- Jest tests for all components

## Components Structure
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── Button.stories.tsx
│   ├── Input/
│   │   ├── Input.tsx
│   │   ├── Input.test.tsx
│   │   └── Input.stories.tsx
│   └── Card/
│       ├── Card.tsx
│       ├── Card.test.tsx
│       └── Card.stories.tsx
└── index.ts
```

## Testing
- Unit tests with Jest and React Testing Library
- Visual regression tests with Storybook
- TypeScript type checking

## Acceptance Criteria
- [ ] All components implemented
- [ ] TypeScript types defined
- [ ] Tests pass with >90% coverage
- [ ] Storybook stories created
- [ ] Components exported properly
```

**Execute and test**:
```bash
# Run agents
agro exec ui-components claude
agro exec ui-components aider

# Test components
agro muster 'npm test' 'output/ui-components'
agro muster 'npm run storybook' 'output/ui-components'

# Compare component implementations
agro muster 'ls -la src/components/' 'output/ui-components'
```

## Data Science Examples

### Machine Learning Pipeline

Create a complete ML pipeline:

```bash
# Project setup
mkdir agro-ml
cd agro-ml
echo "pandas>=2.0.0\nscikit-learn>=1.3.0\nmatplotlib>=3.7.0\njupyter>=1.0.0" > requirements.txt
git init
git add requirements.txt
git commit -m "Add ML dependencies"

# Initialize Agro
agro init

# Create ML task
agro task ml-pipeline
```

**Task specification** (`.agdocs/specs/ml-pipeline.md`):
```markdown
# Machine Learning Pipeline

Create a complete ML pipeline for predicting house prices.

## Requirements
- Data loading and preprocessing
- Feature engineering
- Model training and evaluation
- Hyperparameter tuning
- Model serialization
- Jupyter notebook for exploration
- Python scripts for production

## Files to Create
- `data_loader.py` - Data loading utilities
- `preprocessor.py` - Data preprocessing
- `model.py` - Model definition and training
- `train.py` - Training script
- `predict.py` - Prediction script
- `requirements.txt` - Dependencies
- `exploration.ipynb` - Jupyter notebook
- `test_pipeline.py` - Tests

## Dataset
Use the Boston Housing dataset from scikit-learn.

## Model Requirements
- Try at least 3 different algorithms
- Cross-validation for model selection
- Feature importance analysis
- Model performance metrics (MAE, MSE, R²)

## Acceptance Criteria
- [ ] Data pipeline implemented
- [ ] Models trained and evaluated
- [ ] Best model selected and saved
- [ ] Jupyter notebook with analysis
- [ ] Production scripts working
- [ ] Tests pass
```

**Execute and analyze**:
```bash
# Run ML task
agro exec ml-pipeline gemini
agro exec ml-pipeline claude

# Compare approaches
agro muster 'python train.py' 'output/ml-pipeline'
agro muster 'python -m pytest test_pipeline.py' 'output/ml-pipeline'

# Start Jupyter notebooks
agro muster --server 'jupyter lab --no-browser' 'output/ml-pipeline'
```

### Data Analysis Dashboard

Create an interactive data dashboard:

```bash
# Project setup
mkdir agro-dashboard
cd agro-dashboard
echo "streamlit>=1.28.0\nplotly>=5.17.0\npandas>=2.0.0" > requirements.txt
git init
git add requirements.txt
git commit -m "Add dashboard dependencies"

# Initialize Agro
agro init

# Create dashboard task
agro task data-dashboard
```

**Task specification** (`.agdocs/specs/data-dashboard.md`):
```markdown
# Interactive Data Dashboard

Create an interactive dashboard for sales data analysis.

## Requirements
- Streamlit web application
- Interactive charts with Plotly
- Data filtering and selection
- Multiple dashboard pages
- CSV data upload functionality
- Export functionality

## Dashboard Features
- Sales overview page
- Time series analysis
- Geographic analysis
- Product performance
- Customer segmentation

## Technical Requirements
- `dashboard.py` - Main Streamlit app
- `data_processor.py` - Data processing utilities
- `charts.py` - Chart generation functions
- `config.py` - Configuration settings
- Sample data files
- Requirements.txt with dependencies

## Acceptance Criteria
- [ ] Dashboard loads and runs
- [ ] All charts display correctly
- [ ] Filters work properly
- [ ] Data upload functionality
- [ ] Export features working
- [ ] Mobile responsive design
```

**Execute and test**:
```bash
# Run dashboard task
agro exec data-dashboard streamlit
agro exec data-dashboard claude

# Test dashboards
agro muster --server 'streamlit run dashboard.py' 'output/data-dashboard'

# Access dashboards
open http://localhost:8501  # First implementation
open http://localhost:8502  # Second implementation
```

## DevOps Examples

### Docker Container Setup

Containerize an application:

```bash
# Project with existing app
cd existing-app
agro init

# Create containerization task
agro task dockerize-app
```

**Task specification** (`.agdocs/specs/dockerize-app.md`):
```markdown
# Dockerize Application

Create Docker configuration for the application.

## Requirements
- Multi-stage Dockerfile for optimization
- Docker Compose for development
- Environment variable configuration
- Health checks
- Security best practices

## Files to Create
- `Dockerfile` - Main container definition
- `docker-compose.yml` - Development setup
- `docker-compose.prod.yml` - Production setup
- `.dockerignore` - Exclude unnecessary files
- `entrypoint.sh` - Container startup script

## Docker Image Requirements
- Use official Python/Node base image
- Non-root user for security
- Minimal image size
- Proper layer caching
- Health check endpoint

## Acceptance Criteria
- [ ] Docker image builds successfully
- [ ] Container runs without errors
- [ ] Health checks pass
- [ ] Development setup works
- [ ] Production setup configured
- [ ] Image size optimized
```

**Execute and test**:
```bash
# Run containerization
agro exec dockerize-app aider
agro exec dockerize-app claude

# Test Docker builds
agro muster 'docker build -t test-app .' 'output/dockerize-app'
agro muster 'docker run --rm test-app npm test' 'output/dockerize-app'

# Test Docker Compose
agro muster 'docker-compose up --build -d' 'output/dockerize-app'
agro muster 'docker-compose logs' 'output/dockerize-app'
```

### CI/CD Pipeline

Create GitHub Actions workflow:

```bash
# Project setup
cd your-project
agro init

# Create CI/CD task
agro task github-actions
```

**Task specification** (`.agdocs/specs/github-actions.md`):
```markdown
# GitHub Actions CI/CD

Create a comprehensive CI/CD pipeline with GitHub Actions.

## Requirements
- Automated testing on push/PR
- Multiple environment testing
- Security scanning
- Automated deployment
- Notification system

## Workflows to Create
- `.github/workflows/ci.yml` - Continuous Integration
- `.github/workflows/cd.yml` - Continuous Deployment
- `.github/workflows/security.yml` - Security scanning
- `.github/workflows/release.yml` - Release automation

## CI Features
- Test on multiple Python/Node versions
- Run linting and formatting checks
- Generate test coverage reports
- Build and test Docker images
- Cache dependencies for speed

## CD Features
- Deploy to staging on main branch
- Deploy to production on release
- Rollback capability
- Environment-specific configurations

## Acceptance Criteria
- [ ] CI workflow runs on all PRs
- [ ] Tests pass on multiple environments
- [ ] Security scanning integrated
- [ ] Deployment automation works
- [ ] Notifications configured
```

**Execute and test**:
```bash
# Run CI/CD setup
agro exec github-actions aider
agro exec github-actions claude

# Test workflow syntax
agro muster 'cat .github/workflows/ci.yml' 'output/github-actions'

# Compare implementations
agro muster 'find .github/ -name "*.yml" | head -5' 'output/github-actions'
```

## Advanced Examples

### Microservices Architecture

Create a microservices setup:

```bash
# Project setup
mkdir agro-microservices
cd agro-microservices
git init
agro init

# Create microservices task
agro task microservices-setup
```

**Task specification** (`.agdocs/specs/microservices-setup.md`):
```markdown
# Microservices Architecture

Create a microservices architecture with multiple services.

## Services to Create
- `user-service/` - User management
- `product-service/` - Product catalog
- `order-service/` - Order processing
- `gateway/` - API Gateway
- `shared/` - Shared utilities

## Requirements
- Each service in separate directory
- Docker configuration for each service
- Docker Compose for orchestration
- Service discovery
- Inter-service communication
- API documentation

## Service Structure
```
<service-name>/
├── src/
├── tests/
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
```

## Infrastructure
- Docker Compose with all services
- Service health checks
- Environment configuration
- Logging configuration
- Monitoring setup

## Acceptance Criteria
- [ ] All services implemented
- [ ] Services communicate properly
- [ ] Docker orchestration works
- [ ] API documentation generated
- [ ] Health checks pass
- [ ] Tests pass for all services
```

**Execute and test**:
```bash
# Run microservices setup
agro exec microservices-setup claude
agro exec microservices-setup aider

# Test service orchestration
agro muster 'docker-compose up --build -d' 'output/microservices-setup'
agro muster 'docker-compose ps' 'output/microservices-setup'

# Test service communication
agro muster 'curl http://localhost:8080/health' 'output/microservices-setup'
```

### Performance Optimization

Optimize application performance:

```bash
# Existing slow application
cd slow-app
agro init

# Create optimization task
agro task performance-optimization
```

**Task specification** (`.agdocs/specs/performance-optimization.md`):
```markdown
# Performance Optimization

Optimize the application for better performance.

## Analysis Required
- Profile application performance
- Identify bottlenecks
- Database query optimization
- Frontend bundle optimization
- Memory usage optimization

## Optimizations to Implement
- Database indexing
- Query optimization
- Caching implementation
- Code splitting
- Image optimization
- Lazy loading

## Benchmarking
- Before/after performance metrics
- Load testing with different scenarios
- Memory usage profiling
- Response time measurements

## Tools to Use
- Python: cProfile, memory_profiler
- Node.js: clinic.js, webpack-bundle-analyzer
- Database: EXPLAIN ANALYZE
- Frontend: Lighthouse, WebPageTest

## Acceptance Criteria
- [ ] Performance bottlenecks identified
- [ ] Optimizations implemented
- [ ] Performance improved by >30%
- [ ] Benchmarks documented
- [ ] No functionality broken
```

**Execute and benchmark**:
```bash
# Run optimization
agro exec performance-optimization claude
agro exec performance-optimization aider

# Run benchmarks
agro muster 'python benchmark.py' 'output/performance-optimization'
agro muster 'npm run benchmark' 'output/performance-optimization'

# Compare performance
agro muster 'cat performance-report.md' 'output/performance-optimization'
```

## Domain-Specific Examples

### E-commerce Platform

Create an e-commerce platform:

```bash
# Project setup
mkdir agro-ecommerce
cd agro-ecommerce
git init
agro init

# Create e-commerce task
agro task ecommerce-platform
```

**Task specification** (`.agdocs/specs/ecommerce-platform.md`):
```markdown
# E-commerce Platform

Create a complete e-commerce platform with modern features.

## Core Features
- Product catalog with search/filtering
- Shopping cart functionality
- User authentication and profiles
- Order management
- Payment integration (mock)
- Admin dashboard

## Technical Stack
- Backend: FastAPI or Django
- Frontend: React or Vue.js
- Database: PostgreSQL or SQLite
- Authentication: JWT tokens
- File storage: Local or S3-compatible

## Database Models
- Users, Products, Categories
- Orders, OrderItems
- Reviews, Ratings
- Inventory management

## API Endpoints
- Authentication: /auth/login, /auth/register
- Products: /products, /products/{id}
- Cart: /cart, /cart/items
- Orders: /orders, /orders/{id}
- Admin: /admin/products, /admin/orders

## Frontend Pages
- Home page with featured products
- Product listing with filters
- Product detail page
- Shopping cart
- Checkout process
- User dashboard
- Admin interface

## Acceptance Criteria
- [ ] All core features implemented
- [ ] User authentication working
- [ ] Product management complete
- [ ] Shopping cart functional
- [ ] Order process working
- [ ] Admin dashboard operational
- [ ] Tests pass
- [ ] API documentation generated
```

**Execute and test**:
```bash
# Run e-commerce development
agro exec ecommerce-platform claude
agro exec ecommerce-platform aider

# Start development servers
agro muster --server 'npm run dev' 'output/ecommerce-platform'
agro muster --server 'python manage.py runserver' 'output/ecommerce-platform'

# Test API endpoints
agro muster 'curl http://localhost:8000/products' 'output/ecommerce-platform'
agro muster 'python -m pytest tests/test_api.py' 'output/ecommerce-platform'
```

### IoT Data Processing

Create an IoT data processing system:

```bash
# Project setup
mkdir agro-iot
cd agro-iot
git init
agro init

# Create IoT task
agro task iot-data-processing
```

**Task specification** (`.agdocs/specs/iot-data-processing.md`):
```markdown
# IoT Data Processing System

Create a system for processing IoT sensor data.

## Requirements
- Data ingestion from multiple sensors
- Real-time data processing
- Data storage and retrieval
- Alerting system
- Dashboard for visualization
- Historical data analysis

## Components
- Data collector service
- Message queue (Redis/RabbitMQ)
- Data processor
- Database (InfluxDB/TimescaleDB)
- Alert manager
- Web dashboard

## Sensor Types
- Temperature sensors
- Humidity sensors
- Motion detectors
- Air quality sensors
- Water level sensors

## Processing Features
- Data validation
- Anomaly detection
- Trend analysis
- Aggregation (hourly, daily)
- Alerting thresholds

## Dashboard Features
- Real-time sensor readings
- Historical charts
- Alert notifications
- Sensor status monitoring
- Data export functionality

## Acceptance Criteria
- [ ] Data ingestion working
- [ ] Real-time processing active
- [ ] Alerts triggering correctly
- [ ] Dashboard displaying data
- [ ] Historical analysis available
- [ ] System scalable
```

**Execute and test**:
```bash
# Run IoT system development
agro exec iot-data-processing gemini
agro exec iot-data-processing claude

# Test data pipeline
agro muster 'python simulate_sensors.py' 'output/iot-data-processing'
agro muster 'python -m pytest tests/test_pipeline.py' 'output/iot-data-processing'

# Start dashboard
agro muster --server 'streamlit run dashboard.py' 'output/iot-data-processing'
```

## Real-World Scenario Examples

### Legacy Code Modernization

Modernize a legacy codebase:

```bash
# Legacy project
cd legacy-project
agro init

# Create modernization task
agro task modernize-legacy
```

**Task specification** (`.agdocs/specs/modernize-legacy.md`):
```markdown
# Legacy Code Modernization

Modernize the legacy codebase while maintaining functionality.

## Current State Analysis
- Python 2.7 codebase
- No tests
- Deprecated dependencies
- No documentation
- Monolithic structure

## Modernization Goals
- Upgrade to Python 3.9+
- Add comprehensive tests
- Update dependencies
- Modularize architecture
- Add type hints
- Improve error handling

## Migration Strategy
- Incremental migration approach
- Maintain backward compatibility
- Add tests before refactoring
- Update dependencies gradually
- Document changes

## Acceptance Criteria
- [ ] Python 3.9+ compatibility
- [ ] Test coverage >80%
- [ ] Dependencies updated
- [ ] Type hints added
- [ ] Documentation complete
- [ ] No functionality lost
- [ ] Performance maintained
```

### Bug Fix Campaign

Systematic bug fixing:

```bash
# Project with known bugs
cd buggy-project
agro init

# Create bug fix task
agro task bug-fix-campaign
```

**Task specification** (`.agdocs/specs/bug-fix-campaign.md`):
```markdown
# Bug Fix Campaign

Systematically fix all known bugs in the application.

## Known Issues
1. Memory leak in data processing
2. Race condition in user authentication
3. SQL injection vulnerability
4. Frontend state management bugs
5. API rate limiting issues

## Bug Fix Process
- Reproduce each bug
- Write failing test
- Implement fix
- Verify fix works
- Update documentation

## Testing Strategy
- Unit tests for each fix
- Integration tests for complex bugs
- Performance tests for optimization
- Security tests for vulnerabilities

## Documentation
- Update changelog
- Document root causes
- Add prevention measures
- Update troubleshooting guide

## Acceptance Criteria
- [ ] All bugs reproduced
- [ ] Tests added for each bug
- [ ] Fixes implemented
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] Performance maintained
```

**Execute and test**:
```bash
# Run systematic bug fixing
agro exec bug-fix-campaign aider
agro exec bug-fix-campaign claude

# Test bug fixes
agro muster 'python -m pytest tests/test_bug_fixes.py -v' 'output/bug-fix-campaign'
agro muster 'python security_scan.py' 'output/bug-fix-campaign'

# Compare approaches
agro muster 'git log --oneline -10' 'output/bug-fix-campaign'
```

## Conclusion

These examples demonstrate Agro's versatility across different domains and complexity levels. Each example includes:

- **Clear task specifications** with specific requirements
- **Acceptance criteria** to measure success
- **Testing strategies** to verify implementations
- **Multiple agent comparisons** to explore different approaches

### Key Takeaways

1. **Specific requirements** lead to better agent performance
2. **Multiple agents** provide different perspectives and solutions
3. **Systematic testing** ensures quality across implementations
4. **Clear documentation** makes results comparable and maintainable

### Best Practices from Examples

- Start with clear, specific task specifications
- Include testing requirements in every task
- Use multiple agents for complex or critical features
- Test all implementations systematically
- Document decisions and learnings

---

## Next Steps

- Try these examples in your own projects
- Adapt task specifications to your specific needs
- Share your own examples with the community
- Contribute new examples to the documentation

---

> 💡 **Tip**: Start with simpler examples and gradually work up to more complex scenarios as you become comfortable with Agro's workflow.