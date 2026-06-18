#!/bin/bash

echo "=========================================="
echo "AWS Infrastructure Report - $(date)"
echo "=========================================="

echo ""
echo "--- EC2 Instances ---"
aws ec2 describe-instances \
  --region ap-south-1 \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress]' \
  --output table

echo ""
echo "--- S3 Buckets ---"
aws s3api list-buckets \
  --query 'Buckets[*].[Name,CreationDate]' \
  --output table

echo ""
echo "--- IAM Users ---"
aws iam list-users \
  --query 'Users[*].[UserName,CreateDate]' \
  --output table

echo ""
echo "--- IAM Role Policies ---"
aws iam list-attached-role-policies \
  --role-name ec2-s3-role \
  --output table

echo ""
echo "=========================================="
echo "Report Complete"
echo "=========================================="
