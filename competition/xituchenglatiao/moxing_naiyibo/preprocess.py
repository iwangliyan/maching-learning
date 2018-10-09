import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
%matplotlib inline


def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 


path_to_bj_aq = "./data/months1_10/"

bj_csv_list  = os.listdir(path_to_bj_aq)

for csv in bj_csv_list :
    if csv != '.DS_Store' and not csv.startswith("._"):
        path_to_file = path_to_bj_aq + csv
        
        data = pd.read_csv(path_to_file)
        i = csv.split('.')[0]

        data['time_stamp'] = pd.to_datetime(data['time_stamp'])
        data = data.groupby(['time_stamp','loc_id'],as_index = False).count()
        data['date'] = data['time_stamp'].apply(lambda x:str(x)[:10])
        data['hour'] = data['time_stamp'].apply(lambda x:int(str(x)[11:13]))
        data['week'] = data['time_stamp'].apply(lambda x:x.weekday())

        for j in range(1,34):
            data_part = data[data['loc_id'] == j]
            mkdir('./data/station_%s' % (j))
            data_part.to_csv('data/station_%s/month_%s.csv' % (j,i),index = False)
            
            
            
#数据预处理


holiday = pd.read_csv('data/holiday.csv')          
datas = []
for i in range(1,34):
    path_to_bj_aq = "./data/station_"+str(i)+"/"

    bj_csv_list  = os.listdir(path_to_bj_aq)
    
    for csv in bj_csv_list :
        if csv != '.DS_Store' and not csv.startswith("._") :
            
            path_to_file = path_to_bj_aq + csv
            data = pd.read_csv(path_to_file)  
            if data.empty == False:
                datas.append(data)

data_all = pd.concat(datas, ignore_index=True)

data_all = pd.merge(data_all, holiday, how='inner', on=['date'])
data_all = data_all[data_all['holiday']!=2]

data_all.rename(index=str, columns={"phone_id": "phone_num"},inplace = True)

data_all['data_mean'] = 0
data_all['data_max'] = 0
data_all['data_min']= 0
data_all['data_median'] = 0
# data_all['data_mean_week_hour'] = 0
# data_all['data_max_week_hour'] = 0
# data_all['data_min_week_hour']= 0
# data_all['data_median_week_hour'] = 0


for i in range(1,34):    
    data_mean = data_all['phone_num'][data_all['loc_id'] == i].mean()
    data_max = data_all['phone_num'][data_all['loc_id'] == i].max()
    data_min = data_all['phone_num'][data_all['loc_id'] == i].min()
    data_median = data_all['phone_num'][data_all['loc_id'] == i].median()
    
    data_all['data_mean'][data_all['loc_id'] == i] = data_mean
    data_all['data_max'][data_all['loc_id'] == i] = data_max
    data_all['data_min'][data_all['loc_id'] == i] = data_min
    data_all['data_median'][data_all['loc_id'] == i] = data_median



data_all.to_csv('data/data_all.csv',index = False)         
            
#处理meo            
data_meo = pd.read_csv('data/beijing_17_18_meo.csv')

data_meo['wind_speed'][data_meo['wind_direction'] == 999017] = 0.1
data_meo['wind_u'] = data_meo['wind_speed']*np.cos(data_meo['wind_direction'])
data_meo['wind_v'] = data_meo['wind_speed']*np.sin(data_meo['wind_direction'])

data_meo['weather'].replace(['Fog','Haze','Rain','Sunny/clear'],[1,2,3,4],inplace=True)

data_meo['SSD'] = (1.818*data_meo['temperature']+18.18)*(0.88+0.002*data_meo['humidity'])+(data_meo['temperature']-32)/(45-data_meo['temperature'])-3.2*data_meo['wind_speed']+18.2
del data_meo['wind_direction']         
data_meo.to_csv('data/data_meo.csv',index = False)      

#处理aq
data_aq = pd.read_csv('data/aq_beifen.csv')
data_aq['rate'].replace(['重度污染','严重污染','中度污染','轻度污染','良','优'],[1,2,3,4,5,6],inplace=True)
data_aq.to_csv('data/data_aq.csv',index = False)  

#合并数据
data_aq = pd.read_csv('data/data_aq.csv')
data_meo = pd.read_csv('data/data_meo.csv')
data_base = pd.read_csv('data/data_all.csv')
# print(data_base.isnull().sum())
# print(data_base.columns.size)
# print(data_base.iloc[:,0].size)
# print(data_meo.columns.size)
# print(data_meo.iloc[:,0].size)
data = pd.merge(data_base, data_meo, how='inner', on=['time_stamp'])
data = pd.merge(data, data_aq, how='inner', on=['date'])
# print(data.columns.size)
# print(data.iloc[:,0].size)



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
data.to_csv('chouchoukan.csv',index=False)