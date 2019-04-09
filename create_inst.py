import boto3
import argparse
import common as c

wc = c.CommonClient()

def main():
    parser = argparse.ArgumentParser(description='open an instance')
    parser.add_argument('-t', '--instance-type', required=True, choices=c.get_all_types())
    parser.add_argument("-r", "--region", choices=wc.get_regions() + ['all'],
            default=wc.get_default_region())
    args = parser.parse_args()

    resource = boto3.resource('ec2', region_name=args.region)

    # avail_zones = [
    #     'ap-southeast-1a',
    #     'ap-southeast-1b',
    #     'ap-southeast-1c',
    # ]

    instance = resource.create_instances(
        InstanceType=args.instance_type,
        LaunchTemplate={
            'LaunchTemplateId': 'lt-03eecea2ddd365870',
            'Version': '1',
        },
        # Placement={
        #     'AvailabilityZone': avail_zones[2],
        # },
        MinCount=1,
        MaxCount=1,
        KeyName='zyy-console'
    )

    print(instance)

if __name__ == '__main__':
    main()
