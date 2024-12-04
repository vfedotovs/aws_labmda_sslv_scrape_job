FROM amazon/aws-lambda-python:3.9

# copy requirements.txt to container
COPY requirements.txt ./

# installing dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy function code to container
COPY app.py ./

# setting the CMD to your handler file_name.function_name
CMD [ "app.handler" ]
