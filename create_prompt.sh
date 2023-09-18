#!/bin/bash

printf "Consider the following project\n"

echo "\`\`\`"

tree -L 2 -I "volume|audio*|*.md"

printf "\`\`\`\n\n"

echo "With the following cloudformation files:"

printf "infra/infrastructure.yaml\n\n"

printf "\`\`\`yaml"

cat ./infra/infrastructure.yaml

printf "\`\`\`\n\n"

echo "infra/lambda_bucket.yaml"

printf "\`\`\`yaml"

cat ./infra/lambda_bucket.yaml

printf "\`\`\`\n\n"

printf "I'm then running the following command to create the stack:\n"
printf "aws cloudformation create-stack --stack-name lambda-buckets --template-body file://infra/lambda_bucket.yaml\n"
printf "aws cloudformation create-stack --stack-name transcription-webapp --template-body file://infra/infrastructure.yaml --capabilities CAPABILITY_IAM\n"
