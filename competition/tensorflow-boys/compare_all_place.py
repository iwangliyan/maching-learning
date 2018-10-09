# -*- coding: utf-8 -*-

import pandas as pd
from cleaning_method import old2new
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




if __name__ == '__main__':
    file0 = 'data/ori_train.csv'
    df00 = pd.read_csv(file0, sep=',', header=None, dtype=object)
    df0 = old2new(df00)
    df0['people'] = df0['people'].apply(pd.to_numeric)
    df0 = df0.reindex(columns=['date', 'people'])
    df0['date'] = df0['date'].apply(lambda x:  str(datetime.strptime(x, '%Y-%m-%d:%H').date()-timedelta(1)))
    group0 = df0.groupby('date')
    res0 = group0['people'].mean()
    
    file1 = 'data/train3.csv'
    df1 = old2new(pd.read_csv(file1, sep=',', header=None))
    df1['people'] = df1['people'].apply(pd.to_numeric)
    df1 = df1.reindex(columns=['date', 'people'])
    df1['date'] = df1['date'].apply(lambda x: str(datetime.strptime(x, '%Y-%m-%d:%H').date()))
    group1 = df1.groupby('date')
    res1 = group1['people'].mean()
    
    
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel('t', fontproperties='SimHei')
    ax.set_ylabel('people number', fontproperties='SimHei')
    res0['2017-10-10':].plot(label='2016 old data', style='r.-')
    res1.plot(label='2017 new data', style='b.-')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
    
    