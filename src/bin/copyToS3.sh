#!/bin/bash

# require credentials to be set up in ~/.aws/credentials file using aws access key and secret.
# [ucsd]
# aws_access_key_id=
# aws_secret_access_key=


LOCAL_BUCKET='./data/'
S3_BUCKET='s3://dse-cohort5-group1/'

# we currently only have access to us-east-1 (virginia)
AWS_REGION='us-east-1'

# copies data from local computer to s3. Can also be done with python Boto3 sdk
aws s3 cp $LOCAL_BUCKET $S3_BUCKET --recursive --profile=ucsd --region=us-east-1
