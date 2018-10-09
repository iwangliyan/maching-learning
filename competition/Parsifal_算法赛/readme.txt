1.解压"Parsifal_算法赛.rar"之后，请直接使用pycharm软件打开整个"Parsifal-算法赛"工程文件。
2.整个工程全部使用【python3.6】编写，需要导入的包有：

  import pandas as pd
  import numpy as np
  import seaborn as sns
  import matplotlib.pyplot as plt
  import datetime
  from xgboost import XGBRegressor
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.linear_model import LinearRegression
  from sklearn.cross_validation import cross_val_score
  from sklearn.cross_validation import train_test_split
  from sklearn.metrics import mean_squared_error
  from hyperopt import fmin, tpe, hp,space_eval,rand,Trials,partial,STATUS_OK

  # 【注】hyperopt包不常见，应该需要自行安装导入

3.程序运行会生成大量中间csv文件，内容较多且繁杂，大概总的文件大小加起来有1.8G左右，发送邮件会有问题，
  如果竞赛评委组需要这部分中间生成的文件，我可以提供。