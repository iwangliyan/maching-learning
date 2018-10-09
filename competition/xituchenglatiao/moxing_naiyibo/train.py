import time
import datetime
import math
import numpy as np
import pandas as pd
import lightgbm as lgb
from dateutil.parser import parse
from sklearn.cross_validation import KFold
from sklearn.metrics import mean_squared_error


train = pd.read_csv('./chouchoukan.csv')
dev = pd.read_csv('./chouchoukan_dev.csv')

# train = train.drop(['data_min_week','data_median','data_min','data_max','data_mean'],axis = 1)
# test = test.drop(['data_min_week','data_median','data_min','data_max','data_mean'],axis = 1)
# print(train['holiday'])
# del test['holiday']
# del dev['holiday']
# del train['holiday']
# train = train.astype('float64')
predictors = [f for f in train.columns if f not in ['phone_num','time_stamp']]

def evalerror(pred, df):
    label = df.get_label().values.copy()
    score = math.sqrt(mean_squared_error(label,pred))
    return ('mse',score,False)

print('Training..')
params = {
    'learning_rate': 0.01,
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'rmse',
    'sub_feature': 0.7,
    'num_leaves': 60,
    'colsample_bytree': 0.7,
    'feature_fraction': 0.7,
    'min_data': 100,
    'min_hessian': 1,
    'verbose': -1,
}

# from sklearn.cross_validation import train_test_split  
# train_feat, val_feat, train_y, val_y = train_test_split(train[predictors],train['phone_num'],test_size = 0.2,random_state=42) 
train_feat = train[predictors]
train_y = train['phone_num']

val_feat = dev[predictors]
val_y = dev['phone_num']
lgb_train = lgb.Dataset(train_feat, train_y,categorical_feature=['loc_hour','loc_week','loc_rate','loc_weather','hour_rate','hour_weather','hour_week','week_rate','week_weather','rate_weather','loc_id','week','hour','weather','rate'])
lgb_val = lgb.Dataset(val_feat, val_y,categorical_feature=['loc_hour','loc_week','loc_rate','loc_weather','hour_rate','hour_weather','hour_week','week_rate','week_weather','rate_weather','loc_id','week','hour','weather','rate'])
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=50000,
                valid_sets=lgb_val,
                verbose_eval=100,
                feval=evalerror,
                early_stopping_rounds=100)
print(pd.Series(gbm.feature_importance(),index = predictors).sort_values(ascending = False))
# import pickle
# with open('gbm_pm25_ld.pkl', 'wb') as f:
#     pickle.dump(gbm, f)

