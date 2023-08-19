#!/bin/bash

export BUCKET_NAME=audios
export UPLOAD_FILE_SQS=upload-file-sqs

echo "Creating CloudFormation stack..."

# Create the stack using the CloudFormation template
aws --endpoint-url=http://host.docker.internal:4566 --region us-east-1 cloudformation create-stack --stack-name my-stack --template-body file:///infra/infrastructure.yaml

echo "============ ARN for upload file SQS ============"

UPLOAD_FILE_SQS_ARN=$(aws --endpoint-url=http://localstack:4566 sqs get-queue-attributes\
                  --attribute-name QueueArn --queue-url=http://localhost:4566/000000000000/"$UPLOAD_FILE_SQS"\
                  |  sed 's/"QueueArn"/\n"QueueArn"/g' | grep '"QueueArn"' | awk -F '"QueueArn":' '{print $2}' | tr -d '"' | xargs)

echo "============ Set S3 Bucket Notification ============"

aws --endpoint-url=http://localhost:4566 s3api put-bucket-notification-configuration\
    --bucket $BUCKET_NAME\
    --notification-configuration  '{
                                      "QueueConfigurations": [
                                         {
                                           "QueueArn": "'"$UPLOAD_FILE_SQS_ARN"'",
                                           "Events": ["s3:ObjectCreated:*"]
                                         }
                                       ]
                                     }'

echo "CloudFormation stack created."
