1.��ѹ"Parsifal_�㷨��.rar"֮����ֱ��ʹ��pycharm���������"Parsifal-�㷨��"�����ļ���
2.��������ȫ��ʹ�á�python3.6����д����Ҫ����İ��У�

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

  # ��ע��hyperopt����������Ӧ����Ҫ���а�װ����

3.�������л����ɴ����м�csv�ļ������ݽ϶��ҷ��ӣ�����ܵ��ļ���С��������1.8G���ң������ʼ��������⣬
  ���������ί����Ҫ�ⲿ���м����ɵ��ļ����ҿ����ṩ��