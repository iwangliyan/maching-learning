import pandas as pd
import numpy as np
path = '../data/'
res_10 = pd.read_csv(path+'10.csv')
res_11 = pd.read_csv(path+'11.csv')
res_10 = res_10['phone_id'].groupby([res_10['time_stamp'], res_10['loc_id']]).count().reset_index()
res_11 = res_11['phone_id'].groupby([res_11['time_stamp'], res_11['loc_id']]).count().reset_index()
res10 = pd.DataFrame(columns=['loc_id','time_stamp'])
from tqdm import tqdm_notebook
n = 0
for j in tqdm_notebook(range(1, 32)):
    if j<10:
        j = '0'+str(j)
    else:
        j = str(j)
    for k in range(0, 24):
        if k<10:
            s = '0'+str(k)
        else:
            s = str(k)
        for i in range(1, 34):            
            res10.loc[n, 'loc_id'] = i
            res10.loc[n, 'time_stamp'] = '2017-10-'+j+' '+s
            n += 1
res10 = pd.merge(res10, res_10, on=['time_stamp', 'loc_id'], how='left')
res10['day'] = res10['time_stamp'].map(lambda x:x.split(' ')[0])
res10['day'] = res10['day'].map(lambda x:x.split('-')[2])
res10['hour'] = res10['time_stamp'].map(lambda x:x.split(' ')[1])
res10['weekday'] = res10['day'].map(lambda x:(int(x)-1)%7)
res11 = pd.DataFrame(columns=['loc_id','time_stamp'])
from tqdm import tqdm_notebook
n = 0
for j in tqdm_notebook(range(1, 31)):
    if j<10:
        j = '0'+str(j)
    else:
        j = str(j)
    for k in range(0, 24):
        if k<10:
            s = '0'+str(k)
        else:
            s = str(k)
        for i in range(1, 34):            
            res11.loc[n, 'loc_id'] = i
            res11.loc[n, 'time_stamp'] = '2017-11-'+j+' '+s
            n += 1
res11 = pd.merge(res11, res_11, on=['time_stamp', 'loc_id'], how='left')
res11['day'] = res11['time_stamp'].map(lambda x:x.split(' ')[0])
res11['day'] = res11['day'].map(lambda x:x.split('-')[2])
res11['hour'] = res11['time_stamp'].map(lambda x:x.split(' ')[1])
res11['weekday'] = res11['day'].map(lambda x:(int(x)+2)%7)
for i, r in res11[(res11['phone_id'].isnull()==True)].iterrows():
    res11.loc[i, 'phone_id'] = res11[(res11['phone_id'].isnull()==False)&(res11['hour']==r['hour'])&(res11['loc_id']==r['loc_id'])&(res11['weekday']==r['weekday'])]['phone_id'].mean()
res = pd.concat([res10, res11], ignore_index=True)
for i, r in res[(res['phone_id'].isnull()==True)].iterrows():
    res.loc[i, 'phone_id'] = res[(res['phone_id'].isnull()==False)&(res['hour']==r['hour'])&(res['loc_id']==r['loc_id'])&(res['weekday']==r['weekday'])]['phone_id'].mean()
res = res.iloc[6336:]
res12 = pd.DataFrame(columns=['loc_id','time_stamp','num_of_people'])
from tqdm import tqdm_notebook
n = 0

for j in tqdm_notebook(range(1, 32)):
    if j<10:
        d = '0'+str(j)
    else:
        d = str(j)
    for k in range(0, 24):
        if k<10:
            h = '0'+str(k)
        else:
            h = str(k)
        for i in range(1, 34):            
            res12.loc[n, 'loc_id'] = str(i)
            res12.loc[n, 'time_stamp'] = '2017-12-'+d+' '+h
            w = (j+4)%7
            res12.loc[n, 'num_of_people'] = res[(res['weekday']==w)&(res['hour']==h)&(res['loc_id']==i)]['phone_id'].values.sum()/len(res[(res['weekday']==w)&(res['hour']==h)&(res['loc_id']==i)])
            n += 1
res12.to_csv('../result/sub_12_mean.csv', index=False)
