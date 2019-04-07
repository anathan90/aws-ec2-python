import boto.ec2
import json
from optparse import OptionParser

def get_all_ec2_instance_ids(conn_ec2):
    '''
    Function to get id's of all running and pending EC2 instances

    Args:
        conn_ec2 (boto.ec2.connection.EC2Connection): connector used to obtain info on EC2 instances
    Returns:
        instance_ids: list of ids for all running and pending EC2 instances.
    '''

    instance_ids = []
    reservations = conn_ec2.get_all_reservations(filters={'instance-state-name': 'running'}) + \
                   conn_ec2.get_all_reservations(filters={'instance-state-name': 'pending'})
    for reservation in reservations:
        for instance in reservation.instances:
            instance_id = str(instance).split(":")[1]
            instance_ids.append(instance_id)

    return instance_ids

def launch_instance(conn_ec2, s3_bucket, aws_region, ami_id, ec2_instance_profile_name,
                     instance_type, security_group, key_name, init_file_path=None):
    '''
    Function launches ec2 instances

    Args:
        conn_ec2 (boto.ec2.connection.EC2Connection): EC2 connector
        s3_bucket (str): name of S3 bucket
        aws_region (str): name of AWS region (e.g. "us-east-2")
        ami_id (str): id corresponding to AMI template        
        ec2_instance_profile_name (str): EC2 instance profile name is used to set up communication of EC2 instance
                                         with S3
        instance_type (str): size of EC2 instance (cheapest option is t2.nano)
        security_group (str): AWS security group
        key_name (str): private key name in case we need to SSH into any EC2 instance
    Returns:
        ec2_instance_id_new: id of newly launched EC2 instance
    '''
    
    ec2_instance_ids = get_all_ec2_instance_ids(conn_ec2)

    
    if init_file_path:
        with open(init_file_path, 'r') as f:
            user_data = f.read()
    else:
        user_data = ""

    conn_ec2.run_instances(str(ami_id), instance_profile_name=str(ec2_instance_profile_name),
                instance_type=str(instance_type), security_group_ids=[str(security_group)], key_name=str(key_name),
                user_data=user_data)

    ec2_instance_ids_updated = get_all_ec2_instance_ids(conn_ec2)
    
    ec2_instance_id_new = list(set(ec2_instance_ids_updated) - set(ec2_instance_ids))[0]

    return ec2_instance_id_new


def modify_auto_termination(conn_ec2,ec2_instance_id):
    '''
    Function modifies termination behavior so that EC2 instances can terminate themselves

    Args:
        conn_ec2 (boto.ec2.connection.EC2Connection): EC2 connector
        ec2_instance_id: id for EC2 instance to be modified
    Returns:
        None
    '''
    
    conn_ec2.modify_instance_attribute(instance_id=ec2_instance_id,attribute="instanceInitiatedShutdownBehavior",
                                           value="terminate")                                           

def terminate_instances(conn_ec2,ec2_instance_ids):
    '''
    Function terminates EC2 instance

    Args:
        conn_ec2 (boto.ec2.connection.EC2Connection): EC2 connector
        ec2_instance_ids: list of EC2 instance ids to be terminated
    Returns:
        None
    '''
    
    conn_ec2.terminate_instances(instance_ids=ec2_instance_ids)
