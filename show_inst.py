import boto3
from pprint import pprint
from common import *


def main():
    client = boto3.client('ec2', region_name='ap-southeast-1')

    resp = client.describe_instances()

    if len(resp['Reservations']):
        instances = resp['Reservations'][0]['Instances']
    else:
        return
    # pprint(instances)

    keys = [
        'InstanceType',
        # 'KeyName',
        'PublicIpAddress',
        # 'ImageId',
        'InstanceId',
        # 'InstanceLifecycle',
        'SpotInstanceRequestId',
        'LaunchTime',
    ]

    # header
    j_print('AvaliZone')
    for k in keys:
        j_print(k)
    new_line()

    for inst in instances:
        if inst['State']['Name'] == 'terminated':
            continue
        j_print(inst['Placement']['AvailabilityZone'])
        for k in keys:
            j_print(inst[k])
        new_line()


if __name__ == '__main__':
    main()
