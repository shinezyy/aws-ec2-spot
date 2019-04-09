import boto3
import argparse
import pandas as pd
import sys

from pprint import pprint
from datetime import datetime, timedelta

import common as c


def get_instances(n_core: int = None):
    inst_list = c.get_all_types()
    if n_core is None:
        pass
    elif n_core == 4:
        inst_list = [x for x in inst_list if '.xl' in x]
    elif n_core == 8:
        inst_list = [x for x in inst_list if '.2xl' in x]
    elif n_core == 16:
        inst_list = [x for x in inst_list if '.4xl' in x]
    elif n_core == 32:
        inst_list = [x for x in inst_list if '.8xl' in x]
    else:
        assert False
    return inst_list


wc = c.CommonClient()

parser = argparse.ArgumentParser(description='get spot price and process')
parser.add_argument("-s", "--sort", required=True, choices=[
    "price", "ce",
    ])
parser.add_argument("-c", "--cores", choices=[4, 8, 16, 32], type=int)

parser.add_argument("-r", "--region", choices=wc.get_regions() + ['all'],
        default=wc.get_default_region())

parser.add_argument("-z", "--avail-zone", default='ap-southeast-1c')

args = parser.parse_args()

keys = [
    'AvailabilityZone',
    'InstanceType',
    'SpotPrice',
    'Timestamp',
]

foreign_keys = [
    'Compute Units (ECU)',
    # 'Linux On Demand cost',
    'Physical Processor',
    'Clock Speed(GHz)',
]


def get_spot_history(region: str):
    client = wc.get_client(region)
    resp = client.describe_spot_price_history(
        InstanceTypes=get_instances(args.cores),
        StartTime=datetime.today() - timedelta(1),
        ProductDescriptions=['Linux/UNIX'],
    )

    histories = resp['SpotPriceHistory']

    ec2config = c.EC2Config()

    table = []
    for history in histories:
        row = [history[k] for k in keys]

        row += [ec2config.get_config(history['InstanceType'])[k].values[0]
                for k in foreign_keys]
        try:
            row[len(keys)] = int(row[len(keys)].split(' ')[0])  # ECU
        except ValueError as e:
            row[len(keys)] = 0

        table.append(row)
    return table

def main():
    table = []
    if args.region == 'all':
        for region in wc.get_regions():
            print(region)
            table += get_spot_history(region)
    else:
        table = get_spot_history(args.region)

    table = pd.DataFrame.from_records(table, columns=keys + foreign_keys)
    table = table.sort_values(by='Timestamp')
    table = table.drop_duplicates(
        subset=['AvailabilityZone',
                'InstanceType'], keep='last')

    table['SpotPrice'] = table['SpotPrice'].astype(float)
    print(table)

    table = table.sort_values(by='SpotPrice')
    table = table.drop_duplicates(
        subset=['InstanceType'], keep='first')

    table['CostEfficiency'] = table['Compute Units (ECU)'] / table['SpotPrice']

    if args.sort == 'ce':
        table = table.sort_values(by='CostEfficiency', ascending=False)
    else:
        table = table.sort_values(by='SpotPrice', ascending=True)
    print(table)
    # for row in table.iterrows():
    #     row = row[1]
    #     print(row)

    # print(resp)


if __name__ == '__main__':
    main()
