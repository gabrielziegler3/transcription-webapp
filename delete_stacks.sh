#!/bin/bash

echo "Deleting files from buckets..."

aws s3 rm --recursive s3://audios-418411734027
aws s3 rm --recursive s3://lambda-bucket-418411734027

echo "Deleting stack transcription-webapp..."

aws cloudformation delete-stack --stack-name transcription-webapp

# echo "Deleting bucket..."
#
# aws s3api delete-bucket --bucket audios-418411734027

echo "Waiting for stack to be deleted..."

# wait for stack to be deleted
aws cloudformation wait stack-delete-complete --stack-name transcription-webapp

echo "Deleting stack lambda-bucket-stack..."

aws cloudformation delete-stack --stack-name lambda-bucket-stack
