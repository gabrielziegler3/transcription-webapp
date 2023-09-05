#!/bin/bash
echo "########### Setting up localstack profile ###########"
export AWS_REGION=us-east-1

aws configure set aws_access_key_id test --profile=localstack
aws configure set aws_secret_access_key test --profile=localstack
aws configure set region $AWS_REGION --profile=localstack

export AWS_DEFAULT_PROFILE=localstack
export BUCKET_NAME=audios
export UPLOAD_FILE_SQS=upload-file-sqs
export LAMBDA_BUCKET=lambda-bucket

echo "============ Creating CloudFormation stack... ============"

# Create the stack using the CloudFormation template
aws --endpoint-url=http://localhost:4566 --region $AWS_REGION cloudformation create-stack --stack-name my-stack --template-body file:///infra/infrastructure.yaml

echo "============ ARN for upload file SQS ============"

UPLOAD_FILE_SQS_ARN=$(aws --endpoint-url=http://localhost:4566 sqs get-queue-attributes --region "$AWS_REGION" \
                      --attribute-name QueueArn --queue-url=http://localhost:4566/000000000000/"$UPLOAD_FILE_SQS"\
                      |  sed 's/"QueueArn"/\n"QueueArn"/g' | grep '"QueueArn"' | awk -F '"QueueArn":' '{print $2}' | tr -d '"' | xargs)

echo "============ Zipping the Lambda function... ============"

# Create the ZIP file
zip -r /lambda/lambda.zip /lambda/

echo "============ Inserting lambda zip into Lambda bucket ============"

aws --endpoint-url=http://localhost:4566 --region $AWS_REGION s3 cp /lambda/lambda.zip s3://$LAMBDA_BUCKET/lambda.zip

echo "============ Set S3 Bucket Notification ============"

aws --endpoint-url=http://localhost:4566 s3api put-bucket-notification-configuration\
    --bucket $BUCKET_NAME\
    --region $AWS_REGION\
    --notification-configuration  '{
                                      "QueueConfigurations": [
                                         {
                                           "QueueArn": "'"$UPLOAD_FILE_SQS_ARN"'",
                                           "Events": ["s3:ObjectCreated:*"]
                                         }
                                       ]
                                     }'

echo "============ CloudFormation stack created ============"
