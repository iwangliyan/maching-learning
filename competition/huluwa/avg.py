# -*- coding: utf-8 -*-
"""
Created on Sun May 27 19:09:40 2018

@author: wangqian
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle as pkl
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb

def loc_id_cnt(num):
    df = pd.read_csv('./data/%02d.csv'%num)
    df_res = df.groupby(['time_stamp', 'loc_id']).agg({ 'phone_id':'count'})
    df_res.reset_index(inplace=True)
    return df_res

def handle(df):
    # 时间维度
    df['datetime'] = df.time_stamp.apply(pd.to_datetime)
    del df['time_stamp']
    df['month'] = df.datetime.apply(lambda x: x.month)
    df['day'] = df.datetime.apply(lambda x: x.day)
    df['hour'] = df.datetime.apply(lambda x: x.hour)
    df['weekday'] = df.datetime.apply(lambda x: x.weekday())
    df['weekend'] = df.datetime.apply(lambda x: int(x.weekday()>4))
    # 加入假期，节假日
    """
    def isSummer(x):
        if x > '2017-07-15 00:00:00' and x < '2017-09-03:00:00:00':
            return 1
        else:
            return 0

    def isSummerNear(x):
        if x > '2017-07-12 00:00:00' and x < '2017-07-15:00:00:00':
            return 1
        elif x > '2017-09-03 00:00:00' and x < '2017-09-06:00:00:00'::
            return 0 
    """
    def isHoliday(x):
        if x.date() == datetime.date(2017, 4, 4) or  \
        x.date() == datetime.date(2017, 5, 1) or  \
        x.date() == datetime.date(2017, 5, 30) or \
        x.date() == datetime.date(2017, 1, 1) or \
        (x.date() >= datetime.date(2017, 10, 1) 
        and x.date() <= datetime.date(2017, 10, 8)):
            return 1
        else:
            return 0
    df['isHoliday'] = df.datetime.apply(isHoliday)
    return df

def handle_each_loc(n, pre_df):
    loc1 = loc_df[n]
    stamp = datetime.datetime(2017, 12, 1, 0, 0, 0)
    while stamp < datetime.datetime(2018, 1, 1, 0, 0, 0):

        wekdy = stamp.weekday()
        tmp = loc1[loc1.weekday==wekdy]
        tmp = tmp[tmp.hour==stamp.hour]
        try:
            phn_id = tmp.phone_id.mean()
#            length = len(tmp.phone_id[-3:])
#            fenmu = 0
#            fenzi = 0
#            for i in range(1, length+1):
#                fenzi += (tmp.phone_id[-i:].mean()*(7+i))
#                fenmu += (7+i)
#            phn_id = round(fenzi/fenmu)
        except Exception as e:
            phn_id = 0
            print(e)
            print(n, stamp.weekday(), stamp.hour, phn_id)
            print(stamp)
            stamp = stamp + datetime.timedelta(hours=1)
#            continue
        #print(stamp.weekday(), stamp.hour, phn_id)

        append_df = pd.DataFrame()
        append_df['loc_id'] = [n+1]
        append_df['phone_id'] = [phn_id]
        append_df['datetime'] = [stamp]
        append_df['hour'] = [stamp.hour]
        append_df['weekday'] = [stamp.weekday()]

        loc1 = loc1.append(append_df)

        stamp = stamp + datetime.timedelta(hours=1)
#    _ = loc1[loc1.datetime >= '2017-01-01 00:00:00']
    pre_df.append(loc1)
    return pre_df

df = pd.DataFrame()
for i in range(11,12):
    _df = loc_id_cnt(i)
    df = df.append(_df)
#df['datetime'] = df.time_stamp.apply(pd.to_datetime)
#df = df[df.datetime >= datetime.datetime(2017,11,1,0,0,0)]
df = handle(df)
loc_df = []
for i in range(1, 34):
    _df = df[df.loc_id==i]
    _df.reset_index(inplace=True, drop=True)
    loc_df.append(_df)
pre_df = []
for n in range(33):
    print(n)
    pre_df = handle_each_loc(n, pre_df)
res = pd.DataFrame()
for each in pre_df:   
    each['time_stamp'] = each['datetime'].astype(str).apply(lambda x: x[:13])
    each['num_of_people'] = each['phone_id']
    res = res.append(each[['loc_id','time_stamp','num_of_people']])
res = res[res.time_stamp>='2017-12-01 00']
res = res.sort_values(by=['time_stamp','loc_id'])
res.to_csv('res.csv',index=False)
