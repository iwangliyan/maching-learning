# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime


if __name__ == '__main__':
    filename = 'data/train3.csv'
    all_place_list = list(range(1, 34))
    year = 2017
    date_start = 20171017
    is_save = True
    
	
    def is_weekend(x):
        x = datetime.strptime(str(x), '%Y%m%d')
        if x.weekday() + 1 in (6, 7):
            return True
        else:
            return False
    
	
    data = pd.read_csv(filename, dtype=object, header=None)
    data[0] = data[0].apply(pd.to_numeric)
    data[2] = data[2].apply(pd.to_numeric)
    n_data = data.shape[0]
    
	
    def week_res(data, place_1, weekend_res, weekday_res):
        data1 = data[data[0]==place_1].reindex(columns=[1, 2])
        n_data1 = data1.shape[0]
        data1_1 = np.zeros([n_data1, 4], dtype=object)
        data1_1[:, 0:2] = data1
        for i in range(n_data1):
            data1_1[i, 2] = int(str(year) + data1_1[i, 0][:2] + data1_1[i, 0][2: 4])
            data1_1[i, 3] = int(data1_1[i, 0][4: 6])
        data1_2 = pd.DataFrame(data1_1[:, 1: 4], dtype='int').reindex(columns=[2, 1, 0])
        date1_list = data1_2[1].unique().astype('int')
        n_date1 = date1_list.shape[0]
        ss = list(date1_list)
        ss.insert(0, 'key')
        data1_3 = np.array(data1_2)
        data1_4 = pd.DataFrame(np.zeros((24, n_date1), dtype='int'), columns=date1_list, index=range(24))
        data1_4 = data1_4 - 1
        for i in range(n_data1):
            hour = data1_3[i, 0]
            date = data1_3[i, 1]
            data1_4.loc[hour, date] = data1_3[i, 2]
        new_date1_list = []
        for i in date1_list:
            if i > date_start:
                new_date1_list.append(i)
        data1_4 = data1_4.reindex(columns=new_date1_list)
		
        date1_weekend = list(map(lambda x: x if is_weekend(x) else None, new_date1_list))
        date_weekend = []
        for i in date1_weekend:
            if i:
                date_weekend.append(i)
        data_weekend = data1_4.reindex(columns=date_weekend)
        data_weekend = data_weekend[data_weekend>=0]
        date1_weekday = list(map(lambda x: x if not is_weekend(x) else None, new_date1_list))
        date_weekday = []
        for i in date1_weekday:
            if i:
                date_weekday.append(i)
        data_weekday = data1_4.reindex(columns=date_weekday)
        data_weekday = data_weekday[data_weekday>=0]
		
        data_weekend_T = data_weekend.T
        data_weekend_T[data_weekend_T == data_weekend_T.max()] = np.nan
        data_weekend_T[data_weekend_T == data_weekend_T.min()] = np.nan
        data_weekend_mean = data_weekend_T.mean(axis=0)
        data_weekday_T = data_weekday.T
        data_weekday_T[data_weekday_T == data_weekday_T.max()] = np.nan
        data_weekday_T[data_weekday_T == data_weekday_T.max()] = np.nan
        data_weekday_T[data_weekday_T == data_weekday_T.min()] = np.nan
        data_weekday_T[data_weekday_T == data_weekday_T.min()] = np.nan
        data_weekday_mean = data_weekday_T.mean(axis=0)
        weekend_res.append(data_weekend_mean)
        weekday_res.append(data_weekday_mean)
        		
    weekend_res = []
    weekday_res = []
    for place in all_place_list:
        week_res(data, place, weekend_res, weekday_res)
        
		
    res = pd.DataFrame(np.zeros((24552, 3)), dtype=object)
    line = 0
    for i in range(1, 34):
        for j in pd.date_range(start='2017-12-01', end='2017-12-31'):
            for k in range(24):
                res.iloc[line, 0] = i
                res.iloc[line, 1] = datetime.strftime(j, format='%Y-%m-%d') + ' ' + str('0'+ str(k))[-2:]
                if j.weekday() in [5, 6]:
                    res.iloc[line, 2] = weekend_res[i-1][k]
                else:
                    res.iloc[line, 2] = weekday_res[i-1][k]
                line += 1
    res.to_csv('result/result_'+ str(datetime.now().date()) +'.csv', index=False, header=False
	
    

