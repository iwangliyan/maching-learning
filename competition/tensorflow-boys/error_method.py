# _*_ coding utf:8 _*_
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def show_fft(data, axis=0):
    data_fft = np.fft.fft(data.X[axis])
    plt.plot(np.abs(data_fft))
    half_size = int(data_fft.size/2)
    max_index = np.argmax(data_fft[: half_size])
    f_data = 1/data.dt
    f = max_index * f_data / data.n
    T = 1/f
    print('该样本第{}个节点的固有频率为：{},周期为{}'.format(axis, f, T))
    return T



def show_errors(real, predicted, name='error'):
    # print('________________________')
    # print('误差分析：')
    # print('MSE:{:.4f}'.format(mse(real, predicted)))
    print('{}:{:.4f}'.format(name, rmse(real, predicted)))
    # print('MAE:{:.4f}'.format(mae(real, predicted)))
    # print('MPAE:{:.4f}%'.format(mape(real, predicted)))


def deviation(x, y):

    d = (x - y).dropna()
    return x, y, d


def mse(x, y):
    x, y, d = deviation(x, y)
    return (d**2).sum()/d.size


def rmse(x, y):
    return np.sqrt(mse(x, y))


def mae(x, y):
    x, y, d = deviation(x, y)
    return np.abs(d).sum().sum()/d.size


def mape(real, predict):
    real, predict, d = deviation(real, predict)
    return np.abs(d / real).sum().sum()/d.size * 100
