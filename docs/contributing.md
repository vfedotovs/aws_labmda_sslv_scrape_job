# Contributing Guide

Thank you for your interest in contributing to the AWS Lambda SSLV Scraper project! This guide will help you get started with contributing.

## Getting Started

### Prerequisites
- Docker Desktop
- AWS CLI configured
- Git
- Make (for using Makefile)

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/aws_labmda_sslv_scrape_job.git
cd aws_labmda_sslv_scrape_job

# Set up upstream remote
git remote add upstream https://github.com/original-owner/aws_labmda_sslv_scrape_job.git

# Install dependencies
pip install -r requirements.txt
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 2. Make Your Changes
- Follow the existing code style
- Add appropriate error handling
- Include logging for debugging
- Update documentation if needed

### 3. Test Your Changes
```bash
# Test locally
make build CITY=ogre
make test CITY=ogre

# Check logs
make logs CITY=ogre

# Clean up
make cleanup CITY=ogre
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add support for new city scraping"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions small and focused
- Use meaningful variable names

### Example Function
```python
def extract_data_from_url(urls: list) -> None:
    """
    Extract apartment data from SSLV message URLs.
    
    Args:
        urls: List of message URLs to process
        
    Returns:
        None: Data is written to local file
    """
    # Implementation here
```

### Error Handling
```python
try:
    # Main logic
    result = process_data(url)
except requests.RequestException as e:
    logger.error(f"Network error processing {url}: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Adding New Cities

### 1. Update app.py
Add new city URLs to the handler function:
```python
def handler(event, context):
    # Add new city pages
    page_one = requests.get("https://www.ss.lv/lv/real-estate/flats/new-city/sell/")
    page_two = requests.get("https://www.ss.lv/lv/real-estate/flats/new-city/sell/page2.html")
    page_three = requests.get("https://www.ss.lv/lv/real-estate/flats/new-city/sell/page3.html")
```

### 2. Update Documentation
- Add city to supported cities list
- Update examples in documentation
- Add city-specific configuration if needed

### 3. Test Thoroughly
```bash
# Test new city
make build CITY=newcity
make test CITY=newcity
```

## Testing Requirements

### Local Testing
- [ ] Container builds successfully
- [ ] Local test runs without errors
- [ ] Data extraction works correctly
- [ ] S3 upload simulation works

### Code Quality
- [ ] No hardcoded credentials
- [ ] Proper error handling
- [ ] Appropriate logging
- [ ] Code follows style guidelines

## Pull Request Guidelines

### Before Submitting
1. Ensure all tests pass
2. Update documentation if needed
3. Add appropriate commit messages
4. Self-review your changes

### Pull Request Template
Use the provided PR template and fill out all relevant sections:
- Description of changes
- Type of change
- Testing completed
- City support affected

### Review Process
1. Automated checks must pass
2. Code review by maintainers
3. Address any feedback
4. Merge after approval

## Commit Message Format

Use conventional commit format:
```
type(scope): description

feat: add support for new city scraping
fix: resolve S3 upload timeout issue
docs: update deployment instructions
refactor: improve error handling
test: add unit tests for data extraction
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Issue Reporting

### Bug Reports
Use the issue template and include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages and logs

### Feature Requests
- Clear description of the feature
- Use case and benefits
- Implementation suggestions (if any)
- Any breaking changes

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks
- Any unprofessional conduct

## Getting Help

### Documentation
- Check existing documentation in `docs/` folder
- Review README.md for quick start
- Look at troubleshooting guide

### Community
- Open an issue for questions
- Use discussions for general questions
- Tag maintainers for urgent issues

### Development Questions
- How to add a new city?
- How to modify scraping logic?
- How to improve performance?
- How to add monitoring?

## Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Release notes prepared

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to this project! 🎉
