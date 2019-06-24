from datetime import datetime
import pytz
import pandas as pd
import boto3


tz = pytz.timezone('Asia/Shanghai')


def j_print(s):
    if isinstance(s, datetime):
        # print(pytz.utc.localize(s, is_dst=None).astimezone(tz), end='')
        print(s.astimezone(tz).strftime('%y.%m.%d-%H:%M'), end='')
        # print(s.replace(tzinfo=tz), end='')
    else:
        print(str(s).ljust(26, ' '), end='')


def new_line():
    print('')


def get_all_types():
    return [
            'z1d.4xlarge',
            'z1d.2xlarge',
            'z1d.xlarge',

            'c5.8xlarge',

            'c5d.4xlarge',
            'c5.4xlarge',
            'c5n.4xlarge',

            'c5d.2xlarge',
            'c5.2xlarge',
            'c5n.2xlarge',

            'c5d.xlarge',
            'c5.xlarge',
            'c5n.xlarge',

            'r5d.4xlarge',
            'r5.4xlarge',
            'r5a.4xlarge',

            'r5d.2xlarge',
            'r5.2xlarge',
            'r5a.2xlarge',

            'r5d.xlarge',
            'r5.xlarge',
            'r5a.xlarge',

            'm5d.4xlarge',
            'm5.4xlarge',
            'm5a.4xlarge',

            'm5d.2xlarge',
            'm5.2xlarge',
            'm5a.2xlarge',

            'm5d.xlarge',
            'm5.xlarge',
            'm5a.xlarge',

            'c4.8xlarge',
            'c4.4xlarge',
            'c4.2xlarge',
            'c4.xlarge',

            'c3.8xlarge',
            'c3.4xlarge',
            'c3.2xlarge',
            'c3.xlarge',

            't3.2xlarge',
            't3.xlarge',

            't2.2xlarge',
            't2.xlarge',
            ]


freq_list = [
    ('Intel Xeon Platinum 8175', '2.5GHz'),
    ('Intel Xeon Platinum 8151', '4.0GHz'),
]


class CommonClient:
    def __init__(self, t='ec2'):
        self.regions = None
        self.azs = None
        self.default_region = 'ap-southeast-1'
        self.t = t
        self.client = boto3.client(self.t, self.default_region)

    def get_regions(self):
        if self.regions is None:
            resp = self.client.describe_regions()
            self.regions = [dic['RegionName'] for dic in resp['Regions']]
        return self.regions

    def get_client(self, region='ap-southeast-1'):
        return boto3.client(self.t, region)

    def get_az(self, region: str):
        self.client = boto3.client(self.t, region)
        resp = self.client.describe_availability_zones(Filters=[{
            'Name': 'region-name', 'Values': [region]
            }])
        self.azs = [dic['ZoneName'] for dic in resp['AvailabilityZones']]
        return self.azs

    def get_cached_az(self):
        return self.azs

    def get_default_region(self):
        return self.default_region


class EC2Config:
    def __init__(self):
        self.df = pd.read_csv(
            './data/ec2-comparison.csv', sep=',',
            index_col=None,
            header=0
        )

        for cpu, freq in freq_list:
            self.df.loc[self.df['Physical Processor'] == cpu,
                        'Clock Speed(GHz)'] = freq

    def get_config(self, api_name: str):
        return self.df[self.df['API Name'] == api_name]

    def filter_config(self, fuzzy_name: str, ncpu: int):
        pass
        # return self.df[
        #     self.df['API Name'] == fuzzy_name \
        #     and  self.df['API Name'] ==]


def main():
    ec2config = EC2Config()


if __name__ == '__main__':
    main()



