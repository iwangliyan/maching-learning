# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from error_method import rmse


if __name__ == '__main__':
    filename = 'data/train3.csv'
    place_list = [6, 7, 8]
    all_place_list = list(range(1, 34)) 
    year = 2017
    date_start = 20171101
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
    place_1, place_2, place_3 = place_list[0], place_list[1], place_list[2]
    data_1 = pd.Series(data[data[0]==place_1][2])
    data_1.index = data[data[0]==place_1][1]
    data_2 = pd.Series(data[data[0]==place_2][2])
    data_2.index = data[data[0]==place_2][1]
    data_3 = pd.Series(data[data[0]==place_3][2])
    data_3.index = data[data[0]==place_3][1]
    
	
    fig = plt.figure(figsize=(12, 9))
    fig.subplots_adjust(wspace=None, hspace=None)
    ax = fig.add_subplot(3, 1, 1)
    ax.set_title('不同地点的人次时序图', fontproperties='SimHei', fontsize=16)
    plt.subplot(311)
    data_1.plot(label='Place'+str(place_1), style='r-', use_index=False)
    plt.ylabel('人次/位', fontproperties='SimHei', fontsize=12)
    plt.legend(loc='upper left')
    plt.subplot(312)
    data_2.plot(label='Place'+str(place_2), style='g-', use_index=False)
    plt.ylabel('人次/位', fontproperties='SimHei', fontsize=12)
    plt.legend(loc='upper left')
    plt.subplot(313)
    data_3.plot(label='Place'+str(place_3), style='b-', use_index=False)
    plt.xlabel('时间/h', fontproperties='SimHei', fontsize=12)
    plt.ylabel('人次/位', fontproperties='SimHei', fontsize=12)
    plt.legend(loc='upper left')
    if is_save:
        ts_path = 'fig/时序图{}-{}-{}'.format(str(place_1), str(place_2), str(place_3))
        if os.path.exists(ts_path):
            raise OSError('时序图文件已存在！')
        plt.savefig(ts_path)
    
	
    def fig2(data, place_1, weekend_res, weekday_res):
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
        data_weekend_mean = data_weekend.mean(axis=1)
        data_weekday_mean = data_weekday.mean(axis=1)
        weekend_res.append(data_weekend_mean)
        weekday_res.append(data_weekday_mean)
		
        res0 = 0
        for i in range(data_weekend.shape[1]):
            res0 += rmse(data_weekend.iloc[:, i], data_weekend_mean)
        res0 = res0 / data_weekend.shape[1]
        res1 = 0
        for i in range(data_weekday.shape[1]):
            res1 += rmse(data_weekday.iloc[:, i], data_weekday_mean)
        res1 = res1 / data_weekday.shape[1]
		
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(211)
        ax.set_title('周末一天内各小时人流量情况, Place:{},RMSE:{}'.format(str(place_1), str(res0)), fontproperties='SimHei', fontsize=14)
        ax.set_ylabel('人数', fontproperties='SimHei')
        data_weekend.plot(ax=ax, label='weekends', use_index=False, grid=True, legend=False, style='c--', xticks=range(24))
        plt.plot(range(24), data_weekend_mean, 'r-', linewidth=5)
        ax = fig.add_subplot(212)
        ax.set_title('非周末一天内各小时人流量情况, Place:{},RMSE:{}'.format(str(place_1), str(res1)), fontproperties='SimHei', fontsize=14)
        ax.set_ylabel('人数', fontproperties='SimHei')
        ax.set_xlabel('时间/h', fontproperties='SimHei')
        data_weekday.plot(ax=ax, label='weekdays', use_index=False, grid=True, legend=False, style='c--', xticks=range(24))
        plt.plot(range(24), data_weekday_mean, 'r-', linewidth=5)
        plt.show()
        
	
    weekend_res = []
    weekday_res = []
    for place in all_place_list:
        fig2(data, place, weekend_res, weekday_res)
        
		
    res = pd.DataFrame(np.zeros((48312, 3)), dtype=object)
    line = 0
    for i in range(1, 34):
        for j in pd.date_range(start='2017-11-01', end='2017-12-31'):
            for k in range(24):
                res.iloc[line, 0] = i
                res.iloc[line, 1] = datetime.strftime(j, format='%Y-%m-%d') + ' ' + str('0'+ str(k))[-2:]
                if j.weekday() in [5, 6]:
                    res.iloc[line, 2] = weekend_res[i-1][k]
                else:
                    res.iloc[line, 2] = weekday_res[i-1][k]
                line += 1
    res.to_csv('result/result'+ str(datetime.now().date()) +'.csv', index=False, header=False)


    
        
    
    
    
    

        
    
    
    
    
    
    

