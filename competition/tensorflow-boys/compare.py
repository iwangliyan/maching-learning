# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime
from error_method import rmse


if __name__ == '__main__':
    path1 = 'data/train1.csv'
    path2 = 'data/train2.csv'
    date_start1 = 20161010
    date_start2 = 20171010 
    year1 = 2016
    year2 = 2017
    
    def is_weekend(x):
        x = datetime.strptime(str(x), '%Y%m%d')
        if x.weekday() + 1 in (6, 7):
            return True
        else:
            return False
            
    def mean_list(data, place, year, date_start, weekday_res):
        data1 = data[data[0]==place].reindex(columns=[1, 2])
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

        date1_weekday = list(map(lambda x: x if not is_weekend(x) else None, new_date1_list))
        date_weekday = []
        for i in date1_weekday:
            if i:
                date_weekday.append(i)
        data_weekday = data1_4.reindex(columns=date_weekday)
        data_weekday = data_weekday[data_weekday>=0]
        data_weekday_mean = data_weekday.mean(axis=1)
        weekday_res.append(data_weekday_mean)


    

    data1 = pd.read_csv(path1, dtype=object, header=None)
    data1[0] = data1[0].apply(pd.to_numeric)
    data1[2] = data1[2].apply(pd.to_numeric)
    data2 = pd.read_csv(path2, dtype=object, header=None)
    data2[0] = data2[0].apply(pd.to_numeric)
    data2[2] = data2[2].apply(pd.to_numeric)
    weekday_res1 = []
    weekday_res2 = []
    for i in range(1, 37):
        mean_list(data1, i, year1, date_start1, weekday_res1)
    for i in range(1, 34):
        mean_list(data2, i, year2, date_start2, weekday_res2)
    res = np.zeros((33, 36), dtype='float')

    for i in range(33):
        for j in range(36):
            res[i, j] = rmse(weekday_res2[i], weekday_res1[j])
    print('最佳配对结果：')
    print('上半年--下半年        两个位置间的RMSE')
    for i in range(33):
        print(str('0' + str(i+1))[-2:],'--', str('0' + str(np.argmin(res[i])+1))[-2:], '       {}'.format(np.min(res[i])))
        


    