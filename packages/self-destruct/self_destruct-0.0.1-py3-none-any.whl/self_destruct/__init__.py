import sys

import boto3
from ec2_metadata import ec2_metadata
from requests.exceptions import ConnectTimeout


def self_destruct(terminate: bool = True):
    try:
        region = ec2_metadata.region
    except ConnectTimeout:
        print("Cannot access metadata -- likely "
              "not running on an EC2 instance")
        sys.exit(0)
    ec2 = boto3.resource('ec2', region_name=region)
    ids = [ec2_metadata.instance_id]
    if terminate:
        ec2.instances.filter(InstanceIds=ids).terminate()
    else:
        ec2.instances.filter(InstanceIds=ids).stop()
