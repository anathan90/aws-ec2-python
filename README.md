# aws-ec2-python
Managing EC2 Instances on Amazon Web Services (AWS) using Python

## Overview
This simple Python (2.7) module helps launch, modify (in terms of auto-termination) and terminate EC2 instances on Aamazon Web 
Services (AWS).

## AWS Requirements
1. Create AWS account (https://aws.amazon.com/).
2. Create EC2 key pairs.
3. Create EC2 instance that will serve as image (AMI) template.
4. Configure your machine with following AWS credentials (command is aws configure):
** Access key ID
** Secret access key
5. Create IAM role for EC2 instances - in our example we've set up .

### Files


### Examples
## We will launch an istance and terminate it manually.
## We need to define a number of parameters (they are all listed in configuration.json file, which can be read before launching any instances): 
* aws_region
* ami_id
* ec2_instance_profile_name
* instance_type
* security_group
* key_name
```
>>> import aws 
>>> import boto.ec2
>>> conn_ec2 = boto.ec2.connect_to_region(aws_region) #setting up ec2 connection, need to specify aws_region, e.g. 'us-east-2'
>>> ec2_instance_id = aws.launch_instance(conn_ec2, aws_region, ami_id, ec2_instance_profile_name, instance_type, security_group, key_name) #launching instance
>>> aws.get_all_ec2_instance_ids(conn_ec2) #see instance ids for all running or pending EC2 instances
['i-0a15b7223c23aaf38']
>>> aws.terminate_instances(conn_ec2, [ec2_instance_id])
```
