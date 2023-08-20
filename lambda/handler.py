import json

def lambda_handler(event, context):
    for record in event['Records']:
        # Extract the S3 bucket name and object key from the SQS message
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        print(f"File uploaded: {object_key} in bucket {bucket_name}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processed message successfully')
    }
