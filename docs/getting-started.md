# Getting Started

## Quick Start

### Prerequisites
- Docker installed and running
- AWS CLI configured (`aws configure`)
- AWS account with ECR and Lambda permissions

### 1. Clone and Setup
```bash
git clone <your-repo>
cd aws_labmda_sslv_scrape_job
```

### 2. Configure AWS Settings
Update the Makefile with your AWS account details:
```bash
# Edit Makefile and update:
AWS_ACCOUNT_ID = your-actual-account-id
AWS_REGION = your-preferred-region
```

### 3. Build and Test
```bash
# Build container for Ogre city
make build CITY=ogre

# Test locally
make test CITY=ogre

# Check logs
make logs CITY=ogre
```

### 4. Deploy to AWS
```bash
# Full deployment pipeline
make deploy-ogre
```

## Supported Cities
- **Ogre** (default)
- **Jurmala** 
- **Adazi**

## Quick Commands
```bash
make help                    # Show all available commands
make build CITY=jurmala      # Build for specific city
make test CITY=adazi         # Test specific city
make deploy-ogre            # Full deployment for Ogre
make cleanup CITY=jurmala   # Clean up local resources
```

## Troubleshooting
See [Troubleshooting Guide](troubleshooting.md) for common issues.
