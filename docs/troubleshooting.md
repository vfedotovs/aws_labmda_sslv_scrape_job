# Troubleshooting Guide

## Common Issues and Solutions

### Docker Build Issues

#### Platform Architecture Warning
**Problem**: `InvalidBaseImagePlatform: Base image was pulled with platform "linux/amd64", expected "linux/arm64"`

**Solution**:
```bash
# Use the updated Makefile with explicit platform
make build CITY=ogre

# Or build for local architecture for testing
make build-local CITY=ogre
```

#### Build Context Issues
**Problem**: Docker build fails with "context" errors

**Solution**:
```bash
# Ensure you're in the project root directory
cd /path/to/aws_labmda_sslv_scrape_job
make build CITY=ogre
```

### AWS Authentication Issues

#### ECR Login Failures
**Problem**: `Error: AWS CLI not configured`

**Solution**:
```bash
# Configure AWS CLI
aws configure

# Verify configuration
aws sts get-caller-identity

# Test ECR login
make login CITY=ogre
```

#### Permission Denied Errors
**Problem**: `AccessDenied` when pushing to ECR

**Solution**:
1. Verify IAM permissions for ECR
2. Check repository exists:
   ```bash
   aws ecr describe-repositories --repository-names sslv-scraper-ogre
   ```
3. Ensure correct AWS region

### Lambda Deployment Issues

#### Function Not Found
**Problem**: `Function not found` during deployment

**Solution**:
1. Create Lambda function first:
   ```bash
   aws lambda create-function --function-name sslv-scraper-ogre --package-type Image --code ImageUri=your-ecr-uri --role your-role-arn
   ```
2. Or update existing function:
   ```bash
   make deploy CITY=ogre
   ```

#### Image URI Issues
**Problem**: Invalid image URI in Lambda

**Solution**:
1. Verify ECR repository exists
2. Check image was pushed successfully:
   ```bash
   aws ecr describe-images --repository-name sslv-scraper-ogre
   ```
3. Use correct ECR URI format

### Local Testing Issues

#### Container Won't Start
**Problem**: Container fails to start locally

**Solution**:
```bash
# Check container logs
docker logs sslv-scraper-ogre-test

# Verify environment variables
docker run --rm -e AWS_ACCESS_KEY_ID=test -e AWS_SECRET_ACCESS_KEY=test sslv-scraper-ogre:latest env
```

#### Port Already in Use
**Problem**: `Port 9000 is already in use`

**Solution**:
```bash
# Stop existing containers
make test-stop CITY=ogre

# Or use different port
docker run -p 9001:8080 -e AWS_ACCESS_KEY_ID=... sslv-scraper-ogre:latest
```

#### Test Timeout
**Problem**: Test takes too long or hangs

**Solution**:
1. Check container is running: `docker ps`
2. Monitor logs: `make logs CITY=ogre`
3. Test manually: `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

### S3 Upload Issues

#### Bucket Not Found
**Problem**: S3 bucket doesn't exist

**Solution**:
```bash
# Create bucket
aws s3 mb s3://lambda-ogre-scraped-data

# Verify bucket exists
aws s3 ls s3://lambda-ogre-scraped-data
```

#### Permission Denied on S3
**Problem**: Cannot upload to S3

**Solution**:
1. Check Lambda execution role has S3 permissions
2. Verify bucket policy allows Lambda access
3. Test S3 access:
   ```bash
   aws s3 cp test.txt s3://lambda-ogre-scraped-data/
   ```

### Web Scraping Issues

#### Network Timeouts
**Problem**: Requests to ss.lv timeout

**Solution**:
1. Check internet connectivity
2. Verify ss.lv is accessible
3. Consider increasing Lambda timeout

#### Parsing Errors
**Problem**: BeautifulSoup parsing fails

**Solution**:
1. Check if website structure changed
2. Verify HTML content is valid
3. Add error handling for malformed HTML

## Debugging Commands

### Container Debugging
```bash
# Check container status
make status

# View detailed logs
make logs CITY=ogre

# Interactive shell in container
docker run -it --entrypoint /bin/bash sslv-scraper-ogre:latest
```

### AWS Debugging
```bash
# Check Lambda function status
aws lambda get-function --function-name sslv-scraper-ogre

# View CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/sslv-scraper

# Check ECR images
aws ecr describe-images --repository-name sslv-scraper-ogre
```

### Network Debugging
```bash
# Test connectivity to ss.lv
curl -I https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/

# Test local Lambda endpoint
curl -v -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## Performance Optimization

### Slow Execution
**Solutions**:
1. Increase Lambda memory allocation
2. Optimize web scraping logic
3. Use connection pooling
4. Implement parallel processing

### High Memory Usage
**Solutions**:
1. Process data in smaller chunks
2. Clear variables after use
3. Optimize BeautifulSoup parsing
4. Monitor memory usage in CloudWatch

## Getting Help

### Log Analysis
1. Check CloudWatch logs for detailed error messages
2. Look for stack traces in Lambda logs
3. Monitor S3 access logs

### Community Support
- Check AWS Lambda documentation
- Review Docker troubleshooting guides
- Search for similar issues in AWS forums

### Escalation
If issues persist:
1. Collect all relevant logs
2. Document exact error messages
3. Note environment details (OS, Docker version, AWS region)
4. Create detailed issue report
