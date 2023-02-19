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


## How to test lambda function locally and update  
1. Docker cotainer must be built on x86_64 architecture (ARM seems to be supported as well)

2. Test local container build #docker build -t docker-lambda .

[ec2]lambda-build]$ docker images
REPOSITORY                 TAG       IMAGE ID       CREATED          SIZE
docker-lambda              latest    00501cfe1339   11 seconds ago   625MB


3. Test local container start
docker run -p 9000:8080 docker-lambda

[ec2]$ docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                                       NAMES
c0f865256da5   docker-lambda   "/lambda-entrypoint.…"   53 seconds ago   Up 52 seconds   0.0.0.0:9000->8080/tcp, :::9000->8080/tcp   zen_varahamihira


4. Test lambda execution locally (use curl to trigger function call)
In a separate terminal, you can then locally invoke the function using curl :
Important (time to complete function run can take 3-4 min please allow time before curl will return 200 and message that file uploaded to to S3 with sucess)

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'


5.  Upload the image to the Amazon ECR repository (log in to AWS console ECR GUI to get login and  push steps)
In the following commands, replace 123456789012 with your AWS account ID and set the region value to the region where you want
to create the Amazon ECR repository.


aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com    


6. TAG image wit latest tag 
docker tag docker-lambda:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/docker-lambda:latest


7. Push image to ECR 
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/docker-lambda:latest        


8. Open AWS labmbda GUI and use update image option

