import json
import datetime
from sklearn import preprocessing
import numpy as np

fid = open("data/trains.json")
data_raw = json.load(fid)
fid.close()
start_time = datetime.datetime.strptime("2017-10-17", "%Y-%m-%d")
feats_raw = []
labs = []
for data in data_raw:
    data_time = datetime.datetime.strptime(data["date"], "%Y-%m-%d:%H")
    if data_time > start_time:
        holiday = int(data_time.weekday() == 5 or data_time.weekday() == 6)
        feats_raw.append([holiday, data_time.weekday(), data_time.hour, data["place"] - 1])
        labs.append(data["people"])
ohcoder = preprocessing.OneHotEncoder()
ohcoder.fit(feats_raw)
print("code len:", ohcoder.n_values_)
feats = ohcoder.transform(feats_raw).toarray()



def gen_times(begin_date, end_date):
    delta_time = datetime.timedelta(hours=1)
    while begin_date < end_date:
        yield begin_date
        begin_date = begin_date + delta_time


file_name = "result/result_2018-05-27.csv"
fid = open(file_name, 'w', encoding='utf8')
begin_date = datetime.datetime.strptime("2017-12-01", "%Y-%m-%d")
end_date = datetime.datetime.strptime("2018-01-01", "%Y-%m-%d")
for loc in range(1, 34):
    for time in gen_times(begin_date, end_date):
        feat_raw = np.array([int(time.weekday() == 5 or time.weekday() == 6), time.weekday(), time.hour, loc - 1])
        feat = ohcoder.transform(feat_raw.reshape(1, 4)).toarray()
        dtest = xgb.DMatrix(feat)
        res = model.predict(dtest)
        tmp = [str(loc), datetime.datetime.strftime(time, "%Y-%m-%d %H"), str(max(res[0], 0)) + "\n"]
        fid.write(",".join(tmp))
fid.close()

file_name1 = "data/result_2018-05-26-12.csv"
file_name2 = "data/result_2018-05-27-3338789.csv"
fid = open(file_name1,"r")
line1 = fid.readlines()
fid.close()
fid = open(file_name2,"r")
line2 = fid.readlines()
fid.close()

n = len(line1)
fid = open("data/combine1.csv", 'w',encoding='utf8')
for i in range(n):
    tmp = line1[i].strip("\n").split(",")[:-1]
    res = (float(line1[i].strip("\n").split(",")[-1]) + float(line2[i].strip("\n").split(",")[-1]))/2
    tmp.append(str(res)+"\n")
    fid.write(",".join(tmp))
fid.close()