# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
from datetime import datetime


def res_mean(res1, res2, weight1=0.5):

    m = res1.shape[0]
    res = pd.DataFrame(np.zeros((m, 3)), dtype=object)
    res[0] = res1[0]
    res[1] = res1[1]
    res[2] = weight1 * res1[2] + (1 - weight1) * res2[2]
    res = res.fillna(0)
    return res


if __name__ == '__main__':
    folder = 'result'
    filename = 'res_mean_' + str(datetime.now().date()) + '.csv'
    file1 = 'results_2018-05-24.csv'
    file2 = 'result_2018-05-23.csv'
    path = os.path.join(folder, filename)
    path1 = os.path.join(folder, file1)
    path2 = os.path.join(folder, file2)
    res1 = pd.read_csv(path1, header=None)
    res2 = pd.read_csv(path2, header=None)
    res = res_mean(res1, res2, weight1=0.5)
    res.to_csv(path, index=False, header=False)
    