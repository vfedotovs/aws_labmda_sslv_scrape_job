# AWS Labmda function for scraping data from www.ss.lv


## General info
This function will scrape apartments for sale data from ss.lv for once city and will upload data as json file in AWS S3 bucket.


## Technologies
Project is created with:
* Python 3.8
* requests 
* bs4
* AWS lambda
* AWS S3


## Test your function locally using the docker build and docker run commands.

```sh
# Build you doker image:
docker build -t <image name> .

# Run your image locally:
docker run -p 9000:8080 <image name>


# In a separate terminal, you can then locally invoke the function using cURL:
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
```

Deploying the function to ECR, check out the AWS documentation:

Creating a ECR repository:
https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html

Pushing image to ECR:
https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
