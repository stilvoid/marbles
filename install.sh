#!/bin/bash

set -e

ZIP_FILE=lambda.zip

STACK_NAME=marbles

bucket="$1"
site_name="$2"

if [ -z $bucket ]; then
    read -p "S3 bucket to store template assets (e.g. mybucket): " bucket
fi

if [ -z $site_name ]; then
    read -p "Site name: " site_name
fi

echo "Packaging code..."

./package.sh

echo "Deploying application"

# Use existing bucket if we've deployed before
input_bucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME 2>/dev/null | jq -r .Stacks[0].Outputs[0].OutputValue)
if [ -z $input_bucket ]; then
    input_bucket="${STACK_NAME}-$(pwgen -A -0 8 1)"
fi

# Do the deployment
aws cloudformation package --template-file template.yaml --s3-bucket $bucket --output-template-file template.out.yaml >/dev/null
aws cloudformation deploy --template-file template.out.yaml --stack-name $STACK_NAME --parameter-overrides BucketName=$input_bucket SiteName="$site_name" --capabilities CAPABILITY_IAM >/dev/null

# Clean up
rm $ZIP_FILE
rm template.out.yaml

website=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq -r .Stacks[0].Outputs[1].OutputValue)

echo
echo "Upload markdown files to $input_bucket (e.g. aws s3 cp README.md s3://$input_bucket)."
echo
echo "The website will then be updated at $website"
echo
