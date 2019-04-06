import boto3
from pprint import pprint
from common import *
from os.path import expanduser


def main():
    client = boto3.client('ec2', region_name='ap-southeast-1')

    resp = client.describe_instances()

    if len(resp['Reservations']):
        # pprint(resp['Reservations'])
        instances = [resp['Reservations'][i]['Instances'][0]
                     for i in range(0, len(resp['Reservations']))]
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
        with open(expanduser('~/.ec2_ip'), 'w') as f:
            f.write(str(inst['PublicIpAddress']))


if __name__ == '__main__':
    main()
