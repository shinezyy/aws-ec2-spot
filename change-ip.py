import boto3
import argparse
import json
from pprint import pprint

import common as c


def release_static_ip(client, inst):
    resp = client.release_static_ip(staticIpName=f'{inst}-static-ip')
    pprint(resp)

def alloc_static_ip(client, inst):
    try:
        resp = client.allocate_static_ip(staticIpName=f'{inst}-static-ip')
        pprint(resp)
    except Exception as e:
        print(e)
    client.attach_static_ip(staticIpName=f'{inst}-static-ip',
            instanceName=inst)

def print_ip(client, inst):
    insts = dict(client.get_instances())['instances']
    # pprint(insts)
    instance = [i for i in insts if i['name'] == inst][0]
    # pprint(instance)
    print('New IP addr:', instance['publicIpAddress'])


def main():

    parser = argparse.ArgumentParser()
    lc = c.CommonClient(t='lightsail')

    parser.add_argument("-r", "--region", required=True,
            default=lc.get_default_region())
    parser.add_argument("-s", "--show-instance-name", action='store_true')
    parser.add_argument("-i", "--instance-name")
    args = parser.parse_args()

    assert args.instance_name or args.show_instance_name

    client = lc.get_client(args.region)
    insts = dict(client.get_instances())['instances']
    inst_names = [e['name'] for e in insts]

    if args.show_instance_name:
        pprint(insts)
        print(inst_names)
        return

    pprint(insts)
    inst = [i for i in insts if i['name'] == args.instance_name][0]

    if inst['isStaticIp']:
        release_static_ip(client, args.instance_name)
    else:
        alloc_static_ip(client, args.instance_name)
    print_ip(client, args.instance_name)


if __name__ == '__main__':
    main()
