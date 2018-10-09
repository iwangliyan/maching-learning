import json
import datetime
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as npfrom sklearn import tree
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn.tree import ExtraTreeRegressor


fid = open("data/trains.json")
data_raw = json.load(fid)
fid.close()
start_time = datetime.datetime.strptime("2017-10-17", "%Y-%m-%d")
feats_raw = []
labs = []
for data in data_raw:
    data_time = datetime.datetime.strptime(data["date"], "%Y-%m-%d:%H")
    if data_time > start_time:
        feats_raw.append([data["holiday"], data["week"]-1, data["place"]-1, data_time.hour])
        labs.append(data["people"])

ohcoder = preprocessing.OneHotEncoder()
ohcoder.fit(feats_raw)
print(ohcoder.n_values_)
feats = ohcoder.transform(feats_raw).toarray()

train_feats, val_feats, train_labs, val_labs = train_test_split(feats, labs, test_size = 0.2, random_state = 0)

fid = open("data/trains.json")
data_raw = json.load(fid)
fid.close()
start_time = datetime.datetime.strptime("2017-10-17", "%Y-%m-%d")
val_start = datetime.datetime.strptime("2017-11-24", "%Y-%m-%d")
train_feats_raw = []
train_labs = []
val_feats_raw = []
val_labs = []
for data in data_raw:
    data_time = datetime.datetime.strptime(data["date"], "%Y-%m-%d:%H")
    if data_time > start_time and data_time < val_start:
        train_feats_raw.append([data["holiday"], data["week"], data["place"]-1, data_time.hour])
        train_labs.append(data["people"])
    if data_time >= val_start:
        val_feats_raw.append([data["holiday"], data["week"]-1, data["place"]-1, data_time.hour])
        val_labs.append(data["people"])
ohcoder = preprocessing.OneHotEncoder()
ohcoder.fit(train_feats_raw)
print(ohcoder.n_values_)
train_feats = ohcoder.transform(train_feats_raw).toarray()
val_feats = ohcoder.transform(val_feats_raw).toarray()

def fit_and_perform(model, train_feats, train_labs, val_feats, val_labs):
    model.fit(train_feats, train_labs)
    train_score = model.score(train_feats, train_labs)
    train_res = model.predict(train_feats)
    val_score = model.score(val_feats, val_labs)
    val_res = model.predict(val_feats)
    plt.figure(figsize=(20,8))
    plt.subplot(121)
    plt.scatter(train_labs,train_res, color = 'r', s = 20)
    plt.plot([0, 13000],[0, 13000])
    plt.title('score: %f'%train_score)
    plt.subplot(122)
    plt.scatter(val_labs, val_res, color = 'r', s = 20)
    plt.plot([0, 13000],[0, 13000])
    plt.title('score: %f'%val_score)
    plt.show()
    print("RMSE:",np.mean((val_res-val_labs)**2)**0.5)


model = tree.DecisionTreeRegressor()
# model = linear_model.LinearRegression()
# model = svm.SVR()
# model = neighbors.KNeighborsRegressor()
# model = ensemble.RandomForestRegressor(n_estimators=20)
# model = ensemble.AdaBoostRegressor(n_estimators=50)
# model = ensemble.GradientBoostingRegressor(n_estimators=200)
# model_BaggingRegressor = ensemble.BaggingRegressor()
# model = ExtraTreeRegressor()
fit_and_perform(model, train_feats, train_labs, val_feats, val_labs)

