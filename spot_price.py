from datetime import datetime, timedelta
import boto3
import pandas as pd

from common import *

client = boto3.client('ec2', region_name='ap-southeast-1')

avail_zones = [
    'ap-southeast-1a',
    'ap-southeast-1b',
    'ap-southeast-1c',
]


def main():
    resp = client.describe_spot_price_history(
        InstanceTypes=[
            # 't2.xlarge',
            # 't3.xlarge',
            # 'c1.xlarge',
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
            'z1d.xlarge',
        ],
        StartTime=datetime.today() - timedelta(1),
        ProductDescriptions=['Linux/UNIX'],
    )

    histories = resp['SpotPriceHistory']

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

    ec2config = EC2Config()

    table = []
    for history in histories:
        row = [history[k] for k in keys]

        row += [ec2config.get_config(history['InstanceType'])[k].values[0]
                for k in foreign_keys]
        # print(row)

        row[len(keys)] = int(row[len(keys)].split(' ')[0])  # ECU

        table.append(row)

    table = pd.DataFrame.from_records(table, columns=keys + foreign_keys)
    table = table.sort_values(by='Timestamp')
    table = table.drop_duplicates(
        subset=['AvailabilityZone',
                'InstanceType'], keep='last')

    table['SpotPrice'] = table['SpotPrice'].astype(float)
    table['CostEfficiency'] = table['Compute Units (ECU)'] / table['SpotPrice']

    table = table.sort_values(by='CostEfficiency', ascending=False)
    print(table)
    # for row in table.iterrows():
    #     row = row[1]
    #     print(row)

    # print(resp)


if __name__ == '__main__':
    main()