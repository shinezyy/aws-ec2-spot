import boto3
from pprint import pprint
from common import *
from os.path import expanduser
import argparse
import common as c

wc = c.CommonClient()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', '--kill', action='store_true',
        help='Kill all spot instances'
    )
    parser.add_argument("-r", "--region", choices=wc.get_regions() + ['all'],
            default=wc.get_default_region())
    args = parser.parse_args()

    client = boto3.client('ec2', region_name=args.region)

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
        'LaunchTime',
        'SpotInstanceRequestId',
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

        is_spot = True
        for k in keys:
            if k in inst:
                j_print(inst[k])
            else:
                is_spot = False
        new_line()

        if not is_spot:
            continue

        if not args.kill:
            with open(expanduser('~/.ec2_ip'), 'w') as f:
                f.write(str(inst['PublicIpAddress']))

            with open(expanduser('~/.ssh/config.d/spot_config_template')) as inf, \
                    open(expanduser('~/.ssh/config.d/spot_config'), "w") as outf:
                for line in inf:
                    if line.strip().startswith("HostName"):
                        outf.write("    Hostname {}".format(inst['PublicIpAddress']))
                        outf.write("\n")
                    else:
                        outf.write(line)

        else:
            resp = client.cancel_spot_instance_requests(
                SpotInstanceRequestIds=[
                    inst['SpotInstanceRequestId'],
                ],
            )
            print(resp)
            resp = client.terminate_instances(
                InstanceIds=[
                    inst['InstanceId'],
                ],
            )
            print(resp)


if __name__ == '__main__':
    main()
