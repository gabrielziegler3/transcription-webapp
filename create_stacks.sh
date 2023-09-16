#!/bin/bash

echo "Creating bucket stacks..."

aws cloudformation create-stack --stack-name lambda-bucket-stack --template-body file://infra/lambda_bucket.yaml

echo "Zipping lambda function..."

cd lambda/

zip -r lambda.zip lambda_function.py

cd ..

echo "Waiting for bucket stack to be created..."

# wait for stack to be created
aws cloudformation wait stack-create-complete --stack-name lambda-bucket-stack

echo "Uploading lambda function to S3..."

aws s3 cp lambda/lambda.zip s3://lambda-bucket-418411734027

echo "Creating stack transcription-webapp"

aws cloudformation create-stack --stack-name transcription-webapp --template-body file://infra/infrastructure.yaml --capabilities CAPABILITY_IAM
