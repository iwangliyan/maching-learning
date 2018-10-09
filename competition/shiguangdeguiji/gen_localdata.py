import pandas as pd
from tqdm import tqdm_notebook
for i in tqdm_notebook(range(1,12)):
    data=pd.read_csv('../data/'+str(i)+'.csv')
    data['time_stamp']=pd.to_datetime(data['time_stamp'])
    data['day']=data['time_stamp'].dt.day
    data['hour']=data['time_stamp'].dt.hour
    data['month']=data['time_stamp'].dt.month
    data_local=data.groupby(['month','day','hour','loc_id']).agg({'phone_id':'count'}).reset_index().rename(columns={'phone_id':'num'})
    data_local['year']=2017
    data_local['time_stamp']=pd.to_datetime(data_local[['year','month','day','hour']])
    data_local.to_csv('../data/'+str(i)+'_local'+'.csv',index=False)
    del data,data_local

data=pd.read_csv('../result/sub_12_mean.csv')
data['time_stamp']=pd.to_datetime(data['time_stamp'])
data['day']=data['time_stamp'].dt.day
data['hour']=data['time_stamp'].dt.hour
data['month']=data['time_stamp'].dt.month
data['year']=2017
data.rename(columns={'num_of_people':'num'},inplace=True)
data.to_csv('../data/12_local'+'.csv',index=False)
