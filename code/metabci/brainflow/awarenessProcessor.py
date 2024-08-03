# -*- coding: utf-8 -*-
#! /usr/bin/env python3


# Author:    FANG Junying  junyinghouse@gmail.com
# Date:      2018/11/14

import numpy as np
import pandas as pd
import time
from scipy import fftpack as fft
from scipy import signal
import matplotlib.pyplot as plt

class awarenessProcessor():

    def __init__(self,srate = 250, freqNotch = 50,threshold=0.35):
        self.srate = srate
        self.freqNotch = freqNotch
        self._reSrate = 250
        w0, Q = self.freqNotch / (self._reSrate / 2), 20
        self.preprocessFilterCoef = dict(b=[], a=[])
        # ”Q” 是指波器的质量因子，它描述了滤波器的带宽和中心频率之间的关系。
        # 表示滤波器的带宽相对于中心频率的宽窄程度，因此这个值会影响信号滤波的效果。
        b, a = signal.iirnotch(w0=w0, Q=Q)  # 其中 w0 是中心频率，Q 是质因数。
        # 调用这个函数会返回滤波器的传递函数系数 b 和 a。这些系数可以用于对输入信号进行滤波操作。
        self.preprocessFilterCoef['b'].append(b)
        self.preprocessFilterCoef['a'].append(a)
        b = [0.00842862794201852, 0, -0.0337145117680741, 0, 0.0505717676521111, 0, -0.0337145117680741, 0,
             0.00842862794201852]
        a = [1, -6.05023914232432, 16.0672806050219, -24.5619000248999, 23.7209182114390,
             -14.8469602184898, 5.88026365830379, -1.34582826820149, 0.136465182736200]
        self.preprocessFilterCoef['b'].append(np.asarray(b))
        self.preprocessFilterCoef['a'].append(np.asarray(a))
        self.filterBank()

    def process(self, data):
        #数据处理函数
        data = self.filterPreprocess(data) #滤波器 预处理 data为预处理后的数据
        (nChans, nPoints) = data.shape
        dataFilterBank = self.decomposeEEG(data) #dataFilterBank可能为处理后的alpha的频段数据
        alpha = dataFilterBank[0]
        R = []
        for i in range(data.shape[0]):
            temp = np.corrcoef(data[i, :], alpha[i, :])[0, 1] # 计算数据行和alpha行的相关系数
            R.append(temp) # 将计算的相关系数添加到列表R中
        ratio2 = np.mean(np.array(R)) # 计算R列表中的平均值
        return ratio2

    def decomposeEEG(self,data): #对输入的 EEG 数据应用滤波器系数进行滤波处理，并返回处理后的数据列表。 ！！找师姐
        dataT = data.T
        sz = dataT.shape
        nFilterBank = len(self.filterBankCoef['b'])
        dataFilterBank = [] #用于存储滤波处理后的数据
        for idxFilter in range(nFilterBank):
            dataFilted = np.zeros(sz)
            for j in range(sz[1]):
                dataFilted[:, j] = signal.filtfilt(self.filterBankCoef['b'][idxFilter], self.filterBankCoef['a'][idxFilter],dataT[:, j])
            dataFilterBank.append(dataFilted.T)
        return dataFilterBank

    def filterBank(self):   #输入了哪一个？
        self.filterBankCoef = dict(b=[], a=[])
        # 8- 13Hz
        b = [0.000219606211224022,0,-0.000658818633672065,0,0.000658818633672065,0,-0.000219606211224022]
        a = [1,-5.56079349059432,13.0652289772800,-16.5937442756934,12.0140576812634,-4.70214056108852,0.777638560238082]
        # b = [1.32937289e-05, 0.00000000e+00, - 5.31749156e-05, 0.00000000e+00, 7.97623734e-05, 0.00000000e+00 ,- 5.31749156e-05, 0.00000000e+00, 1.32937289e-05]
        # a = [1. , - 7.42078963, 24.33387612, - 46.0424045,  54.9728954, -42.40969785, 20.64571976 ,-5.79949408,0.71991033]
        self.filterBankCoef['b'].append(np.asarray(b))
        self.filterBankCoef['a'].append(np.asarray(a))
        # 14-30Hz
        b =  [0.00564754852466921,0,-0.0169426455740076,0,0.0169426455740076,0,-0.00564754852466921]
        a = [1,-4.51670122762224,9.05849614926530,-10.2548740529082,6.90785746292266,-2.62754012296493,0.444898775893761]
        self.filterBankCoef['b'].append(np.asarray(b))
        self.filterBankCoef['a'].append(np.asarray(a))

    def filterPreprocess(self,data):
        data = np.atleast_2d(data)
        dataT = data.T
        nFilterPreprocess = len(self.preprocessFilterCoef['b'])
        sz = dataT.shape
        for i in range(sz[1]):
            for idx in range(nFilterPreprocess):
                dataT[:, i] = signal.filtfilt(self.preprocessFilterCoef['b'][idx],
                                              self.preprocessFilterCoef['a'][idx], dataT[:, i]) #这行代码对 `dataT` 的每一列应用预处理滤波器，使用 `signal.filtfilt` 函数对数据进行滤波处理，并将结果存储回相同的位置。
        return dataT.transpose()





