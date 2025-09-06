# Deployment Guide

## AWS Infrastructure Setup

### 1. ECR Repositories
Create ECR repositories for each city:
```bash
# Create repositories
aws ecr create-repository --repository-name sslv-scraper-ogre --region us-east-1
aws ecr create-repository --repository-name sslv-scraper-jurmala --region us-east-1
aws ecr create-repository --repository-name sslv-scraper-adazi --region us-east-1
```

### 2. Lambda Functions
Create Lambda functions for each city:
```bash
# Create Lambda function for Ogre
aws lambda create-function \
  --function-name sslv-scraper-ogre \
  --package-type Image \
  --code ImageUri=123456789012.dkr.ecr.us-east-1.amazonaws.com/sslv-scraper-ogre:latest \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --timeout 900 \
  --memory-size 512
```

### 3. S3 Buckets
Create S3 buckets for data storage:
```bash
# Create buckets for each city
aws s3 mb s3://lambda-ogre-scraped-data
aws s3 mb s3://lambda-jurmala-scraped-data
aws s3 mb s3://lambda-adazi-scraped-data
```

## Deployment Process

### Manual Deployment
```bash
# 1. Build container
make build CITY=ogre

# 2. Test locally
make test CITY=ogre

# 3. Push to ECR
make push CITY=ogre

# 4. Deploy to Lambda
make deploy CITY=ogre
```

### Automated Deployment
```bash
# Full pipeline for any city
make deploy-ogre
make deploy-jurmala
make deploy-adazi
```

## Environment Variables

### Required AWS Environment Variables
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

### Lambda Configuration
- **Timeout**: 900 seconds (15 minutes)
- **Memory**: 512 MB
- **Architecture**: x86_64

## Monitoring and Logs

### CloudWatch Logs
```bash
# View logs for specific function
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/sslv-scraper
```

### Lambda Metrics
Monitor these key metrics:
- Invocations
- Duration
- Errors
- Throttles

## Rollback Strategy

### Rollback to Previous Version
```bash
# List available versions
aws lambda list-versions-by-function --function-name sslv-scraper-ogre

# Update to previous version
aws lambda update-function-code \
  --function-name sslv-scraper-ogre \
  --image-uri 123456789012.dkr.ecr.us-east-1.amazonaws.com/sslv-scraper-ogre:previous-tag
```

## Security Best Practices

### IAM Roles
- Use least privilege principle
- Separate roles for different environments
- Regular access reviews

### Container Security
- Scan images for vulnerabilities
- Use specific image tags (not `latest`)
- Regular base image updates

### Network Security
- VPC configuration if needed
- Security groups with minimal access
- Private subnets for Lambda functions
