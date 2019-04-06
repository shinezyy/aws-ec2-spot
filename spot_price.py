from datetime import datetime

import boto3

client = boto3.client('ec2', region_name='ap-southeast-1')

avail_zones = [
    'ap-southeast-1a',
    'ap-southeast-1b',
    'ap-southeast-1c',
]

for az in avail_zones:
    resp = client.describe_spot_price_history(
        InstanceTypes=[
            't2.xlarge',
            't3.xlarge',
            'c1.xlarge',
            'p3.2xlarge',
            'm2.4xlarge',
            'r4.2xlarge',
            'i3.2xlarge',
            'c5d.2xlarge',
            'c5.2xlarge',
            'm5d.2xlarge',
            'm5.2xlarge',
            'r5d.2xlarge',
            'r5.2xlarge',
            'z1d.2xlarge',
        ],
        AvailabilityZone=az,
        StartTime=datetime(2019, 4, 1),
        ProductDescriptions=['Linux/UNIX'],
    )

    print(resp)