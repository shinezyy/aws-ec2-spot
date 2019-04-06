import boto3

resource = boto3.resource('ec2', region_name='ap-southeast-1')

avail_zones = [
    'ap-southeast-1a',
    'ap-southeast-1b',
    'ap-southeast-1c',
]

instance = resource.create_instances(
    InstanceType=
    # 't2.xlarge',
    # 't3.xlarge',
    # 'c1.xlarge',
    # 'p3.2xlarge',
    # 'm2.4xlarge',
    # 'r4.2xlarge',
    # 'i3.2xlarge',
    # 'c5d.2xlarge',
    'c5.2xlarge',
    # 'm5d.2xlarge',
    # 'm5.2xlarge',
    # 'r5d.2xlarge',
    # 'r5.2xlarge',
    # 'z1d.2xlarge',
    # 'z1d.xlarge',

    LaunchTemplate={
        'LaunchTemplateId': 'lt-06db38f15ad93e916',
        'Version': '4',
    },
    # Placement={
    #     'AvailabilityZone': avail_zones[2],
    # },
    MinCount=1,
    MaxCount=1,
    KeyName='zyy-console'
)

print(instance)