# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import OrderedDict
import os
import logging




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    read_name = 'train.csv'
    save_name = 'trains.csv'
    
    if os.path.exists(save_name):
        raise OSError('文件已存在，无法保存!')
    train = pd.read_csv(read_name, dtype=object, delimiter=',', header=None)
    n_row, n_col = train.shape
    counter = OrderedDict()
    for i in range(n_row):
        label = (train.iloc[i, 2], train.iloc[i, 1])
        if label in counter:
            counter[label] += 1
        else:
            counter[label] = 1
        
    df_counter = pd.DataFrame(np.zeros((len(counter), 3)))
    for i, item in enumerate(counter.items()):
        df_counter.iloc[i] = [item[0][0], item[0][1], item[1]]
    df_counter = df_counter.sort_values(by=[0, 1], ascending=[True, True])
    df_counter[0] = df_counter[0].apply(pd.to_numeric)
    df_counter.to_csv(save_name, index=False, header=False)
    logging.info('保存成功,新文件名为{}'.format(save_name))
    print(df_counter.describe())
    
        
        
        
    