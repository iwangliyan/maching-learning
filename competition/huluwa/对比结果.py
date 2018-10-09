# -*- coding: utf-8 -*-
"""
Created on Thu May 24 22:53:12 2018

@author: linzizhan
"""

import pandas as pd

df = pd.read_csv('weather.csv')
#df1 = pd.read_csv('gbdt_res.csv')
#df2 = pd.read_csv('ave_res.csv')
#import matplotlib.pyplot as plt
#plt.scatter(df1.num_of_people,df2.num_of_people)
#plt.plot([0,8000],[0,8000])
#df1['num_of_people'] = df1.num_of_people.apply(lambda x:round(x*0.95))
#df1.num_of_people - df2.num_of_people
#import pickle as pkl

#loc_df = []
#with open('loc_df_list.pkl', 'rb') as f:
#    a = pkl.load(f)
#loc_df = []
#for i in range(1, 34):
#    _df = df[df.loc_id == i]
#    _df = handle_features(_df, w)
#    _df.reset_index(inplace=True, drop=True)
#    loc_df.append(_df)
