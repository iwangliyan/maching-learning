# coding:utf-8
import math
import numpy as np
import pandas as pd
import seaborn as sns
from pandas import DataFrame
from xgboost import XGBRegressor
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error

from hyperopt import fmin, tpe, hp,space_eval,rand,Trials,partial,STATUS_OK
import matplotlib.pyplot as plt
# 读取数据
path_train = 'E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/train_featured_人群分类.csv'
path_test = 'E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/test_featured_人群分类.csv'
train = pd.read_csv(path_train)
test = pd.read_csv(path_test)
X_test_divided = train.drop(train[(train['month'] != 10) | (train['day'] < 25)].index).reset_index(drop=True)
X_train_divided = train.drop(train[(train['month'] == 10) & (train['day'] > 24)].index).reset_index(drop=True)
'''
train_full = X_train_divided

# 异常值处理

for i in range(1, 34):
    for j in range(24):
        data = train_full.drop(train_full[(train_full['location'] != i) | (train_full['hour'] != j)].index)  # .reset_index(drop=True)
        # print(data.index)
        # print(data['registered'])
        q_point = data['registered'].quantile([0.25, 0.75, 0.5]).values  # 找到上下四分位点
        up = q_point[1] + 1.5 * (q_point[1] - q_point[0])
        down = q_point[0] - 1.5 * (q_point[1] - q_point[0])
        middle = q_point[2]
        print('第', i, '个地点', '第', j, '小时', up, down, q_point[0], q_point[1])
        # print(middle)
        temp = data[(data['registered'] < down) | (data['registered'] > up)].index
        # print(train_full.loc[temp]['registered'])
        for item in temp:
            train_full['registered'][item] = middle
        # print(train_full.loc[temp]['registered'])
        # train_full.loc[data[(data['registered'] < down) | (data['registered'] > up)].index]['registered'] = middle

        # print(train_full.loc[data[(data['registered'] < down) | (data['registered'] > up)].index]['registered'])

        # train_full = train_full.drop(data[(data['registered'] < down) | (data['registered'] > up)].index)
        # print(len(train_full['registered']))

for i in range(1, 34):
    for j in range(24):
        data = train_full.drop(train_full[(train_full['location'] != i) | (train_full['hour'] != j)].index)  # .reset_index(drop=True)
        # print(data.index)
        # print(data['registered'])
        q_point = data['casual'].quantile([0.25, 0.75, 0.5]).values  # 找到上下四分位点
        up = q_point[1] + 1.5 * (q_point[1] - q_point[0])
        down = q_point[0] - 1.5 * (q_point[1] - q_point[0])
        middle = q_point[2]
        print('第', i, '个地点', '第', j, '小时', up, down, q_point[0], q_point[1])
        # print(middle)
        temp = data[(data['casual'] < down) | (data['casual'] > up)].index
        # print(train_full.loc[temp]['casual'])
        for item in temp:
            train_full['casual'][item] = middle
        # print(train_full.loc[temp]['casual'])
        # train[(data['casual'] < down) | (data['casual'] > up)]['casual'] = middle
        # train_full = train_full.drop(data[(data['casual'] < down) | (data['casual'] > up)].index)
        # print(len(train_full['casual']))

X_train_divided = train_full

print('异常值处理完毕')
X_train_divided.to_csv('E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/X_train_divided_异常值处理后的特征集3.5.csv', index=False)
'''

'''
# 以复制形式扩充训练集
# max(floor(30/log(rank+3))-7, 1)
locations = [pd.DataFrame()]*33
all_locations = pd.DataFrame()
for i in range(1, len(locations)+1):
    print('第', i, '个地点')
    locations[i-1] = X_train_divided.drop(X_train_divided[(X_train_divided['location'] != i)].index).reset_index(drop=True)
    locations[i-1] = locations[i-1].sort_values(by=['month', 'day', 'hour'], ascending=False)
    print(locations[i-1].head(3))
    original_lenth = len(locations[i-1])
    print(original_lenth)
    for j in range(original_lenth):
        for k in range(max(math.floor(30/math.log10(j+20))-7, 1)):
            locations[i-1].loc[len(locations[i-1])+1] = locations[i-1].loc[j]
    all_locations = pd.concat([all_locations, locations[i-1]], axis=0)
    print(len(all_locations))
all_locations.to_csv('E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/test_featured_人群分类_扩充之后.csv', index=False)
X_train_divided = all_locations
'''

X_train_divided = pd.read_csv('E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/所有train进行异常值处理后的特征集.csv')

# 分割食堂和平常
X_train_divided_shitang = X_train_divided.drop(X_train_divided[(X_train_divided['big_loc'] != 'shitang')].index)
X_train_divided_else = X_train_divided.drop(X_train_divided[(X_train_divided['big_loc'] == 'shitang')].index)
X_test_divided_shitang0 = X_test_divided.drop(X_test_divided[(X_test_divided['big_loc'] != 'shitang')].index)
X_test_divided_else0 = X_test_divided.drop(X_test_divided[(X_test_divided['big_loc'] == 'shitang')].index)


# 正常处理开始，分割训练集测试集

print(len(X_train_divided))
y_train_divided_shitang_registered = X_train_divided_shitang.pop('registered')
y_train_divided_shitang_casual = X_train_divided_shitang.pop('casual')
y_test_divided_shitang_registered = X_test_divided_shitang0.pop('registered')
y_test_divided_shitang_casual = X_test_divided_shitang0.pop('casual')

y_train_divided_else_registered = X_train_divided_else.pop('registered')
y_train_divided_else_casual = X_train_divided_else.pop('casual')
y_test_divided_else_registered = X_test_divided_else0.pop('registered')
y_test_divided_else_casual = X_test_divided_else0.pop('casual')


y_train_registered = train.pop('registered')
y_train_casual = train.pop('casual')

# 定义目标函数
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())
# print(train.head(3))
# print(train.head(3))

# y_train_casual = np.log1p(y_train_casual)
# y_train_registered = np.log1p(y_train_registered)
# train['flow'] = np.log1p(train['flow'])
# test['flow'] = np.log1p(test['flow'])

train.pop('day')
test.pop('day')

# train.pop('flow')
# test.pop('flow')


# 将分类的数值特征进行one-hot编码
cols = ('location', 'weekday', 'hour_cat', 'big_loc', 'weather1', 'weather2', 'air', 'working')
for c in cols:
    train[c] = train[c].astype(str)
    test[c] = test[c].astype(str)
    X_train_divided_shitang[c] = X_train_divided_shitang[c].astype(str)
    X_train_divided_else[c] = X_train_divided_else[c].astype(str)
    X_test_divided_shitang0[c] = X_test_divided_shitang0[c].astype(str)
    X_test_divided_else0[c] = X_test_divided_else0[c].astype(str)
train = pd.get_dummies(train)
test = pd.get_dummies(test)
X_train_divided_shitang = pd.get_dummies(X_train_divided_shitang)
X_train_divided_else = pd.get_dummies(X_train_divided_else)
X_test_divided_shitang = pd.get_dummies(X_test_divided_shitang0)
X_test_divided_else = pd.get_dummies(X_test_divided_else0)

# 分割训练集和验证集合
# X_train_divided, X_test_divided, y_train_divided, y_test_divided = train_test_split(train, y_train, test_size=0.3, random_state=0)

features_shitang = ['month', 'week', 'hour', 'max_temp', 'min_temp', 'location_8', 'location_10', 'location_12', 'location_29',
                    'weekday_1', 'hour_cat_3', 'hour_cat_4', 'hour_cat_5', 'hour_cat_1', 'hour_cat_2', 'hour_cat_0',
                    'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'weekday_7',
                    'hour_cat_10', 'hour_cat_11', 'hour_cat_12', 'hour_cat_13', 'hour_cat_14',
                    'hour_cat_15', 'hour_cat_16', 'hour_cat_17', 'hour_cat_18', 'hour_cat_19',
                    'hour_cat_20', 'hour_cat_21', 'hour_cat_22', 'hour_cat_23',  'hour_cat_6', 'hour_cat_7', 'hour_cat_8', 'hour_cat_9', 'weather1_1', 'weather1_2',
                    'weather1_4', 'weather2_1', 'weather2_2', 'working_no', 'working_yes']
# 删除的特征有：'weather1_3' 'weather2_3' 'weather2_4' 'air4', 'air_1', 'air_2', 'air_3', 'wind1', 'wind2' 'flow', 'flow2', 'big_loc_shitang', 'big_loc_jiaoxuelou', 'big_loc_sushe'
#

features_else = ['month', 'week', 'hour', 'max_temp', 'min_temp', 'location_1', 'location_11',  'location_13', 'location_14',
                 'location_15', 'location_16', 'location_17', 'location_18', 'location_19','location_2', 'location_20',
                 'location_21', 'location_22', 'location_23', 'location_24', 'location_25', 'location_26',
                 'location_27', 'location_28', 'location_3', 'location_30', 'location_31', 'location_32',
                 'location_33', 'location_4', 'location_5', 'location_6', 'location_7', 'location_9',
                 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'weekday_7',
                 'hour_cat_0', 'hour_cat_1', 'hour_cat_10', 'hour_cat_11', 'hour_cat_12', 'hour_cat_13', 'hour_cat_14',
                 'hour_cat_15', 'hour_cat_16', 'hour_cat_17', 'hour_cat_18', 'hour_cat_19', 'hour_cat_2',
                 'hour_cat_20', 'hour_cat_21', 'hour_cat_22', 'hour_cat_23', 'hour_cat_3', 'hour_cat_4', 'hour_cat_5',
                 'hour_cat_6', 'hour_cat_7', 'hour_cat_8', 'hour_cat_9','big_loc_jiaoxuelou', 'big_loc_sushe',
                 'weather1_1', 'weather1_2', 'weather1_4', 'weather2_1', 'weather2_2', 'working_no', 'working_yes']
# 删除的特征有：'weather1_3' 'weather2_3' 'weather2_4' 'air4', 'air_1', 'air_2', 'air_3', 'wind1', 'wind2' 'flow', 'flow2', 'big_loc_shitang'

# X_train_divided = X_train_divided[features]
# X_test_divided = X_test_divided[features]


# ---------------------------------------------食堂预测部分--------------------------------------------------------#
# 真正预测部分
gbm_shitang_registered = XGBRegressor(nthread=4,  # 进程数
                                      n_estimators=260,  # 树的数量
                                      learning_rate=0.05,  # 学习率
                                      subsample=0.8,  # 采样数
                                      max_depth=11,  # 最大深度
                                      min_child_weight=1,  # 孩子数
                                      )  # max_delta_step=10)  # 10步不降则停止
gbm_shitang_registered.fit(X_train_divided_shitang[features_shitang], y_train_divided_shitang_registered)   # X_train_divided[features], y_train_divided_registered  # train[features], y_train_registered
y_pred_shitang_registered = gbm_shitang_registered.predict(X_test_divided_shitang[features_shitang])  # X_test_divided[features]  # test[features]


print('registered predicted !')
gbm_shitang_casual = XGBRegressor(nthread=4,  # 进程数
                                  n_estimators=310,  # 树的数量
                                  learning_rate=0.07,  # 学习率
                                  subsample=0.6,  # 采样数
                                  max_depth=13,  # 最大深度
                                  min_child_weight=4,  # 孩子数
                                  gamma=0.5
                                  )  # max_delta_step=10)  # 10步不降则停止
gbm_shitang_casual.fit(X_train_divided_shitang[features_shitang], y_train_divided_shitang_casual)  # X_train_divided[features], y_train_divided_casual  # train[features], y_train_casual
y_pred_shitang_casual = gbm_shitang_casual.predict(X_test_divided_shitang[features_shitang])  # X_test_divided[features]  # test[features]
print('casual predicted !')

# xgb.plot_importance(gbm_registered)
# plt.show()
# xgb.plot_importance(gbm_casual)
# plt.show()
y_pred_shitang = y_pred_shitang_registered + y_pred_shitang_casual
zero_count = 0
for i in range(len(y_pred_shitang)):
    # print(i)
    if y_pred_shitang[i] < 0:
        y_pred_shitang[i] = 0
        zero_count += 1
print('一共统计出', zero_count, '个0')

y_rule = X_test_divided_shitang['flow'].values
y_rule2 = X_test_divided_shitang['flow2'].values
y_rule3 = X_test_divided_shitang['flow3'].values
y_test_divided_shitang = (y_test_divided_shitang_casual + y_test_divided_shitang_registered)
score = rmse(y_pred_shitang, y_test_divided_shitang.values)
print(score)
score2 = rmse(y_rule, y_test_divided_shitang.values)
score3 = rmse(y_rule2, y_test_divided_shitang.values)
score4 = rmse(y_rule3, y_test_divided_shitang.values)

score5 = rmse((y_rule*0.5)+(y_rule2*0.5), y_test_divided_shitang.values)
score6 = rmse((y_rule*0.5)+(y_rule3*0.5), y_test_divided_shitang.values)
score7 = rmse((y_rule2*0.5)+(y_rule3*0.5), y_test_divided_shitang.values)
score8 = rmse((y_rule3*0.5)+(y_pred_shitang*0.5), y_test_divided_shitang.values)

score9 = rmse((y_rule*(1/3))+(y_rule2*(1/3)+(y_rule3*(1/3))), y_test_divided_shitang.values)
score10 = rmse((y_rule*(1/4))+(y_rule2*(1/4)+(y_rule3*(1/4))+(y_pred_shitang*(1/4))), y_test_divided_shitang.values)
print(score, score2, score3, score4)
print(score5, score6, score7, score8)
print(score9, score10)
X_test_divided_shitang0['pred_flow'] = y_pred_shitang

# ---------------------------------------------其余地点预测部分--------------------------------------------------------#
# 真正预测部分
gbm_else_registered = XGBRegressor(nthread=4,  # 进程数
                                   n_estimators=310,  # 树的数量
                                   learning_rate=0.10,  # 学习率
                                   subsample=0.7,  # 采样数
                                   max_depth=14,  # 最大深度
                                   min_child_weight=5,  # 孩子数
                                   )  # max_delta_step=10)  # 10步不降则停止
gbm_else_registered.fit(X_train_divided_else[features_else], y_train_divided_else_registered)   # X_train_divided[features], y_train_divided_registered  # train[features], y_train_registered
y_pred_else_registered = gbm_else_registered.predict(X_test_divided_else[features_else])  # X_test_divided[features]  # test[features]
print('registered predicted !')
gbm_else_casual = XGBRegressor(nthread=4,  # 进程数
                               n_estimators=330,  # 树的数量
                               learning_rate=0.09,  # 学习率
                               subsample=0.7,  # 采样数
                               max_depth=13,  # 最大深度
                               min_child_weight=0,  # 孩子数
                               gamma=0.5
                               )  # max_delta_step=10)  # 10步不降则停止
gbm_else_casual.fit(X_train_divided_else[features_else], y_train_divided_else_casual)  # X_train_divided[features], y_train_divided_casual  # train[features], y_train_casual
y_pred_else_casual = gbm_else_casual.predict(X_test_divided_else[features_else])  # X_test_divided[features]  # test[features]
print('casual predicted !')

# xgb.plot_importance(gbm_registered)
# plt.show()
# xgb.plot_importance(gbm_casual)
# plt.show()
y_pred_else = y_pred_else_registered + y_pred_else_casual
zero_count = 0
for i in range(len(y_pred_else)):
    # print(i)
    if y_pred_else[i] < 0:
        y_pred_else[i] = 0
        zero_count += 1
print('一共统计出', zero_count, '个0')

y_rule = X_test_divided_else['flow'].values
y_rule2 = X_test_divided_else['flow2'].values
y_rule3 = X_test_divided_else['flow3'].values
y_test_divided_else = (y_test_divided_else_casual + y_test_divided_else_registered)
score = rmse(y_pred_else, y_test_divided_else.values)
print(score)
score2 = rmse(y_rule, y_test_divided_else.values)
score3 = rmse(y_rule2, y_test_divided_else.values)
score4 = rmse(y_rule3, y_test_divided_else.values)

score5 = rmse((y_rule*0.5)+(y_rule2*0.5), y_test_divided_else.values)
score6 = rmse((y_rule*0.5)+(y_rule3*0.5), y_test_divided_else.values)
score7 = rmse((y_rule2*0.5)+(y_rule3*0.5), y_test_divided_else.values)
score8 = rmse((y_rule3*0.5)+(y_pred_else*0.5), y_test_divided_else.values)

score9 = rmse((y_rule*(1/3))+(y_rule2*(1/3)+(y_rule3*(1/3))), y_test_divided_else.values)
score10 = rmse((y_rule*(1/4))+(y_rule2*(1/4)+(y_rule3*(1/4))+(y_pred_else*(1/4))), y_test_divided_else.values)
print(score, score2, score3, score4)
print(score5, score6, score7, score8)
print(score9, score10)
X_test_divided_else0['pred_flow'] = y_pred_else
# ---------------------------------------------两部分进行结合--------------------------------------------------------#

temp_result = pd.concat([X_test_divided_shitang0, X_test_divided_else0], axis=0)
y_real_shitang = pd.DataFrame(y_test_divided_shitang_registered + y_test_divided_shitang_casual)  # 整合食堂预测流量
y_real_else = pd.DataFrame(y_test_divided_else_registered + y_test_divided_else_casual)  # 整合其他地点预测流量
y_real = pd.concat([y_real_shitang, y_real_else], axis=0)  # 整合所有真实流量

temp_result['ground_truth'] = y_real
temp_result = temp_result.sort_values(by=['month', 'day', 'hour', 'location'])  # 进行排序
y_pred = temp_result['pred_flow']  # 抽取全部预测流量
y_rule = temp_result['flow']
y_rule2 = temp_result['flow2']
y_rule3 = temp_result['flow3']
score11 = rmse(y_pred.values, temp_result['ground_truth'].values)
score2 = rmse(y_rule, temp_result['ground_truth'].values)
score3 = rmse(y_rule2, temp_result['ground_truth'].values)
score4 = rmse(y_rule3, temp_result['ground_truth'].values)

score5 = rmse((y_rule*0.5)+(y_rule2*0.5), temp_result['ground_truth'].values)
score6 = rmse((y_rule*0.5)+(y_rule3*0.5), temp_result['ground_truth'].values)
score7 = rmse((y_rule2*0.5)+(y_rule3*0.5), temp_result['ground_truth'].values)
score8 = rmse((y_rule3*0.5)+(y_pred*0.5), temp_result['ground_truth'].values)

score9 = rmse((y_rule*(1/3))+(y_rule2*(1/3)+(y_rule3*(1/3))), temp_result['ground_truth'].values)
score10 = rmse((y_rule*(1/4))+(y_rule2*(1/4)+(y_rule3*(1/4))+(y_pred*(1/4))), temp_result['ground_truth'].values)
print('  ')
print(score11, score2, score3, score4)
print(score5, score6, score7, score8)
print(score9, score10)

# y_pred.to_csv('E:/学习/研究生1/创新竞赛/2018年算法赛/data/xgboost/XGBoost_最强版本.csv')

'''


# 调参部分
'''
X_train_divided = X_train_divided_shitang[features_shitang]
y_train_divided_registered = y_train_divided_shitang_registered
X_test_divided = X_test_divided_shitang[features_shitang]
y_test_divided_registered = y_test_divided_shitang_registered

print(len(X_train_divided))
print(len(y_train_divided_registered))
print(len(X_test_divided))
print(len(y_test_divided_registered))
'''
X_train_divided = X_train_divided_else[features_else]
y_train_divided_registered = y_train_divided_else_registered
X_test_divided = X_test_divided_else[features_else]
y_test_divided_registered = y_test_divided_else_registered


def GBM_registered(argsDict):

    global X_train_divided, y_train_divided_registered, y_test_divided_registered, X_test_divided
    gbm_registered = XGBRegressor(nthread=4,    # 进程数
                       max_depth=argsDict["max_depth"],  # 最大深度
                       n_estimators=argsDict['n_estimators'] * 10 + 50,   # 树的数量
                       learning_rate=argsDict["learning_rate"] * 0.01 + 0.02,  # 学习率
                       subsample=argsDict["subsample"] * 0.1 + 0.1,  # 采样数
                       min_child_weight=argsDict["min_child_weight"],   # 孩子数
                       )  # max_delta_step=10)  # 10步不降则停止

    gbm_registered.fit(X_train_divided, y_train_divided_registered)
    y_pred_registered_para = gbm_registered.predict(X_test_divided)
    score1 = rmse(y_pred_registered_para, y_test_divided_registered.values)
    # score1 = np.mean(np.sqrt(-cross_val_score(gbm_registered, X_train_divided, y_train_divided_registered, cv=2, scoring='neg_mean_squared_error', verbose=1)))
    print(score1)
    return score1


space_registered = {"max_depth": hp.randint("max_depth", 15),
                    "n_estimators": hp.randint("n_estimators", 30),  # [0,1,2,3,4,5] -> [50,]
                    "learning_rate": hp.randint("learning_rate", 10),  # [0,1,2,3,4,5] -> 0.05,0.06
                    "subsample": hp.randint("subsample", 10),  # [0,1,2,3] -> [0.7,0.8,0.9,1.0]
                    "min_child_weight": hp.randint("min_child_weight", 10)
                    }
algo_registered = partial(tpe.suggest, n_startup_jobs=10)
best_registered = fmin(GBM_registered, space_registered, algo=algo_registered, max_evals=100)

print(best_registered)
print(GBM_registered(best_registered))

'''
y_train_divided_casual = y_train_divided_shitang_casual
y_test_divided_casual = y_test_divided_shitang_casual
'''
y_train_divided_casual = y_train_divided_else_casual
y_test_divided_casual = y_test_divided_else_casual



def GBM_casual(argsDict):

    global X_train_divided, y_train_divided_casual, y_test_divided_casual, X_test_divided
    gbm_casual = XGBRegressor(nthread=4,    # 进程数
                              max_depth=argsDict["max_depth"],  # 最大深度
                              n_estimators=argsDict['n_estimators'] * 10 + 50,   # 树的数量
                              learning_rate=argsDict["learning_rate"] * 0.01 + 0.02,  # 学习率
                              subsample=argsDict["subsample"] * 0.1 + 0.1,  # 采样数
                              min_child_weight=argsDict["min_child_weight"],   # 孩子数
                              )  # max_delta_step=10)  # 10步不降则停止

    gbm_casual.fit(X_train_divided, y_train_divided_casual)
    y_pred_casual_para = gbm_casual.predict(X_test_divided)
    score2 = rmse(y_pred_casual_para, y_test_divided_casual.values)
    # score2 = np.mean(np.sqrt(-cross_val_score(gbm_casual, X_train_divided, y_train_divided_casual, cv=2, scoring='neg_mean_squared_error', verbose=1)))
    print(score2)
    return score2


space_casual = {"max_depth": hp.randint("max_depth", 15),
                    "n_estimators": hp.randint("n_estimators", 30),  # [0,1,2,3,4,5] -> [50,]
                    "learning_rate": hp.randint("learning_rate", 10),  # [0,1,2,3,4,5] -> 0.05,0.06
                    "subsample": hp.randint("subsample", 10),  # [0,1,2,3] -> [0.7,0.8,0.9,1.0]
                    "min_child_weight": hp.randint("min_child_weight", 10)
                }
algo_casual = partial(tpe.suggest, n_startup_jobs=10)
best_casual = fmin(GBM_casual, space_casual, algo=algo_casual, max_evals=100)
print(best_casual)
print(GBM_casual(best_casual))
'''

