import boto3
import json
import datetime
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the desired log level

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Read environment variables for result bucket name
    result_bucket_name = os.environ.get('RESULT_BUCKET_NAME', 'processed-files')

    logger.info(event)

    for record in event['Records']:
        # Extract the S3 bucket name and object key from the SQS message
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        # Log information to CloudWatch Logs
        logger.info(f"File uploaded: {object_key} in bucket {bucket_name}")

        # Prepare the result file content
        result_content = f"| {object_key} | {datetime.datetime.now().isoformat()} |\n"

        now = datetime.datetime.now()

        # Define the result file name
        result_file_name = f'result_file_{now}.csv'

        # Check if the result file already exists and append to it
        try:
            existing_file = s3_client.get_object(Bucket=result_bucket_name, Key=result_file_name)
            existing_content = existing_file['Body'].read().decode('utf-8')
            result_content = existing_content + result_content
        except:
            pass

        # Write the result file to the new S3 bucket
        s3_client.put_object(Bucket=result_bucket_name, Key=result_file_name, Body=result_content)

    return {
        'statusCode': 200,
        'body': json.dumps('Processed message successfully')
    }
