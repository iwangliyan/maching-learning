
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
#根据地点、时间获得人数
def get_unique(df, grouping_col, target_col):
    
    used_cols = grouping_col.copy()
    used_cols.extend(['row_id'])
    used_cols.extend(target_col)
    all_df = df[used_cols]
    
    group_used_cols = grouping_col.copy()
    group_used_cols.extend(target_col)
    grouped = all_df[group_used_cols].groupby(grouping_col)
    
    the_count = pd.DataFrame(grouped[target_col].nunique()).reset_index()
    return the_count
#统计获得人数，并将处理得到的人数存储至csv文件中
def get_count_csv():
    months=['01','02','03','04','05','06','07','08','09','10','11']
    for month in months:
        print('正在生成'+month+'月数据...')
        train=pd.read_csv('../months1_10/'+month+'.csv')
        train['time_stamp'] = pd.to_datetime(train['time_stamp'])
        train['row_id']=train.index
        personnum=get_unique(train,['loc_id','time_stamp'],['phone_id'])
        personnum.to_csv('../handeled_data/'+month+'_count.csv',index=False)
#获得12月提交格式
def get_12_subcsv():
    print('正在生成12月格式...')
    date11=pd.date_range(start='2017-12-01 00',freq='H',end='2017-12-31 23')
    df_11=pd.DataFrame()
    for time in date11:
        for i in range(33):
            df_11=df_11.append({'loc_id':i+1,'time_stamp':time},ignore_index=True)
    df_11['loc_id']=df_11['loc_id'].astype(int)
    def totime(x):
        return str(str(x)[0:13])
    df_11['time_stamp']=df_11['time_stamp'].astype(str)
    df_11['time_stamp']=df_11['time_stamp'].apply(totime)
    df_11['num_of_people']=0
    df_11.to_csv('../handeled_data/sub_sample.csv',index=False)
get_count_csv()
get_12_subcsv()
print ('数据生成完成')

