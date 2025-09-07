


ws-lambda-v2.x is running to bucket city-id-5001-lambda-apts-sale-storage

ws-lambda-v3.x -code in branch - create_json_lambda_dev

milestone 1. locally scrapes - and generates json formatted output with metadata - completed in working_with_no_boto.py
milestone 2. to pass test locally - code only uv run -m app - scrapes and uplads json to S3 bucket


milesstone 3. locally docker container scrapes + uploads json to dev s3 bucket
docker build -t ws-lambda-v3 .


Problem 1: will error becaue AWS credential needed for S3 upload
docker run -p 9000:8080 ws-lambda-v3 <<

Fix 1: credentials can be mounted durinf run:
docker run -p 9000:8080 -v ~/.aws:/root/.aws ws-lambda-v3.1 < local docker S3 upload works

Trigger lambda:
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' 

Problem 2 :
bucket name hardcoded need to pass via docker run parameter

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


M4 - create new dev docker registry in was ecr  using awscli  and push container
M5 - deploy new dev lambda using awscli and use docker from ecr
M6 - add cron trigger for  function 
M7 - add status command and add basic tests commnds to ocnfirn that lambda run

M8 add 2 more cities adazi and jurmala
