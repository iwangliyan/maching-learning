# !usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os


def old2new(df):
    df[1] = df[1].apply(num2date)
    df = df.sort_values([1, 0])
    df.columns = ['place', 'date', 'people']
    return df


def num2date(num, year='2017'):
    num = str(num)
    out = str(year) + '-' + num[:2] + '-' + num[2: 4] + ':' + num[4:]
    return out
    

def csv2json(file, year=2017, save_path='data/trains.json'):
    df = pd.read_csv(file, sep=',', header=None)
    df[1] = df[1].apply(num2date)
    df = df.sort_values([1, 0])
    df.columns = ['place', 'date', 'people']
    df_res = df.reindex(columns=['date', 'place', 'people', 'week', 'holiday'])
    df_res['week'] = df_res['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d:%H').weekday()+1)
    df_res['holiday'] = df_res['week'].apply(lambda x: 1 if x in [6, 7] else 0)
    res = df_res.to_json(orient='records')
    if os.path.exists(save_path):
        raise OSError('文件已存在，无法保存！')
    with open(save_path, mode='w+', encoding='utf-8') as f:
        f.write(res)
    f.close()
    
       

if __name__ == '__main__':
    file = 'data/train3.csv'
    csv2json(file)
    