# Development Guide

## Development Environment Setup

### Prerequisites
- Python 3.9+
- Docker Desktop
- AWS CLI v2
- Git
- Make (for using Makefile)
- UV (Python package manager)

### Local Development Setup
```bash
# Clone repository
git clone <your-repo-url>
cd aws_labmda_sslv_scrape_job

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with UV
uv sync

# Configure AWS CLI
aws configure
```

### UV Package Management

#### Installing Dependencies
```bash
# Install all dependencies from pyproject.toml
uv sync

# Add new dependency
uv add requests

# Add development dependency
uv add --dev pytest

# Remove dependency
uv remove package-name
```

#### Virtual Environment
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Run commands in virtual environment
uv run python app.py
```

## Git and Version Control

### Files to Commit vs Ignore

#### ✅ **Files to COMMIT:**
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for reproducible builds (for applications)
- `.python-version` - Python version specification
- `app.py` - Main application code
- `Dockerfile` - Container configuration
- `Makefile` - Build automation
- `README.md` - Project documentation
- `docs/` - Documentation files
- `.github/` - GitHub templates and workflows

#### ❌ **Files to IGNORE (in .gitignore):**
- `__pycache__/` - Python bytecode cache
- `.venv/` - Virtual environment directory
- `.uv_cache/` - UV package cache
- `*.pyc` - Compiled Python files
- `.env` - Environment variables
- `*.log` - Log files
- `*-raw-data-report*.txt` - Generated scraped data files
- `.DS_Store` - macOS system files
- `.vscode/` - VS Code settings (except extensions.json)
- `.idea/` - PyCharm/IntelliJ settings

### UV-Specific Best Practices

#### Lock File Management
```bash
# For applications (like this project): COMMIT uv.lock
# This ensures reproducible builds across environments
git add uv.lock

# For libraries: IGNORE uv.lock
# Libraries should be flexible with dependency versions
```

#### Python Version Management
```bash
# Commit .python-version to ensure consistent Python versions
echo "3.11" > .python-version
git add .python-version
```

#### Dependency Management
```bash
# Always update pyproject.toml for new dependencies
uv add requests

# Commit both pyproject.toml and uv.lock
git add pyproject.toml uv.lock
git commit -m "feat: add requests dependency"
```

## Development Workflow

### 1. Code Changes
```bash
# Make changes to app.py or other files
# Test locally using Makefile
make build-local CITY=ogre
make test CITY=ogre
```

### 2. Testing
```bash
# Run local tests
make test CITY=ogre

# Check logs
make logs CITY=ogre

# Stop test container
make test-stop CITY=ogre
```

### 3. Deployment
```bash
# Deploy to development environment
make deploy CITY=ogre

# Deploy to production (after testing)
make deploy CITY=ogre
```

## Code Structure

### Project Layout
```
aws_labmda_sslv_scrape_job/
├── app.py                 # Main Lambda function
├── main.py               # Alternative entry point (if needed)
├── Dockerfile            # Container configuration
├── Makefile              # Build and deployment automation
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Dependency lock file
├── requirements.txt      # Legacy requirements (can be removed)
├── .python-version      # Python version specification
├── .gitignore           # Git ignore rules
├── README.md            # Project overview
├── docs/                # Documentation
│   ├── getting-started.md
│   ├── deployment.md
│   ├── api.md
│   ├── troubleshooting.md
│   └── development.md
└── .github/             # GitHub templates
    ├── ISSUE_TEMPLATE.md
    └── PULL_REQUEST_TEMPLATE.md
```

### Key Functions in app.py

#### `handler(event, context)`
Main Lambda entry point. Orchestrates the entire scraping process.

#### `find_single_page_urls(bs_object)`
Extracts message URLs from parsed HTML pages.

#### `extract_data_from_url(nondup_urls)`
Main data extraction logic. Processes each message URL.

#### `get_msg_table_info(msg_url, td_class)`
Extracts specific data fields from individual message pages.

#### `upload_text_file_to_s3(file_path, bucket_name, s3_key)`
Handles S3 upload of scraped data.

## Adding New Cities

### 1. Update app.py
Modify the `handler` function to include new city URLs:
```python
def handler(event, context):
    # Add new city pages
    page_one = requests.get("https://www.ss.lv/lv/real-estate/flats/new-city/sell/")
    # ... rest of the logic
```

### 2. Update Makefile
The Makefile already supports new cities. Just use:
```bash
make build CITY=newcity
make test CITY=newcity
make deploy CITY=newcity
```

### 3. Create AWS Resources
```bash
# Create ECR repository
aws ecr create-repository --repository-name sslv-scraper-newcity

# Create S3 bucket
aws s3 mb s3://lambda-newcity-scraped-data

# Create Lambda function
aws lambda create-function --function-name sslv-scraper-newcity --package-type Image --code ImageUri=your-ecr-uri --role your-role-arn
```

## Code Quality

### Python Best Practices
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions
- Handle exceptions gracefully

### Error Handling
```python
try:
    # Scraping logic
    result = scrape_data(url)
except requests.RequestException as e:
    logger.error(f"Network error: {e}")
    return error_response
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return error_response
```

### Logging
```python
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use structured logging
logger.info(f"Processing URL {i+1} of {total_urls}")
```

## Testing Strategy

### Unit Testing
```python
import unittest
from unittest.mock import patch, MagicMock

class TestScraper(unittest.TestCase):
    def test_find_single_page_urls(self):
        # Test URL extraction logic
        pass
    
    def test_extract_data_from_url(self):
        # Test data extraction
        pass
```

### Integration Testing
```bash
# Test full pipeline locally
make build CITY=ogre
make test CITY=ogre
```

### Load Testing
```bash
# Test with multiple concurrent invocations
for i in {1..5}; do
  curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' &
done
```

## Performance Optimization

### Memory Optimization
- Process data in chunks
- Clear large variables after use
- Use generators for large datasets

### Network Optimization
- Implement connection pooling
- Add retry logic with exponential backoff
- Use async requests where possible

### Lambda Optimization
- Optimize cold start time
- Use provisioned concurrency for production
- Monitor and adjust memory allocation

## Security Considerations

### Secrets Management
- Use AWS Secrets Manager for sensitive data
- Never hardcode credentials
- Use IAM roles with least privilege

### Input Validation
- Validate all input parameters
- Sanitize URLs before processing
- Implement rate limiting

### Container Security
- Use specific base image tags
- Regular security updates
- Scan images for vulnerabilities

## Monitoring and Observability

### CloudWatch Metrics
Monitor these key metrics:
- Function duration
- Memory usage
- Error rate
- Invocation count

### Custom Metrics
```python
import boto3
cloudwatch = boto3.client('cloudwatch')

# Send custom metrics
cloudwatch.put_metric_data(
    Namespace='SSLVScraper',
    MetricData=[
        {
            'MetricName': 'ScrapedAds',
            'Value': len(scraped_data),
            'Unit': 'Count'
        }
    ]
)
```

### Logging Best Practices
- Use structured logging (JSON format)
- Include correlation IDs
- Log at appropriate levels
- Don't log sensitive data

## Deployment Strategies

### Blue-Green Deployment
1. Deploy new version to separate Lambda function
2. Test new version thoroughly
3. Switch traffic to new version
4. Keep old version for rollback

### Canary Deployment
1. Deploy to small percentage of traffic
2. Monitor metrics and errors
3. Gradually increase traffic
4. Full deployment if successful

## Contributing

### Code Review Process
1. Create feature branch
2. Make changes with tests
3. Submit pull request
4. Address review feedback
5. Merge after approval

### Commit Message Format
```
feat: add support for new city scraping
fix: resolve S3 upload timeout issue
docs: update deployment instructions
```

### Branch Naming
- `feature/city-support`
- `bugfix/s3-upload-error`
- `docs/api-documentation`