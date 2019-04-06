import boto3

resource = boto3.resource('ec2', region_name='ap-southeast-1')

avail_zones = [
    'ap-southeast-1a',
    'ap-southeast-1b',
    'ap-southeast-1c',
]

instance = resource.create_instances(
    InstanceType='t3.xlarge',
    LaunchTemplate={
        'LaunchTemplateId': 'lt-06db38f15ad93e916',
        'Version': '2',
    },
    MinCount=1,
    MaxCount=1,
    KeyName='zyy-console'
)
