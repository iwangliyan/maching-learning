#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 16:16:59 2018

@author: linzizhan
"""

import pandas as pd

def rain_result(x):
    if type(x) == float:
        return x
    elif x == '-':
        return 0.0
    else:
        return float(x[:-2])
df = pd.read_csv('weather.csv')
df['hour'] = df.time.apply(lambda x: int(x[:2]))
df['date'] = df.day
df = df.drop(['day', 'time'],axis=1)

def onehot(df, col):
    df1 = pd.get_dummies(df[col])
    length = len(df1.columns)
    columns = [col + '_' + str(i + 1) for i in range(length)]
    df1.columns = columns
    df = pd.concat([df, df1], axis = 1)
    del df[col]
    return df

data = pd.read_csv(r'/Volumes/林自展/match/data/data.csv')
data['date'] = data.datetime.apply(lambda x:int(x[:10].replace('-','')))

new = pd.merge(data, df, how='left', on=['date', 'hour'])
new['rain'] = new.rain.apply(lambda x: rain_result(x))
#new['weather'] = pd.get_dummies(new.weather)
new['temp'] = new.temp.apply(lambda x:str(x).replace('℃',''))
new['body_temp'] = new.body_temp.apply(lambda x:str(x).replace('℃',''))
new['wind'] = new.wind.apply(lambda x:str(x).replace('级',''))
new['shidu'] = new.shidu.apply(lambda x:str(x).replace('%',''))
df = onehot(new, 'weather')
df = onehot(df, 'isHoliday')
df = onehot(df, 'wind')
df.to_csv(r'/Volumes/林自展/match/feature_v1.csv', index = False)
#new.to_csv('data_add_wea.csv', index=False)
#df = new[new.loc_id == 1]
#df1 =  df[df.weekday==3]
#import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(10,4))
#ax1 = fig.add_subplot(2,1,1)
#ax2 = fig.add_subplot(2,1,2)
#ax1.plot(range(len(df1)),df1.phone_id)
#ax2.plot(range(len(df1)),df1.rain)
#plt.show()