# AWS Lambda SSLV Scraper Makefile
# Supports multiple cities: ogre, jurmala, adazi

# Default values - can be overridden with make CITY=jurmala
CITY ?= ogre
AWS_ACCOUNT_ID ?= 123456789012
AWS_REGION ?= us-east-1
ECR_REPOSITORY ?= sslv-scraper
LAMBDA_FUNCTION_NAME ?= sslv-scraper-$(CITY)
CONTAINER_NAME ?= sslv-scraper-$(CITY)
IMAGE_TAG ?= latest
PLATFORM ?= linux/amd64

# City-specific configurations
ifeq ($(CITY),ogre)
	LAMBDA_FUNCTION_NAME = sslv-scraper-ogre
	CONTAINER_NAME = sslv-scraper-ogre
	ECR_REPOSITORY = sslv-scraper-ogre
endif

ifeq ($(CITY),jurmala)
	LAMBDA_FUNCTION_NAME = sslv-scraper-jurmala
	CONTAINER_NAME = sslv-scraper-jurmala
	ECR_REPOSITORY = sslv-scraper-jurmala
endif

ifeq ($(CITY),adazi)
	LAMBDA_FUNCTION_NAME = sslv-scraper-adazi
	CONTAINER_NAME = sslv-scraper-adazi
	ECR_REPOSITORY = sslv-scraper-adazi
endif

# ECR repository URI
ECR_URI = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY)

.PHONY: help build test push deploy cleanup clean-all login check-aws

# Default target
help: ## Show this help message
	@echo "AWS Lambda SSLV Scraper - Available commands:"
	@echo ""
	@echo "Usage: make [COMMAND] [CITY=ogre|jurmala|adazi]"
	@echo ""
	@echo "Examples:"
	@echo "  make build CITY=ogre     # Build container for Ogre city"
	@echo "  make test CITY=jurmala   # Test container for Jurmala city"
	@echo "  make deploy CITY=adazi   # Deploy container for Adazi city"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Current configuration:"
	@echo "  CITY: $(CITY)"
	@echo "  AWS_ACCOUNT_ID: $(AWS_ACCOUNT_ID)"
	@echo "  AWS_REGION: $(AWS_REGION)"
	@echo "  ECR_REPOSITORY: $(ECR_REPOSITORY)"
	@echo "  LAMBDA_FUNCTION_NAME: $(LAMBDA_FUNCTION_NAME)"
	@echo "  PLATFORM: $(PLATFORM)"

check-aws: ## Check if AWS CLI is configured
	@echo "Checking AWS CLI configuration..."
	@aws sts get-caller-identity > /dev/null 2>&1 || (echo "Error: AWS CLI not configured. Please run 'aws configure' first." && exit 1)
	@echo "AWS CLI is configured ✓"

login: check-aws ## Login to AWS ECR
	@echo "Logging into AWS ECR..."
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URI)
	@echo "ECR login successful ✓"

build: ## Build Docker container for the specified city
	@echo "Building Docker container for $(CITY) city..."
	@echo "Container name: $(CONTAINER_NAME)"
	@echo "Platform: $(PLATFORM)"
	docker build --platform $(PLATFORM) -t $(CONTAINER_NAME):$(IMAGE_TAG) .
	@echo "Container built successfully ✓"
	@echo "Image: $(CONTAINER_NAME):$(IMAGE_TAG)"

build-local: ## Build Docker container for local architecture (faster, but may not work in AWS)
	@echo "Building Docker container for $(CITY) city (local architecture)..."
	@echo "Container name: $(CONTAINER_NAME)"
	@echo "Note: This build is optimized for local testing only"
	docker build -t $(CONTAINER_NAME):$(IMAGE_TAG) .
	@echo "Container built successfully ✓"
	@echo "Image: $(CONTAINER_NAME):$(IMAGE_TAG)"

build-multi: ## Build multi-platform Docker container (slower but more compatible)
	@echo "Building multi-platform Docker container for $(CITY) city..."
	@echo "Container name: $(CONTAINER_NAME)"
	@echo "This will build for both linux/amd64 and linux/arm64"
	docker buildx build --platform linux/amd64,linux/arm64 -t $(CONTAINER_NAME):$(IMAGE_TAG) .
	@echo "Multi-platform container built successfully ✓"
	@echo "Image: $(CONTAINER_NAME):$(IMAGE_TAG)"

test: ## Test the built container locally
	@echo "Testing container for $(CITY) city..."
	@echo "Starting container on port 9000..."
	@echo "Container will run for 3-4 minutes. Please wait..."
	docker run -d --name $(CONTAINER_NAME)-test \
		-p 9000:8080 \
		-e AWS_ACCESS_KEY_ID=$$AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY=$$AWS_SECRET_ACCESS_KEY \
		-e AWS_REGION=$(AWS_REGION) \
		$(CONTAINER_NAME):$(IMAGE_TAG)
	@echo "Container started. Waiting 10 seconds for initialization..."
	@sleep 10
	@echo "Testing Lambda function invocation..."
	@echo "This may take 3-4 minutes to complete..."
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' || echo "Test completed (check container logs for details)"
	@echo "Test completed. Check container logs with: docker logs $(CONTAINER_NAME)-test"

test-stop: ## Stop the test container
	@echo "Stopping test container..."
	docker stop $(CONTAINER_NAME)-test 2>/dev/null || echo "Container not running"
	docker rm $(CONTAINER_NAME)-test 2>/dev/null || echo "Container not found"
	@echo "Test container stopped ✓"

tag: ## Tag the container for ECR
	@echo "Tagging container for ECR..."
	docker tag $(CONTAINER_NAME):$(IMAGE_TAG) $(ECR_URI):$(IMAGE_TAG)
	@echo "Container tagged: $(ECR_URI):$(IMAGE_TAG)"

push: login tag ## Push container to ECR
	@echo "Pushing container to ECR..."
	docker push $(ECR_URI):$(IMAGE_TAG)
	@echo "Container pushed to ECR successfully ✓"
	@echo "ECR URI: $(ECR_URI):$(IMAGE_TAG)"

deploy: push ## Deploy new Lambda version with updated container
	@echo "Deploying Lambda function: $(LAMBDA_FUNCTION_NAME)"
	@echo "Updating function code with new container image..."
	aws lambda update-function-code \
		--function-name $(LAMBDA_FUNCTION_NAME) \
		--image-uri $(ECR_URI):$(IMAGE_TAG) \
		--region $(AWS_REGION)
	@echo "Lambda function updated successfully ✓"
	@echo "Function: $(LAMBDA_FUNCTION_NAME)"
	@echo "Image: $(ECR_URI):$(IMAGE_TAG)"

cleanup: ## Remove local container and image
	@echo "Cleaning up local container and image for $(CITY)..."
	@echo "Stopping and removing test container..."
	-docker stop $(CONTAINER_NAME)-test 2>/dev/null
	-docker rm $(CONTAINER_NAME)-test 2>/dev/null
	@echo "Removing local image..."
	-docker rmi $(CONTAINER_NAME):$(IMAGE_TAG) 2>/dev/null
	-docker rmi $(ECR_URI):$(IMAGE_TAG) 2>/dev/null
	@echo "Cleanup completed ✓"

clean-all: ## Remove all containers and images for all cities
	@echo "Cleaning up all containers and images..."
	@echo "Removing all test containers..."
	-docker stop sslv-scraper-ogre-test sslv-scraper-jurmala-test sslv-scraper-adazi-test 2>/dev/null
	-docker rm sslv-scraper-ogre-test sslv-scraper-jurmala-test sslv-scraper-adazi-test 2>/dev/null
	@echo "Removing all local images..."
	-docker rmi sslv-scraper-ogre:latest sslv-scraper-jurmala:latest sslv-scraper-adazi:latest 2>/dev/null
	@echo "All cleanup completed ✓"

logs: ## Show logs from the test container
	@echo "Showing logs for $(CONTAINER_NAME)-test..."
	docker logs $(CONTAINER_NAME)-test

status: ## Show status of containers and images
	@echo "=== Container Status ==="
	@docker ps -a --filter "name=sslv-scraper" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "=== Image Status ==="
	@docker images --filter "reference=sslv-scraper*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Quick commands for each city
ogre: ## Quick build and test for Ogre city
	@$(MAKE) build CITY=ogre
	@$(MAKE) test CITY=ogre

jurmala: ## Quick build and test for Jurmala city
	@$(MAKE) build CITY=jurmala
	@$(MAKE) test CITY=jurmala

adazi: ## Quick build and test for Adazi city
	@$(MAKE) build CITY=adazi
	@$(MAKE) test CITY=adazi

# Full deployment pipeline
deploy-ogre: ## Full deployment pipeline for Ogre
	@$(MAKE) build CITY=ogre
	@$(MAKE) test CITY=ogre
	@$(MAKE) deploy CITY=ogre
	@$(MAKE) cleanup CITY=ogre

deploy-jurmala: ## Full deployment pipeline for Jurmala
	@$(MAKE) build CITY=jurmala
	@$(MAKE) test CITY=jurmala
	@$(MAKE) deploy CITY=jurmala
	@$(MAKE) cleanup CITY=jurmala

deploy-adazi: ## Full deployment pipeline for Adazi
	@$(MAKE) build CITY=adazi
	@$(MAKE) test CITY=adazi
	@$(MAKE) deploy CITY=adazi
	@$(MAKE) cleanup CITY=adazi
