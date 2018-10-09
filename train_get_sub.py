
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


month_dfs=list()
months=['01','02','03','04','05','06','07','08','09','10','11']
# 读取处理过的月份人数信息
for month in months:
     month_dfs.append(pd.read_csv('../handeled_data/'+month+'_count.csv'))
df_12=pd.read_csv('../handeled_data/sub_sample.csv')
# 提取月份特征
for month_df in month_dfs:
    month_df['time_stamp'] = pd.to_datetime(month_df['time_stamp'])
    month_df['week']=month_df['time_stamp'].dt.week
    month_df['dow']=month_df['time_stamp'].dt.dayofweek
    month_df['hour']=month_df['time_stamp'].dt.hour
month_df=pd.DataFrame()
# 将各月份信息组合
for month in month_dfs:
    month_df=pd.concat([month_df,month])
# 提取12月月份信息
df_12['time_stamp'] = pd.to_datetime(df_12['time_stamp'])
df_12['week']=df_12['time_stamp'].dt.week
df_12['dow']=df_12['time_stamp'].dt.dayofweek
df_12['hour']=df_12['time_stamp'].dt.hour
df_12

del df_12['num_of_people']
# 截取需要用到的月份
month_pre_df=month_df[month_df['time_stamp']>'2017-10-07 23:00:00']
month_pre_df
# 拼接验证集与训练集，方便处理
test_length=df_12.shape[0]
X_train=pd.concat([df_12,month_pre_df])

#提取是否是周末特征

def isweek(day):
    if day<5:
        return 1
    else:
        return 0
X_train['is_weekday']=X_train['dow'].apply(isweek)



del X_train['time_stamp']
del X_train['week']
# 对数据中地点类型加标签
loc_type=pd.read_csv('./loc_type.csv')
X_train=pd.merge(X_train,loc_type,on='loc_id',how='left')

# 对数据进行one-hot处理
onehoted=pd.get_dummies(X_train,columns=['loc_id','dow','hour','type'])
onehoted
del X_train
test=onehoted[:test_length]
train=onehoted[test_length:]
y=train['phone_id']
del train['phone_id']
del test['phone_id']
# 训练集、验证集分开
from sklearn.cross_validation import train_test_split
import xgboost as xgb
x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
print ('预处理完成，使用xgboost模型...')
# 使用xgboost进行训练、预测
import gc
params = {'eta': 0.2,
          'tree_method': "hist",
          'grow_policy': "lossguide",
          'max_leaves': 1400,  
          'max_depth': 10, 
          'subsample': 0.9, 
          'colsample_bytree': 0.5, 
          'colsample_bylevel':0.7,
          'min_child_weight':0,
          'alpha':12,
          'objective': 'count:poisson', 
          'scale_pos_weight':5,
          'eval_metric': 'rmse', 
          'nthread':8,
          'random_state': 99, 
          
          'silent': True}

dtrain = xgb.DMatrix(x1, y1)
dvalid = xgb.DMatrix(x2, y2)

gc.collect()
watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
model_xgb = xgb.train(params, dtrain, 500, watchlist, maximize=False, early_stopping_rounds = 50, verbose_eval=5)
dtest = xgb.DMatrix(test)
gc.collect()
# 储存预测结果
sub_df=pd.read_csv('../handeled_data/sub_sample.csv')
sub_df['num_of_people1'] = model_xgb.predict(dtest, ntree_limit=model_xgb.best_ntree_limit)
sub_df.sort_values(by='num_of_people1')


# 使用xlightgbm进行训练、预测
print ('使用lightgbm模型...')

import lightgbm as lgb
params = {
        'objective'        : 'regression',
        'metric'           : 'rmse',
        'learning_rate'    : 0.2,
        'boosting_type'    : 'gbdt',
        'min_data_in_leaf':50,
        'num_leaves'       : 30,
        'max_depth'        : -1,
        'feature_fraction' : 0.6,
        'subsample'        : 0.9,
    
        'bagging_freq'     : 5,
        'reg_lambda'       : 1,
        'num_threads'      : 18,
        'min_child_samples': 5,
        'min_child_weight' : 150,
        'max_bin'          : 20,
        'min_split_gain'   : 0,
        'max_drop'         : 70,
        'drop_rate'        : 0.2
        
    
}
d_train = lgb.Dataset(x1, label=y1)
d_valid = lgb.Dataset(x2, label=y2)
model_lgb = lgb.train(params, d_train, 10000, valid_sets=d_valid,# feval=feval_func,
                      early_stopping_rounds=200, verbose_eval=100)
sub_df['num_of_people2']=model_lgb.predict(test)
sub_df.sort_values(by='num_of_people2')


# 对两个模型预测结果求平均
sub_df['num_of_people']=(sub_df['num_of_people1']+sub_df['num_of_people2'])/2
sub_df.loc[sub_df['num_of_people']<0,'num_of_people']=1
del sub_df['num_of_people1']
del sub_df['num_of_people2']
sub_df.to_csv('sub2.csv',index=False)
print ('完成，生成结果文件')
sub_df.sort_values(by='num_of_people')

