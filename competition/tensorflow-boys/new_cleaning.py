# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import OrderedDict
import os
import logging




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    folder = '2016_data'
    save_name = 'ori_train.csv'
    read_list = ['train', 'test1', 'test2']

    
    if os.path.exists(save_name):
        raise OSError('文件已存在，无法保存!')
    counter = OrderedDict()
    for i in read_list:
        read_name = folder + '/' + i + '.csv'
        logging.info('read file:{}'.format(read_name))
        train = pd.read_csv(read_name, dtype=object, delimiter=',', header=1)
        n_row, n_col = train.shape

        for j in range(n_row):
            label = (train.iloc[j, 2], train.iloc[j, 1])
            if int(label[1][0:2]) >= 10:
                if label in counter:
                    counter[label] += 1
                else:
                    counter[label] = 1
    
            
    df_counter = pd.DataFrame(np.zeros((len(counter), 3)))
    for i, item in enumerate(counter.items()):
        df_counter.iloc[i] = [item[0][0], item[0][1], item[1]]
    df_counter = df_counter.sort_values(by=[0, 1], ascending=[True, True])
    df_counter[0] = df_counter[0].apply(pd.to_numeric)
#    df_counter[1] = df_counter[1].apply(lambda x:x[5:7]+x[8:10]+x[11:13])
    df_counter.to_csv(save_name, index=False, header=False)
    logging.info('保存成功,新文件名为{}'.format(save_name))
    print(df_counter.describe())
    
        
        
        
    