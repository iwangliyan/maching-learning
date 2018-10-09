import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
%matplotlib inline


data = pd.DataFrame()

min_time = datetime.datetime.strptime('2017-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')
max_time = datetime.datetime.strptime('2017-11-30 23:00:00', '%Y-%m-%d %H:%M:%S')

delta_all = max_time - min_time
hours_should = delta_all.total_seconds()/3600 + 1
delta = datetime.timedelta(hours=1)
time = min_time

time_stamp = []
loc_id = []
while time <=  max_time :
    
    for i in range(1,34):
        time_stamp.append(time)
        loc_id.append(i)
    time += delta
data['time_stamp'] = time_stamp
data['loc_id'] = loc_id


data['time_stamp'] = pd.to_datetime(data['time_stamp'])
data['date'] = data['time_stamp'].apply(lambda x:str(x)[:10])
data['hour'] = data['time_stamp'].apply(lambda x:int(str(x)[11:13]))
data['week'] = data['time_stamp'].apply(lambda x:x.weekday())

holiday = pd.read_csv('data/holiday.csv')
data = pd.merge(data, holiday, how='inner', on=['date'])
data['holiday'][data['holiday'] == 2] = 1
data['data_mean'] = 0
data['data_max'] = 0
data['data_min']= 0
data['data_median'] = 0

# # data['data_mean_hour'] = 0
# # data['data_max_hour'] = 0
# # data['data_min_hour']= 0
# data['data_median_hour'] = 0

# # data['data_mean_week'] = 0
# # data['data_max_week'] = 0
# # data['data_min_week']= 0
# data['data_median_week'] = 0

# data['data_mean_week_hour'] = 0
# data['data_max_week_hour'] = 0
# data['data_min_week_hour']= 0
# data['data_median_week_hour'] = 0
datas = []
for i in range(1,34):
    path_to_bj_aq = "./data/station_"+str(i)+"/"

    bj_csv_list  = os.listdir(path_to_bj_aq)
    for csv in bj_csv_list :
        if csv != '.DS_Store' and not csv.startswith("._"):
            path_to_file = path_to_bj_aq + csv
            data_su = pd.read_csv(path_to_file)
            if data_su.empty == False:
                datas.append(data_su)

data_all = pd.concat(datas, ignore_index=True)
data_all.rename(index=str, columns={"phone_id": "phone_num"},inplace = True)
# print(data_all)
for i in range(1,34):    
    data_mean = data_all['phone_num'][data_all['loc_id'] == i].mean()
    data_max = data_all['phone_num'][data_all['loc_id'] == i].max()
    data_min = data_all['phone_num'][data_all['loc_id'] == i].min()
    data_median = data_all['phone_num'][data_all['loc_id'] == i].median()
    
    data['data_mean'][data['loc_id'] == i] = data_mean
    data['data_max'][data['loc_id'] == i] = data_max
    data['data_min'][data['loc_id'] == i] = data_min
    data['data_median'][data['loc_id'] == i] = data_median
        
# for i in range(1,34):
#     for h in range(24):   
#         for j in range(7):
#             data_mean = data_all['phone_num'][(data_all['loc_id'] == i)&(data_all['week'] == j)&(data_all['hour'] == h)].mean()
#             data_max = data_all['phone_num'][(data_all['loc_id'] == i)&(data_all['week'] == j)&(data_all['hour'] == h)].max()
#             data_min = data_all['phone_num'][(data_all['loc_id'] == i)&(data_all['week'] == j)&(data_all['hour'] == h)].min()
#             data_median = data_all['phone_num'][(data_all['loc_id'] == i)&(data_all['week'] == j)&(data_all['hour'] == h)].median()
#     #             data_var = data_all['phone_num'][(data_all['loc_id'] == i)&(data_all['week'] == j)&(data_all['hour'] == h)].var()
# #             print(data_mean)

#             data['data_mean_week_hour'][(data['loc_id'] == i)&(data['week'] == j)&(data['hour'] == h)] = data_mean
#             data['data_max_week_hour'][(data['loc_id'] == i)&(data['week'] == j)&(data['hour'] == h)] = data_max
#             data['data_min_week_hour'][(data['loc_id'] == i)&(data['week'] == j)&(data['hour'] == h)] = data_min
#             data['data_median_week_hour'][(data['loc_id'] == i)&(data['week'] == j)&(data['hour'] == h)] = data_median
#     #             data['data_var_week_hour'][(data['loc_id'] == i)&(data['week'] == j)&(data['hour'] == h)] = data_var
data['time_stamp'] = data['time_stamp'].astype('str')



# data['week_num_percent'] = data['week_num']/20
data_aq = pd.read_csv('data/data_aq.csv')
data_meo = pd.read_csv('data/data_meo.csv')
data_meo['time_stamp'] = data_meo['time_stamp'].astype('str')
data = pd.merge(data, data_meo, how='left', on=['time_stamp'])
data = pd.merge(data, data_aq, how='left', on=['date'])


data['loc_hour'] = data['loc_id']*100+data['hour']
data['loc_week'] = data['loc_id']*100+data['week']
data['loc_rate'] = data['loc_id']*100+data['rate']
data['loc_weather'] = data['loc_id']*100+data['weather']

# data_all['week_num_percent'] = data_all['week_num']/20
# data['loc_week_num'] = data['loc_id']*100+data['week_num']

data['hour_rate'] = data['hour']*100+data['rate']
data['hour_weather'] = data['hour']*100+data['weather']
data['hour_week'] = data['hour']*100+data['rate']

data['week_rate'] = data['week']*100+data['rate']
data['week_weather'] = data['week']*100+data['weather']

data['rate_weather'] = data['rate']*100+data['weather']
del data['date']

data.to_csv('test_X.csv',index = False)