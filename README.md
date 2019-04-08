# aws-ec2-python
Managing EC2 Instances on Amazon Web Services (AWS) using Python.

## Overview
This simple Python (2.7) module helps launch, modify (in terms of auto-termination) and terminate EC2 instances on Amazon Web 
Services (AWS).

## AWS Requirements
1. Create AWS account (https://aws.amazon.com/).
2. Create EC2 key pairs.
3. Create EC2 instance that will serve as image (AMI) template.
4. Configure your machine with following AWS credentials (command is aws configure):
** Access key ID
** Secret access key
5. Create IAM role for EC2 instances - for Example 2 we've set up an IAM role that allows EC2 instances to communicate with S3.

### Files
* aws.py: python module containing all functions 
* configuration.json: json file containing all the parameters that need to be defined in order to use the aws.py functions.
* init.txt: sample bash script to be executed on EC2 instance immediately after it has been launched (note that S3 bucket needs to be specified)

### Examples
For both examples we need to define a number of parameters - they are all listed in configuration.json file, which can be read before launching any instances:
* aws_region
* ami_id
* ec2_instance_profile_name
* instance_type
* security_group
* key_name

#### Example 1
In this example we will launch an EC2 istance, inspect all running and pending instances, and terminate it manually. We assume that all variables listed above have been specified.
```
>>> import aws 
>>> import boto.ec2
>>> conn_ec2 = boto.ec2.connect_to_region(aws_region) #setting up ec2 connection, need to specify aws_region, e.g. 'us-east-2'
>>> ec2_instance_id = aws.launch_instance(conn_ec2, aws_region, ami_id, ec2_instance_profile_name, instance_type, security_group, key_name) #launching instance
>>> aws.get_all_ec2_instance_ids(conn_ec2) #see instance ids for all running or pending EC2 instances
['i-0a15b7223c23aaf38']
>>> aws.terminate_instances(conn_ec2, [ec2_instance_id])
```
#### Example 2
In this example we will launch an EC2 instance, automatically run a simple script after launching it (init.txt - the script creates a new file, and uploads to an S3 bucket), and make the EC2 instance terminate itself immediately after the script has been executed. We assume that all variables listed above have been specified.
```
>>> import aws 
>>> import boto.ec2
>>> conn_ec2 = boto.ec2.connect_to_region(aws_region) #setting up ec2 connection, need to specify aws_region, e.g. 'us-east-2'
>>> init_file_path = './init.txt' #specifying path to init.txt file, in order to pass it as parameter to launch_instance method
>>> ec2_instance_id = aws.launch_instance(conn_ec2, aws_region, ami_id, ec2_instance_profile_name, instance_type, security_group, key_name, init_file_path) #launching instance
>>> aws.modify_auto_termination(conn_ec2,ec2_instance_id) #modify EC2 instance to allow auto-termination after script is done running
```
