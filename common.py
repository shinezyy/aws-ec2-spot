from datetime import datetime
import pytz
import pandas as pd


tz = pytz.timezone('Asia/Shanghai')


def j_print(s):
    if isinstance(s, datetime):
        # print(pytz.utc.localize(s, is_dst=None).astimezone(tz), end='')
        print(s.astimezone(tz).strftime('%y.%m.%d-%H:%M'), end='')
        # print(s.replace(tzinfo=tz), end='')
    else:
        print(str(s).ljust(24, ' '), end='')


def new_line():
    print('')


freq_list = [
    ('Intel Xeon Platinum 8175', '2.5GHz'),
    ('Intel Xeon Platinum 8151', '4.0GHz'),
]


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


