import xgboost as xgb
param = {'bst:max_depth':6, 'bst:eta':0.1, 'silent':1, 'objective':'reg:linear' }
plst = param.items()
num_round = 200
# param['nthread'] = 4
# plst += [('eval_metric', 'auc')] # Multiple evals can be handled in this way
# plst += [('eval_metric', 'ams@0')]

dtrain = xgb.DMatrix(train_feats, label=train_labs)
model = xgb.train(plst, dtrain, num_round)
dtest = xgb.DMatrix(train_feats)
train_res = model.predict(dtest)
dtest = xgb.DMatrix(val_feats)
val_res = model.predict(dtest)
plt.figure(figsize=(20,8))
plt.subplot(121)
plt.scatter(train_labs,train_res, color = 'r', s = 20)
plt.plot([0, 13000],[0, 13000])
plt.subplot(122)
plt.scatter(val_labs, val_res, color = 'r', s = 20)
plt.plot([0, 13000],[0, 13000])
plt.show()
print("RMSE:",np.mean((val_res-val_labs)**2)**0.5)


param = {'bst:max_depth': 6, 'bst:eta': 0.1, 'silent': 1, 'objective': 'reg:linear'}
plst = param.items()
num_round = 200

dtrain = xgb.DMatrix(feats, label=labs)
model = xgb.train(plst, dtrain, num_round)

