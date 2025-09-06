# AWS Lambda SSLV Scraper

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)

A serverless web scraper that extracts apartment listings from [ss.lv](https://www.ss.lv) and stores the data in AWS S3. Supports multiple cities with automated deployment via Docker containers.

## 🏠 Supported Cities

- **Ogre** (default)
- **Jurmala** 
- **Adazi**

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- AWS CLI configured (`aws configure`)
- AWS account with ECR and Lambda permissions

### 1. Build and Test
```bash
# Build container for Ogre city
make build CITY=ogre

# Test locally (takes 3-4 minutes)
make test CITY=ogre

# View logs
make logs CITY=ogre
```

### 2. Deploy to AWS
```bash
# Full deployment pipeline
make deploy-ogre
```

## 📋 Technologies

- **Python 3.9** - Runtime environment
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **AWS Lambda** - Serverless compute
- **AWS S3** - Data storage
- **Docker** - Containerization
- **AWS ECR** - Container registry


## 🛠️ Available Commands

The project includes a comprehensive Makefile for easy development and deployment:

```bash
# Show all available commands
make help

# Build containers for different cities
make build CITY=ogre
make build CITY=jurmala
make build CITY=adazi

# Test containers locally
make test CITY=ogre
make logs CITY=ogre

# Deploy to AWS
make deploy CITY=ogre
make deploy-jurmala
make deploy-adazi

# Cleanup local resources
make cleanup CITY=ogre
make clean-all
```

## 📖 Documentation

- **[Getting Started](docs/getting-started.md)** - Quick setup guide
- **[Deployment Guide](docs/deployment.md)** - AWS infrastructure setup
- **[API Documentation](docs/api.md)** - Function interfaces and data formats
- **[Development Guide](docs/development.md)** - Development workflow and best practices
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AWS Lambda    │    │   SSLV Website   │    │   AWS S3        │
│   (Container)   │───▶│   (ss.lv)        │    │   (Data Store)  │
│                 │    │                  │    │                 │
│ • Web Scraper   │    │ • Apartment      │    │ • JSON Files    │
│ • Data Parser   │    │   Listings       │    │ • Timestamped   │
│ • S3 Uploader   │    │ • 3 Pages/City   │    │ • City-specific │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### Environment Variables
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key  
- `AWS_REGION` - AWS region (default: us-east-1)

### Makefile Variables
- `CITY` - Target city (ogre, jurmala, adazi)
- `AWS_ACCOUNT_ID` - Your AWS account ID
- `AWS_REGION` - AWS region
- `PLATFORM` - Docker platform (default: linux/amd64)

## 📊 Data Output

The scraper extracts apartment data including:
- Room count
- Area (m²)
- Floor
- Price
- Publication date
- Location details

Data is stored in S3 as timestamped text files:
```
Ogre-raw-data-report-2023-02-18T14-30-25.txt
```

## ⚡ Performance

- **Execution time**: 3-4 minutes per city
- **Memory usage**: 512 MB
- **Timeout**: 15 minutes
- **Rate limiting**: 2-second delay between requests
- **Data volume**: ~90 ads per city (3 pages × 30 ads)

## 🔒 Security

- IAM roles with least privilege
- Container image scanning
- Secure credential management
- VPC configuration support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `make test`
5. Submit a pull request

See [Development Guide](docs/development.md) for detailed instructions.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Check [Troubleshooting Guide](docs/troubleshooting.md) for common issues
- Review [API Documentation](docs/api.md) for technical details
- Open an issue for bugs or feature requests

