

# -*- coding: utf-8 -*-
#! /usr/bin/env python3


# Author:    FANG Junying  junyinghouse@gmail.com
# Date:      2018/11/13

import numpy as np
import pandas as pd
import time
from scipy import fftpack as fft
class emotionProcessor():
    def __init__(self,srate,baselinesize):
        if srate == None:
            srate = 1000
        self.srate = srate
        self.baselinesize = baselinesize
        self.baselinebuffer = list(np.zeros(baselinesize))
        self.counter = 0
        self.emotionOutput = 0

    def process(self,x):
        ## F3, F4 , alpha 左右比值
        data = x.T
        nPoints,nChans = data.shape
        fftPower = np.zeros((1,nChans))
        diffData = pd.DataFrame(data).diff()
        wrongpos1 = np.where(np.array(diffData) > 1000)
        if len(wrongpos1[0]) > 0:
            for i in range(len(wrongpos1[0])):
                data[wrongpos1[0][i]][wrongpos1[1][i]] = data[wrongpos1[0][i]][wrongpos1[1][i] - 1]

        for i in range(int(nPoints/self.srate)):
            tempbaseline = np.mean(data[i * self.srate:((i + 1) * self.srate), :], axis=0)
            data[i * self.srate:((i + 1) * self.srate), :] =  data[i*self.srate:((i+1)*self.srate),:]  - tempbaseline
        wrongpos2 = np.where(np.array(data) > 75)
        for i in range(len(wrongpos2[0])):
            try:
                data[wrongpos2[0][i]][wrongpos2[1][i]] = data[wrongpos2[0][i]][wrongpos2[1][i]-1]
            except:
                pass
        for k in range(nChans):
            fftPower[0][k] = np.sum(np.abs(fft.fft(data[:, k])[8:12]))

        emotion = np.log(fftPower[0][0]+1e-5) - np.log(fftPower[0][1]+1e-5)

        if self.counter <= self.baselinesize:
            self.counter += 1
            # print(emotion)
            self.baselinebuffer.pop(0)
            self.baselinebuffer.append(emotion)
        else:
            if np.std(self.baselinebuffer) != 0:
                if (emotion - np.mean(self.baselinebuffer))/(np.std(self.baselinebuffer)) > 1.5:
                    self.emotionOutput += 1
                elif (emotion - np.mean(self.baselinebuffer))/(np.std(self.baselinebuffer)) < -1.5:
                    self.emotionOutput -= 1
                else:
                    pass
            elif np.std(self.baselinebuffer) == 0:
                if (emotion - np.mean(self.baselinebuffer)) > 0:
                    self.emotionOutput += 1
                elif (emotion - np.mean(self.baselinebuffer)) < 0:
                    self.emotionOutput -= 1
                else:
                    pass
            self.baselinebuffer.pop(0)
            self.baselinebuffer.append(emotion)

        if self.emotionOutput > 9:
            self.emotionOutput = 9
        elif self.emotionOutput < -9:
            self.emotionOutput = -9
        else:
            pass

        return self.emotionOutput




