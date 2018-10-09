# -*- coding: utf-8 -*-
"""
Created on Sat May 26 11:55:36 2018

@author: linzizhan
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

def load_weather():
	w = pd.read_csv('weather.csv')
	w['datetime'] = (w.day.astype(str) + ' '+ w.time + ':00').apply(pd.to_datetime)
	w['body_temp'] = w.body_temp.apply(lambda x: str(x).replace('℃','')).astype(int)
	w['temp'] = w.temp.apply(lambda x: str(x).replace('℃','')).astype(int)
	w['wind'] = w.wind.apply(lambda x: int(x[:-1]) if x != '-' else 0)
	w['shidu'] = w.shidu.apply(lambda x: int(x[:-1]))
	w['rain'] = w.rain.apply(lambda x: float(x[:-2]) if x != '-' else 0)
	del w['day']
	del w['time']
	w.head()
	return w
def handle_features(each, w):
    df1 = pd.merge(each, w, on='datetime', how='inner')
    df1 = df1.dropna(axis=0)
    df1.weather.replace({u'晴天':1,
                         u'晴朗':1, 
                         u'局部多云':1,
                         u'多云': 1,
                         u'薄雾':3,
                         u'阴天':3,
                         u'周边零星小雨': 2,
                         u'细雨': 2,
                         u'小雨': 2,
                         u'小雪': 2,
                         u'小雨夹雪':2,
                         u'零星细雨': 2,
                         u'零星小雨': 2,
                         u'小阵雨':2,
                         u'中雨': 4,
                         u'中雪': 4,
                         u'中到大阵雨': 4, 
                         u'周边雷暴': 4, 
                         u'零星雷雨': 4,
                         u'有时中雨': 4,
                         u'零星中雪': 4,
                         u'大雨': 5,
                         u'大雪': 5,
                         u'暴阵雨': 5,
                         u'中到大雷雨':5}, inplace=True)
    def handle_temp(x):
        if x < -5: return 1
        elif x < 5: return 2
        elif x < 15: return 3
        elif x < 25: return 4
        elif x< 35: return 5
        else: return 6
#    df1['body_temp'] = df1.body_temp.apply(lambda x: int(x[:-1]))
#    df1['temp'] = df1.temp.apply(lambda x: int(x[:-1]))
    df1['body_temp'] = df1['body_temp'].apply(handle_temp).astype(int)
    df1['temp'] = df1['temp'].apply(handle_temp).astype(int)
#    df1['wind'] = df1.wind.apply(lambda x: int(x[:-1]) if x != '-' else 0)
#    df1['shidu'] = df1.shidu.apply(lambda x: int(x[:-1]))
#    df1['rain'] = df1.rain.apply(lambda x: float(x[:-2]) if x != '-' else 0)
    
    def oneHot(df, col):
        from sklearn.preprocessing import OneHotEncoder
        enc = OneHotEncoder()
        ser = df1[col]
        enc.fit([[i] for i in ser])
        arr = enc.transform([[i] for i in ser]).toarray()
        concat_df = pd.DataFrame(arr, columns=[col+'_'+str(i) for i in range(1,len(arr[1])+1)])
        df = pd.concat([df1, concat_df],axis=1)
        del df[col]
        return df
    
    df1 = oneHot(df1, 'weather')
    df1 = oneHot(df1, 'body_temp')
    df1 = oneHot(df1, 'temp')
    return df1

def rmse(y_test, pred):
    return np.sqrt(np.mean(np.square(y_test.values - pred)))
def sq(y_test, pred):
    return [sum(np.square(y_test.values - pred)),len(pred)]

def train_each_loc(locid):
    # 取一个地点的
    each = df[df.loc_id == locid]
    X_train = each[each.datetime < datetime.datetime(2017,10,1,0,0,0)].iloc[:,5:]
    y_train = each[each.datetime < datetime.datetime(2017,10,1,0,0,0)].iloc[:,1]
    X_test = each[each.datetime >= datetime.datetime(2017,11,1,0,0,0)].iloc[:,5:]
    y_test = each[each.datetime >= datetime.datetime(2017,11,1,0,0,0)].iloc[:,1]
#    X = each.dropna().iloc[:,3:]
#    y = each.dropna().iloc[:,2]

#    X_train,X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
#    gbdt = xgb.XGBRegressor(
#            learning_rate=0.2,
#            n_estimators=500,
#            max_depth=5,
#            min_child_weight=1,
#            gamma=0.8
#            )
    gbdt=GradientBoostingRegressor(
      loss='huber'
    , learning_rate=0.2
    , n_estimators=500
    , subsample=1
    , min_samples_split=2
    , min_samples_leaf=1
    , max_depth=3
    , init=None
    , random_state=None
    , max_features=None
    , alpha=0.9
    , verbose=1
    , max_leaf_nodes=None
    , warm_start=False
    )
    gbdt.fit(X_train,y_train)
    pred=gbdt.predict(X_test)
    print(rmse(y_test, pred))
    return [gbdt, rmse(y_test, pred)]

w = load_weather()
df = pd.DataFrame()
for i in [10,11]:
    _df = loc_id_cnt(i)
    df = df.append(_df)
df = handle(df)
print('handle success')
df = handle_features(df, w)
df['datetime'] = df.datetime.apply(pd.to_datetime)
fl = ['loc_id', 'phone_id', 'datetime', 'month', 'day', 'hour', 'weekday',
       'weekend', 'isHoliday', 'shidu', 'wind', 'rain', 'weather_1',
       'weather_2', 'weather_3', 'weather_4', 'weather_5']
df = df.loc[:, fl]
#df = df[df.datetime >= datetime.datetime(2017,10,8,0,0,0)]
model_list = []
score = []
for locid in range(1, 34):
    print(locid)
    model = train_each_loc(locid)
    model_list.append(model[0])
    score.append(model[1])
print(score)
for i in score:
    if i<100:
        print(score.index(i))
#nov = pd.DataFrame()
#time_stamp_list = []
#stamp = datetime.datetime(2017,1,1,0,0,0)
#time_delta = datetime.timedelta(hours=1)
#while stamp < datetime.datetime(2018,1,1,0,0,0):
#    time_stamp_list.append(stamp)
#    stamp += time_delta
#nov['datetime'] = pd.Series(time_stamp_list)
#nov['time_stamp'] = pd.Series(str(i)[:-6] for i in time_stamp_list)
#nov = handle(nov)
#nov = handle_features(nov, w)
#nov = nov.loc[:, fl]
#nov = nov[nov.datetime >= datetime.datetime(2017,12,1,0,0,0)]
#novfl = nov.iloc[:,1:].columns
#for col in (set(fl) - set(novfl)):
#    nov[col] = 0
#
#time_stamp_list = []
#stamp = datetime.datetime(2017,12,1,0,0,0)
#while stamp < datetime.datetime(2018,1,1,0,0,0):
#    time_stamp_list.append(stamp)
#    stamp += time_delta
#res = pd.DataFrame()
#for loc_id, model in enumerate(model_list):
#    model.predict(nov.iloc[:,5:])
#    _df = pd.DataFrame()
#    _df['loc_id'] = [loc_id+1 for _ in range(len(nov))]
#    _df['time_stamp'] = pd.Series(str(i)[:-6] for i in time_stamp_list)
#    _df['num_of_people'] = model.predict(nov.iloc[:,5:])
#    res = res.append(_df)
##
##
#resNoZero = pd.DataFrame()
#for locid in range(1, 34):
#    tmp = res[res.loc_id==locid]
#    minNum = min(tmp.num_of_people)
#    tmp['num_of_people'] = tmp['num_of_people'] - minNum if minNum < 0 else tmp['num_of_people']
#    resNoZero = resNoZero.append(tmp)
#
#
#resNoZero = resNoZero.sort_values(['time_stamp','loc_id'])
#resNoZero['num_of_people'] = resNoZero['num_of_people'].apply(lambda x:round(x))
#resNoZero.to_csv('gbdt_res_teding3.csv', index=False)
