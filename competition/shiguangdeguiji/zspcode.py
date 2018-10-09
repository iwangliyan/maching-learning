import pandas as pd
from tqdm import tqdm_notebook
import numpy as np
import lightgbm as lgb

#month1=pd.read_csv('../data/1_local.csv')
month3=pd.read_csv('../data/3_local.csv')
month4=pd.read_csv('../data/4_local.csv')
month5=pd.read_csv('../data/5_local.csv')
month6=pd.read_csv('../data/6_local.csv')
# month7=pd.read_csv('../data/7_local.csv')
# month8=pd.read_csv('../data/8_local.csv')
month9=pd.read_csv('../data/9_local.csv')
month10=pd.read_csv('../data/10_local.csv')
month11=pd.read_csv('../data/11_local.csv')
month12=pd.read_csv('../data/12_local.csv')
month12=month12[['month', 'day', 'hour', 'loc_id', 'num', 'year', 'time_stamp']]
data=pd.concat([month3,month4,month5,month6,month9,month10,month11,month12])

data['time_stamp']=pd.to_datetime(data['time_stamp'])
data['weekday']=data['time_stamp'].dt.dayofweek
data['quarter']=data['time_stamp'].dt.quarter
data['weekofyear']=data['time_stamp'].dt.weekofyear

#月
#3，9月 开学月1  #1,6月 考试月2   #7,8月 暑假月3   #2月 寒假月4   #其他 0
term_dict={}
term_dict[3]=term_dict[9]=1
term_dict[1]=term_dict[6]=2
term_dict[7]=term_dict[8]=3
term_dict[2]=4
def term_property(x):
    if x in term_dict:
        return term_dict[x]
    else:
        return 0
data['term_property']=data['month'].apply(term_property)

def term_judge(x):
    if x>=2 and x<=6:
        return 1
    elif (x>=9 and x<=12) or x==1:
        return 2
    else:
        return 3
data['term']=data['month'].apply(term_judge)

#周
def weekofterm(data):
    if data['term']==1:
        return data['weekofyear']-9+1
    elif data['term']==2:
        if data['month']==1:
            if data['weekofyear']==53:
                return 53-37+1
            else:
                return data['weekofyear']+17
        else:
            return data['weekofyear']-37+1 if data['weekofyear']-37+1>0 else -1
    else:
        return -1
data['weekofterm']=data.apply(weekofterm,axis=1)
data['oddevenweek']=data['weekofterm'].apply(lambda x:x%2 if x>0 else x)

#早熄灯
def close_light_day(x):
    if x==4 or x==5:
        return 1
    else:
        return 0
data['close_light_day']=data['weekday'].apply(close_light_day)
#早熄灯
def close_light_hour(x):
    if x['weekday']==4 or x['weekday']==5:#12点熄灯
        if x['hour']>=0 and x['hour']<6 :
            return 1
        else:
            return 0
    else:
        if (x['hour']>=0 and x['hour']<6) or x['hour']==23 :
            return 1
        else:
            return 0
data['close_light_time']=data.apply(close_light_hour,axis=1)

def is_weekend(x):
    if x==5 or x==6:
        return 1
    else:
        return 0
data['is_weekend']=data['weekday'].apply(is_weekend)

def is_holiday(x):
    if x['month']==4 and x['day']==5:
        return 1
    elif x['month']==5 and x['day']==1:
        return 1
    elif x['month']==6 and x['day']==18:
        return 1
    elif x['month']==10 and x['day']<=8:
        return 1
    elif x['month']==9 and x['day']==31:
        return 1
    elif x['month']==1 and x['day']==1:
        return 1
    elif x['month']==12 and x['day']==25:
        return 1
    else:
        return 0
data['is_holiday']=data.apply(is_holiday,axis=1)

#小时
eat_dict={}
eat_dict[7]=eat_dict[8]=2
eat_dict[11]=eat_dict[12]=4
eat_dict[5]=5;eat_dict[6]=6
def is_eating(x):
    if x in eat_dict:
        return eat_dict[x]
    else:
        return 0
class_dict={}
for i in range(8,12+1):
    class_dict[i]=1
for i in range(13,17+1):
    class_dict[i]=2 
for i in range(18,21+1):
    class_dict[i]=3 
    
def is_class(x):
    if x in class_dict:
        return class_dict[x]
    else:
        return 0

def is_free(x):
    if x>=18 and x<=22:
        return 1
    else:
        return 0

def is_sleep(x):
    if (x>=0 and x<7) or x==23:
        return 1
    else:
        return 0

data['is_eating']=data['hour'].apply(is_eating)
data['is_class']=data['hour'].apply(is_class)
data['is_free']=data['hour'].apply(is_free)
data['is_sleep']=data['hour'].apply(is_sleep)

class_build=[22,15,16,24,14,27,33]
sleep_build=[5,1,9,7,25,21,4,6,3,32,17,28,31,18,30,23,11,19,2,13,26]
eat_build=[12,8,29,10]
study_build=[20,22,15,27,33]
build_door=[1,7,4,3,17,31,30,11,2,26]
data['is_class_build']=data['loc_id'].apply(lambda x : 1 if x in class_build else 0)
data['is_sleep_build']=data['loc_id'].apply(lambda x : 1 if x in sleep_build else 0)
data['is_eat_build']=data['loc_id'].apply(lambda x : 1 if x in eat_build else 0)
data['is_study_build']=data['loc_id'].apply(lambda x : 1 if x in study_build else 0)
data['is_build_door']=data['loc_id'].apply(lambda x : 1 if x in build_door else 0)

del data['time_stamp']

train=data[(data.month==9)|(data.month==10)]
val=data[data.month==11]
test=data[data.month==12]

month3_weekend_avr=data[(data.is_weekend==1)&(data.month==3)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month3_avr'})
month3_work_avr=data[(data.is_weekend==0)&(data.month==3)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month3_avr'})

month4_weekend_avr=data[(data.is_weekend==1)&(data.month==4)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month4_avr'})
month4_work_avr=data[(data.is_weekend==0)&(data.month==4)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month4_avr'})

month5_weekend_avr=data[(data.is_weekend==1)&(data.month==5)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month5_avr'})
month5_work_avr=data[(data.is_weekend==0)&(data.month==5)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month5_avr'})

month6_weekend_avr=data[(data.is_weekend==1)&(data.month==6)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month6_avr'})
month6_work_avr=data[(data.is_weekend==0)&(data.month==6)].groupby(['loc_id','hour'])['num'].mean().reset_index().rename(columns={'num':'month6_avr'})

month3_weekend_avr['is_weekend']=1
month3_work_avr['is_weekend']=0
month4_weekend_avr['is_weekend']=1
month4_work_avr['is_weekend']=0

month5_weekend_avr['is_weekend']=1
month5_work_avr['is_weekend']=0
month6_weekend_avr['is_weekend']=1
month6_work_avr['is_weekend']=0

month3_avr=pd.concat([month3_weekend_avr,month3_work_avr])
month4_avr=pd.concat([month4_weekend_avr,month4_work_avr])
month5_avr=pd.concat([month5_weekend_avr,month5_work_avr])
month6_avr=pd.concat([month6_weekend_avr,month6_work_avr])

train=pd.merge(train,month3_avr,on=['is_weekend','loc_id','hour'],how='left')
train=pd.merge(train,month4_avr,on=['is_weekend','loc_id','hour'],how='left')
val=pd.merge(val,month3_avr,on=['is_weekend','loc_id','hour'],how='left')
val=pd.merge(val,month4_avr,on=['is_weekend','loc_id','hour'],how='left')

train=pd.merge(train,month5_avr,on=['is_weekend','loc_id','hour'],how='left')
train=pd.merge(train,month6_avr,on=['is_weekend','loc_id','hour'],how='left')
val=pd.merge(val,month5_avr,on=['is_weekend','loc_id','hour'],how='left')
val=pd.merge(val,month6_avr,on=['is_weekend','loc_id','hour'],how='left')

test=pd.merge(test,month3_avr,on=['is_weekend','loc_id','hour'],how='left')
test=pd.merge(test,month4_avr,on=['is_weekend','loc_id','hour'],how='left')
test=pd.merge(test,month5_avr,on=['is_weekend','loc_id','hour'],how='left')
test=pd.merge(test,month6_avr,on=['is_weekend','loc_id','hour'],how='left')

train['isval']=0
val['isval']=1
test['isval']=2
fsdata=pd.concat([train,val,test])

def divide(x,y):
    return (x + 0.001)/(y + 0.001)

fsdata['(is_eat_build/is_eating)']=divide(fsdata['is_eat_build'],fsdata['is_eating'])
fsdata['(is_eat_build-weekofyear)']=fsdata['is_eat_build']-fsdata['weekofyear']
fsdata['(close_light_time+close_light_day)']=fsdata['close_light_time']+fsdata['close_light_day']
fsdata['(close_light_time/month4_avr)']=divide(fsdata['close_light_time'],fsdata['month4_avr'])
fsdata['(close_light_time*is_class_build)']=fsdata['close_light_time']*fsdata['is_class_build']
fsdata['(close_light_time/is_class_build)']=divide(fsdata['close_light_time'],fsdata['is_class_build'])
fsdata['(month*month3_avr)']=fsdata['month']*fsdata['month3_avr']
fsdata['(month+month4_avr)']=fsdata['month']+fsdata['month4_avr']
fsdata['(month-month4_avr)']=fsdata['month']-fsdata['month4_avr']
fsdata['(month-is_eating)']=fsdata['month']-fsdata['is_eating']
fsdata['(month6_avr*month4_avr)']=fsdata['month6_avr']*fsdata['month4_avr']
fsdata['(month6_avr*loc_id)']=fsdata['month6_avr']*fsdata['loc_id']
fsdata['(term_property*month3_avr)']=fsdata['term_property']*fsdata['month3_avr']
fsdata['(term_property-loc_id)']=fsdata['term_property']-fsdata['loc_id']

bstfeature=['(is_eat_build-weekofyear)', 'year', '(term_property-loc_id)', 'hour', '(close_light_time*is_class_build)', 
 '(month-is_eating)', 'is_class_build', 'close_light_time', 'month', 'weekofterm', 'month6_avr', 'term_property', 
 'month5_avr', 'term', 'loc_id', 'weekofyear', 'oddevenweek', 'is_eating', 'month4_avr', 'month3_avr', 'quarter',
 'close_light_day', '(month*month3_avr)', '(close_light_time/month4_avr)', 'is_free', 
 'is_sleep', '(month6_avr*loc_id)', '(close_light_time+close_light_day)', '(month+month4_avr)', 'is_sleep_build','num']

fstrain=fsdata[fsdata.isval==0]
fsval=fsdata[fsdata.isval==1]
fstest=fsdata[fsdata.isval==2]

fstrain=fstrain[bstfeature]
fsval=fsval[bstfeature]
fstest=fstest[bstfeature]

online=True
if online:
    fstrain=pd.concat([fstrain,fsval])
fstrain_y=fstrain.pop('num')
fstrain_x=fstrain
fsval_y=fsval.pop('num')
fsval_x=fsval
fstest=fstest.drop('num',axis=1)

clf = lgb.LGBMRegressor(
        boosting_type='gbdt', num_leaves=31,n_estimators=1000,
        max_depth=-1, learning_rate=0.07, random_state=9595,n_jobs=-1
)

clf.fit(fstrain_x, fstrain_y)

test_y=clf.predict(fstest)

res12=pd.read_csv('../result/sub_12_mean.csv')
res12['num_of_people']=res12['num_of_people']*0.96*0.5+test_y*0.5*0.98
res12.to_csv('../result/finalres.csv',index=False)


