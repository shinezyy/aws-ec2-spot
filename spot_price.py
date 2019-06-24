import boto3
import argparse
import pandas as pd
import sys
import json

from datetime import datetime, timedelta

import common as c


def get_spot_int_rate(region: str, inst_type: str):
    rate = json.load(open('./data/spot-advisor-data.json'))['spot_advisor']
    region_rate = rate[region]['Linux']
    return int(region_rate[inst_type]['r'])


def get_instances(n_core: int = None, t: str = None):
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
    if t is None:
        pass
    else:
        inst_list = [x for x in inst_list if t in x]

    return inst_list


wc = c.CommonClient()

parser = argparse.ArgumentParser(description='get spot price and process')
parser.add_argument("-s", "--sort", required=True, choices=[
    "price", "ce", "ir"
    ])
parser.add_argument("-c", "--cores", choices=[1, 2, 4, 8, 16, 32], type=int)

parser.add_argument("-r", "--region", choices=wc.get_regions() + ['all'],
        default=wc.get_default_region())

parser.add_argument("-z", "--avail-zone", default='ap-southeast-1c')

parser.add_argument("-t", "--type")

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
        InstanceTypes=get_instances(args.cores, args.type),
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

        try:
            row.append(get_spot_int_rate(region, history['InstanceType']))
        except KeyError as e:
            row.append(100)

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

    table = pd.DataFrame.from_records(table, columns=keys + foreign_keys + ['intr rate'])
    table = table.sort_values(by='Timestamp')
    table = table.drop_duplicates(
        subset=['AvailabilityZone',
                'InstanceType'], keep='last')

    table['SpotPrice'] = table['SpotPrice'].astype(float)

    # table = table.sort_values(by='SpotPrice')

    table['CostEfficiency'] = table['Compute Units (ECU)'] / table['SpotPrice']

    small_is_better = {
            }

    if args.sort == 'ce':
        table = table.sort_values(by=['CostEfficiency', 'intr rate', 'SpotPrice',],
                ascending=[False, True, True,])
    elif args.sort == 'price':
        table = table.sort_values(by=['SpotPrice', 'intr rate', 'CostEfficiency',],
                ascending=[True, True, False])
    else:
        table = table.sort_values(by=['intr rate', 'SpotPrice', 'CostEfficiency',],
                ascending=[True, True, False])

    print(table)
    table.to_csv('./table-{}.csv'.format(args.cores), index=None)

    if args.type is None:
        table = table.drop_duplicates(
            subset=['InstanceType'], keep='first')
        print(table)

    # for row in table.iterrows():
    #     row = row[1]
    #     print(row)

    # print(resp)


if __name__ == '__main__':
    main()
