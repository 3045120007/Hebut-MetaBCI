# -*- coding: utf-8 -*-
# License: MIT License
"""
Start another process, define a framework for offline modeling and online processing with three functions:
    pre(): for offline modeling;

    consume(): for online prediction;

    post(): for subsequent custom operations.

In the actual usage process, you only need to customize the operations of the above functions.
"""
from typing import Optional, Any
from abc import abstractmethod
import os
import multiprocessing
import queue
from .logger import get_logger
import sys
import numpy as np
from struct import pack, unpack
import socket
from dataServerOLD import dataserver_thread, ringBuffer
from emotionForm import Ui_Processor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


logger = get_logger("worker")

def save_result_to_txt(result, filename='output.txt'):
    with open(filename, 'w') as file:
        file.write(str(result))

# class ProcessWorker(multiprocessing.Process):
class ProcessWorker(QMainWindow, Ui_Processor):
    def __init__(self):
        super(ProcessWorker, self).__init__()
        self.setupUi(self)
        self._idx_trigger = 0
        self._flag_stopTimer = False
        self._flag_sock = True

        self.pbStart.clicked.connect(self.pbStart_callback)
        self.pbSetParams.clicked.connect(self.pbSetParams_callback)
        self.pbDataServer.clicked.connect(self.run)
        self.pbOutput.clicked.connect(self.stop)
        self.resultBuffer = ringBuffer(n_chan=3, n_points=60)

        self._timerplot = QTimer(self)
        self._timerplot.timeout.connect(self.put)

    def pbStart_callback(self):
        if self.pbStart.text() == 'Start':
            self.put()
            self._timerplot.start()
            self._timerplot.setInterval(20)
            self.pbStart.setText('Stop')
        elif self.pbStart.text() == 'Stop':
            self._timerplot.stop()
            self.pbStart.setText('Start')
            if hasattr(self, 'udpTriggerThread'):
                self.udpTriggerThread.stop()


    def put(self):
        data = self.thread1.get_bufferData()
        nUpdate = self.thread1.ringBuffer.nUpdate
        result_buffer = np.zeros((2, self.par['nDevice']))
        result_avaliable = True
        emotionOutput, awareOutput, fatigue = 0, 0., 0

        # 处理数据更新和预测结果，保存结果到文件，并将结果添加到 resultBuffer。
        if True:
            self.thread1.ringBuffer.nUpdate = int((self.par['buffersize'] - self.par['ovlap']) * self.par['sampleRate'])
            if 'Neuracle' in self.par['deviceName']:
                predict_label = self.Graph.process_arrays(data)
                if predict_label[0] == 0:
                    self.n1 += 1
                    if self.n1 >= self.N1:
                        result_value = 0
                        save_result_to_txt(result_value, 'outputvideo.txt')
                        self.n1 = 0
                        self.n2 = 0
                else:
                    self.n2 += 1
                    if self.n2 >= self.N2:
                        result_value = 1
                        save_result_to_txt(result_value, 'outputvideo.txt')
                        self.n1 = 0
                        self.n2 = 0
            else:
                predict_label = self.Graph.process_arrays(data)
            self.resultBuffer.appendBuffer(np.asarray([[emotionOutput], [awareOutput], [fatigue]]))

        # 将结果发送到输出设备并更新 EEG 图。
        result_avaliable = True
        if result_avaliable:
            if self.par['isOutput'] and self.pbOutput.text() == 'Disconnect':
                try:
                    self.udpOutput.sendto(pack("fff", emotionOutput, awareOutput, fatigue),
                                          (self.par['ipOutput'], self.par['portOutput']))
                except:
                    raise TypeError('wrong format')
        self.raw = data
        QApplication.processEvents()
        self._idx_trigger = 0


    def run(self):
        if self.par['isOnline']:
            if self.pbDataServer.text() == 'Connect':
                try:
                    self.thread1 = dataserver_thread(threadName='dataServer Thread',
                                                     device=self.par['deviceName'],
                                                     n_chan=self.par['nChan'],
                                                     hostname=self.par['ipData'],
                                                     port=self.par['portData'],
                                                     srate=self.par['sampleRate'],
                                                     t_buffer=self.par['buffersize'])
                    self.thread1.Daemon = True
                    self.thread1.connect()
                except:
                    print("Can't connect recorder. Please open the dataserver port\n")
                else:
                    self.thread1.start()
                    self._flag_stopTimer = False
                    self.pbDataServer.setText('Disconnect')
                    self.pbStart.setEnabled(True)
            elif self.pbDataServer.text() == 'Disconnect':
                self.thread1.stop()
                self._flag_stopTimer = True
                self.pbDataServer.setText('Connect')
                print('Data server disconnected.\n')
                self.pbStart.setEnabled(False)
        else:
            QMessageBox.information(self, ('DataServer Error'), (""" isOnline == False """),
                                    QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))

    @abstractmethod
    def pre(self):
        """Custom function to build a model using offline data.

        author: Lichao Xu

        Created on: 2021-04-01

        update log:
            2022-08-10 by Wei Zhao

        """
        pass

    def pbSetParams_callback(self):
        self.par['sampleRate'] = self.device_config[self.par['deviceName']][0]['sampling_rate']
        self.par['threshold'] = float(self.editThreshold.text())
        self.par['ipData'] = self.editIPDataServer.text()
        self.par['portData'] = int(self.editPortDataServer.text())
        self.par['ipOutput'] = self.editIPOutput.text()
        try:
            self.par['portOutput'] = int(self.editPortOutput.text())
        except:
            QMessageBox.warning(self, ('Output Port Is Error'), (""" Port should be integer """),
                                QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))
        self.par['isOnline'] = self.cbDataServer.isChecked()
        self.par['isOutput'] = self.cbOutput.isChecked()
        self.pbDataServer.setEnabled(True)
        self.pbOutput.setEnabled(True)
        self.pbStart.setText('Start')
        if not self._flag_stopTimer:
            self._timerplot.stop()
        self.initiation()

    def stop(self):
        if self.par['isOutput']:
            if self.pbOutput.text() == 'Connect':
                self.udpOutput = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.pbOutput.setText('Disconnect')
                print('Output connected.\n')
            elif self.pbOutput.text() == 'Disconnect':
                self.udpOutput.close()
                self.pbOutput.setText('Connect')
                print('Output disconnected.\n')
                del self.udpOutput




