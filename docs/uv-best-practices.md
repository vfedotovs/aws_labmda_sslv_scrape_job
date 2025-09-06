# UV Best Practices Guide

## What is UV?

UV is a fast Python package manager and project manager written in Rust. It's designed to be a drop-in replacement for pip, pip-tools, and virtualenv, with significant performance improvements.

## UV Files and Git Management

### Files to COMMIT ✅

#### `pyproject.toml`
- **Purpose**: Project configuration, dependencies, and metadata
- **Why commit**: Essential for project setup and dependency management
- **Contains**: Project name, version, dependencies, build configuration

```toml
[project]
name = "aws-labmda-sslv-scrape-job"
version = "0.1.0"
description = "AWS Lambda scraper for SSLV apartment listings"
requires-python = ">=3.11"
dependencies = [
    "boto3>=1.40.25",
    "bs4>=0.0.2",
    "requests>=2.32.5",
]
```

#### `uv.lock`
- **Purpose**: Lock file ensuring reproducible builds
- **Why commit**: For applications, ensures everyone uses exact same dependency versions
- **Contains**: Exact versions of all dependencies and their transitive dependencies

#### `.python-version`
- **Purpose**: Specifies Python version for the project
- **Why commit**: Ensures consistent Python version across environments
- **Format**: Simple version number (e.g., `3.11`)

### Files to IGNORE ❌

#### `.venv/` or `venv/`
- **Purpose**: Virtual environment directory
- **Why ignore**: Environment-specific, can be recreated
- **Alternative**: Use `uv venv` to create when needed

#### `.uv_cache/`
- **Purpose**: UV package cache
- **Why ignore**: Local cache, can be recreated
- **Location**: Usually in `~/.cache/uv/`

#### `__pycache__/`
- **Purpose**: Python bytecode cache
- **Why ignore**: Generated files, can be recreated
- **Pattern**: `*.pyc`, `*.pyo`, `*$py.class`

## UV Commands and Workflows

### Project Initialization
```bash
# Create new project
uv init my-project
cd my-project

# Initialize existing project
uv init --no-readme
```

### Dependency Management
```bash
# Install all dependencies
uv sync

# Add new dependency
uv add requests

# Add development dependency
uv add --dev pytest

# Add with version constraint
uv add "requests>=2.25.0"

# Remove dependency
uv remove requests

# Update dependencies
uv lock --upgrade
```

### Virtual Environment
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Run command in virtual environment
uv run python app.py

# Run with specific Python version
uv run --python 3.11 python app.py
```

### Development Workflow
```bash
# 1. Clone project
git clone <repo>
cd project

# 2. Install dependencies
uv sync

# 3. Activate environment
source .venv/bin/activate

# 4. Make changes and test
uv run python app.py

# 5. Add new dependencies if needed
uv add new-package

# 6. Commit changes
git add pyproject.toml uv.lock
git commit -m "feat: add new dependency"
```

## Migration from pip/requirements.txt

### Current State
Your project has both `requirements.txt` and `pyproject.toml`:

```bash
# requirements.txt (legacy)
requests==2.25.1
bs4

# pyproject.toml (modern)
[project]
dependencies = [
    "boto3>=1.40.25",
    "bs4>=0.0.2",
    "requests>=2.32.5",
]
```

### Migration Steps
```bash
# 1. Convert requirements.txt to pyproject.toml
uv add --requirements requirements.txt

# 2. Remove requirements.txt (after verification)
rm requirements.txt

# 3. Update Dockerfile to use pyproject.toml
# Change from: COPY requirements.txt ./
# To: COPY pyproject.toml uv.lock ./
```

### Updated Dockerfile
```dockerfile
FROM --platform=linux/amd64 amazon/aws-lambda-python:3.9

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY app.py ./

# Set command
CMD ["app.handler"]
```

## Performance Benefits

### Speed Comparison
- **UV**: ~10-100x faster than pip
- **Dependency resolution**: Much faster
- **Virtual environment creation**: Near-instant
- **Package installation**: Significantly faster

### Memory Usage
- **Lower memory footprint** than pip
- **Efficient caching** system
- **Parallel downloads** when possible

## Best Practices

### 1. Lock File Management
```bash
# For applications: Always commit uv.lock
git add uv.lock
git commit -m "chore: update dependency lock file"

# For libraries: Consider ignoring uv.lock
echo "uv.lock" >> .gitignore
```

### 2. Python Version Management
```bash
# Set Python version in .python-version
echo "3.11" > .python-version

# Use specific Python version
uv run --python 3.11 python app.py
```

### 3. Dependency Groups
```toml
[project]
dependencies = [
    "requests>=2.25.0",
    "boto3>=1.40.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
]
```

### 4. CI/CD Integration
```yaml
# GitHub Actions example
- name: Install UV
  uses: astral-sh/setup-uv@v1

- name: Install dependencies
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest
```

### 5. Docker Integration
```dockerfile
# Multi-stage build with UV
FROM --platform=linux/amd64 amazon/aws-lambda-python:3.9

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY app.py ./

CMD ["app.handler"]
```

## Troubleshooting

### Common Issues

#### 1. Lock File Conflicts
```bash
# Regenerate lock file
rm uv.lock
uv lock

# Update specific dependency
uv lock --upgrade-package requests
```

#### 2. Python Version Mismatch
```bash
# Check Python version
uv python list

# Install specific Python version
uv python install 3.11

# Use specific version
uv run --python 3.11 python app.py
```

#### 3. Cache Issues
```bash
# Clear UV cache
uv cache clean

# Clear specific package cache
uv cache clean requests
```

#### 4. Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf .venv
uv venv
uv sync
```

## Migration Checklist

- [ ] Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Convert requirements.txt to pyproject.toml
- [ ] Update Dockerfile to use UV
- [ ] Update CI/CD pipelines
- [ ] Update documentation
- [ ] Test in all environments
- [ ] Remove requirements.txt
- [ ] Update team on new workflow

## Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
