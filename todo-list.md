
Plan:
-[x] Write code for lambda v2
-[x] Deploy v2 code to aws lambda using GUI for daily scrape job to S3 bucket.

Status: ws-lambda-v2.x is running to bucket city-id-5001-lambda-apts-sale-storage


ws-lambda-v3.x -code in branch - create_json_lambda_dev
-[x] Write improved v3 lambda code
-[ ] Deploy improved v3 lambda code to AWS using cli or makefile for at least 3-6 cities

Tasks:
-[x] T001 write v3 lambda code that scrapes all ads for single city
      and generates json formatted output with metadata - completed in working_with_no_boto.py
-[x] T002 write v3 code and test with 'uv run -m app'- scrapes all ads and uploads json to S3 bucket
      outside docker

-[x] T003 write v3 code and test locally inside docker (should scrape all ads and upload to S3 dev-bucket) 
Steps to test:
docker build -t ws-lambda-v3 .

Problem 1: will error becaue AWS credential needed for S3 upload
docker run -p 9000:8080 ws-lambda-v3 <<

Fix 1: credentials can be mounted during run:
docker run -p 9000:8080 -v ~/.aws:/root/.aws ws-lambda-v3.1 < local docker S3 upload works

Trigger lambda:
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' 

Problem 2 :
S3 bucket name is hardcoded - need to write command via docker to pass it as env parameter

Fix 2: docker-compose up + .env file
docker-compose.yaml
version: '3.8'
services:
  scraper:
    image: ws-lambda-v3.1
    ports:
      - "9000:8080"
    volumes:
      - ~/.aws:/root/.aws
    environment:
      - S3_BUCKET_NAME=my-custom-bucket
      - AWS_REGION=eu-west-1

- [x] T004 Create dev docker registry in AWS ECR using awscli
aws ecr create-repository --repository-name sslv-scraper-ogre --region us-east-1

(Ensure that in Dockerfile platform is set to x86)
build --platform linux/amd64 -t lambda-v3-ogre:3.1 .  < works

tag
docker tag lambda-v3-ogre:3.1 370162467217.dkr.ecr.us-east-1.amazonaws.com/lambda-v3-ogre:latest - works


- [x] T005 Push container to ECR via awscli
login
aws ecr get-login-password --region us-east-1| docker login --username AWS --password-stdin 370162467217.dkr.ecr.us-east-1.amazonaws.com
Login Succeeded   

push
docker push 370162467217.dkr.ecr.us-east-1.amazonaws.com/lambda-v3-ogre:latest  - works

- [ ] T006 Create new dev lambda using awscli and use docker from ECR

create lambda  - fails
aws lambda create-function \
  --function-name dev-lambda-v3-ogre \
  --package-type Image \
  --code ImageUri=370162467217.dkr.ecr.us-east-1.amazonaws.com/lambda-v3-ogre \
  --role arn:aws:iam::370162467217:role/lambda-execution-role \
  --timeout 300 \
  --memory-size 256

- [ ] T007 Create cron trigger job for lambda function using awscli
- [ ] T008 Create status command and add basic tests commnds to confirm that lambda is deployed and was run
- [ ] T009 Deploy 3-5 cities ogre + adazi + jurmala + jelgava + valmiera
- [ ] T010 Test and document rollback
