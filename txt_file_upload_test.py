#!/usr/bin/env python3


import datetime
import boto3


def upload_text_file_to_s3(file_path, bucket_name, s3_key):
    """
    Uploads a text file to an S3 bucket.

    :param file_path: The local path to the text file.
    :param bucket_name: The name of the S3 bucket to upload the file to.
    :param s3_key: The S3 key to use for the uploaded file.
    """

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the file to S3
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, bucket_name, s3_key)


def add_datetime_to_filename(filename):
    """
    Adds the current date and time to a filename.

    :param filename: The original filename.
    :return: The new filename with the current date and time added.
    """

    # Get the current date and time in YYYY-MM-DDTHH-MM-SS format
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # Add the current date and time to the filename
    new_filename = filename.replace('.txt', f'-{current_datetime}.txt')

    return new_filename


def main():
    original_filename = "Ogre-raw-data-report.txt"
    new_filename = add_datetime_to_filename(original_filename)
    S3_bucket="lambda-ogre-scraped-data"
    upload_text_file_to_s3(original_filename, S3_bucket, new_filename )
    
    # Output: Ogre-raw-data-report-2023-02-18.txt (if today is February 18, 2023)
    print(f"File {new_filename} was uploaded to S3 bucket sucessfilly" )


main()
