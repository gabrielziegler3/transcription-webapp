#!/bin/bash

echo "Creating CloudFormation stack..."

# Create the stack using the CloudFormation template
aws --endpoint-url=http://host.docker.internal:4566 --region us-east-1 cloudformation create-stack --stack-name my-stack --template-body file:///infra/queue.yaml

echo "CloudFormation stack created."
