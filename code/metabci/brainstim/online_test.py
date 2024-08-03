from scipy.signal import welch
from scipy import signal
import argparse
import logging
import numpy as np
import pyqtgraph as pg
import pickle
import pandas as pd
import time
from scipy import fftpack as fft
from scipy import signal
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from pyqtgraph.Qt import QtGui, QtCore
# import pip.pyplot as plt
from scipy.fftpack import fft, fftshift, ifft
from awarenessProcessor import  awarenessProcessor
from pyqtgraph.exporters import ImageExporter
from Offline_svm import train_threshold
import os
import sys
import serial.tools.list_ports
def detect_serial_port():
    """ Detect the current serial port being used. """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description:  # 根据需要调整匹配条件
            return port.device
    return None  # 如果未找到匹配的端口，则返回None或者其他适当的值

if hasattr(sys, '_MEIPASS'):
    dll_path = os.path.join(sys._MEIPASS, 'brainflow', 'lib')
    os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']
else:
    dll_path = os.path.join(os.path.dirname(__file__), 'brainflow', 'lib')
    os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']


np.set_printoptions(threshold=np.inf)
data_all = []
awareness = awarenessProcessor()
def save_result_to_txt(result, filename='output.txt'):
    # 打开文件并以写入模式打开
    with open(filename, 'w') as file:
        # 将结果写入文件
        file.write(str(result))
class Graph:

    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim   #将传入的 board_shim 赋值给类的属性，以便在类的其他方法中使用。
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)   #获取采集板的外部信号（例如，脑电信号）通道。
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)   #获取采集板的采样率。
        self.update_speed_ms = 25  #设置更新速度，单位是毫秒。
        self.updata_speed_ms_new= 250 #新的更新速度
        self.window_size = 4  #定义窗口大小，以秒为单位。
        self.num_points = self.window_size * self.sampling_rate   #计算要显示的数据点数，根据窗口大小和采样率确定。
        self.update_count = 0
        self.ratio2_history = []
        self.update_history = []
        self.max_update_history = 10
        self.threshold = 0.25
        train_threshold()
        # 加载分类器
        with open('svm_classifier.pkl', 'rb') as f:
            self.loaded_clf = pickle.load(f)
        self.app = QtGui.QApplication([])    #创建一个Qt应用程序实例
        self.win = pg.GraphicsWindow(title='BrainFlow Plot', size=(1200, 600))   #创建一个名为 'BrainFlow Plot' 的窗口，并设置大小为 800x600。这里使用了 pyqtgraph 库创建一个图形窗口。

        self._init_timeseries()  #调用类内部的 _init_timeseries 方法，可能是用于初始化时间序列数据显示的相关设置。
        self._init_awareness()
        self.order = 2  # 滤波阶数
        self.nyq = 0.5 * self.sampling_rate
        self.lowcut = 4  # 低通滤波频率
        self.highcut = 30  # 高通滤波频率
        self.low = self.lowcut / self.nyq
        self.high = self.highcut / self.nyq
        self.b, self.a = signal.butter(self.order, [self.low, self.high], btype='band')
        ###频段筛选
        self.freq_band_theta = (4, 7)
        self.freq_band_alpha = (8, 13)  # 希望提取的频段为8-12Hz
        self.freq_band_beta = (14, 30)
        # self._init_fft()###################
        self.channel_one = 1 # 第一个通道
        self.channel_two = 2 # 第二个通道
        self.N1 = 2
        self.N2 = 2
        self.n1 = 0
        self.n2 = 0
        timer = QtCore.QTimer()   #创建一个 Qt 定时器。
        timer.timeout.connect(self.update)   #将定时器的超时信号连接到类的 update 方法，表示每次定时器超时时都会调用 update 方法。
        timer.start(self.update_speed_ms)   #启动定时器，设置超时时间为 self.update_speed_ms，即更新速度。

        timer_new = QtCore.QTimer()  # 创建一个 Qt 定时器。
        timer_new.timeout.connect(self.update_new)  # 将定时器的超时信号连接到类的 update 方法，表示每次定时器超时时都会调用 update 方法。
        timer_new.start(self.updata_speed_ms_new)  # 启动定时器，设置超时时间为 self.update_speed_ms，即更新速度。
        QtGui.QApplication.instance().exec_()

    #界面的绘制，坐标设置
    def _init_timeseries(self):
        self.timeseries_plots = list()
        self.timeseries_curves = list()    #创建两个空列表，用于存储图形窗口和曲线对象。
        # for i in range(len(self.exg_channels)):  #通过循环遍历所有外部信号通道。
        for i in range(min(2, len(self.exg_channels))):
            p = self.win.addPlot(row=i, col=0)   #在图形窗口中添加一个绘图区域，将其放置在第 i 行、第 0 列。每个通道对应一个绘图区域。
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)        #隐藏左侧的坐标轴。
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)   #隐藏底部的坐标轴。
            if i == 0:
                p.setTitle('TimeSeries Plot')    #如果是第一个通道，设置图形窗口的标题为 'TimeSeries Plot'。
            self.timeseries_plots.append(p)     #将当前的绘图区域对象添加到 self.plots 列表中。
            curve = p.plot()    #在当前的绘图区域中创建一个曲线对象。
            self.timeseries_curves.append(curve)    #将当前的曲线对象添加到 self.curves 列表中。
    
    def _init_fft(self):################
        # self.fft_plot = self.win.addPlot(row=0, col=1, colspan=len(self.exg_channels))
        self.fft_plot = self.win.addPlot(row=0, col=1, rowspan=8)
        self.fft_plot.setTitle('Average Spectrum Plot')
        self.fft_curve = self.fft_plot.plot(pen='y')
        self.fft_plot.setLabel('bottom', 'Frequency', units='Hz')
        self.fft_plot.setXRange(0, 30)
        allowed_y_range = (0, 1000)
        self.fft_plot.setYRange(*allowed_y_range)

    def _init_awareness(self):
        self.awareness_plot = self.win.addPlot(row=0, col=1, rowspan=8)
        self.awareness_plot.setTitle('addPlot')
        self.awareness_plot.showAxis('left', True)
        self.awareness_plot.setMenuEnabled('left', False)
        self.awareness_plot.showAxis('bottom', True)
        self.awareness_plot.setMenuEnabled('bottom', False)
        self.curve = self.awareness_plot.plot(pen='g')
        self.awareness_plot.setYRange(0, 0.6)

    #更新数据
    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)

        # for count, channel in enumerate(self.exg_channels):   #循环遍历每个外部信号通道。
        for count, channel in enumerate(self.exg_channels[:2]):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)   #去趋势化操作，使用常数值进行去趋势化。这可以有助于移除信号中的基线漂移。
            #滤波
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 3.0, 45.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)    #对信号进行带通滤波，将频率限制在3.0 Hz到45.0 Hz之间。这有助于过滤掉不需要的频率成分。
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 2.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)    #对信号进行带阻滤波，移除在48.0 Hz到52.0 Hz和58.0 Hz到62.0 Hz范围内的频率成分。这可能是为了去除电源线干扰等特定频率的噪音。
            self.timeseries_curves[count].setData(data[channel].tolist())      #将经过处理的通道数据设置为相应曲线对象的数据，以更新图形界面上的曲线。


        self.app.processEvents()
    def process_arrays(self, arrays):
        power_values = []  # 新建一个数组来存储功率值
        filtered_data1 = signal.lfilter(self.b, self.a, arrays[0]) ###
        filtered_data2 = signal.lfilter(self.b, self.a, arrays[1])
        frequencies, power_spectrum1 = welch(filtered_data1, fs=250, nperseg=self.num_points)
        frequencies, power_spectrum2 = welch(filtered_data2, fs=250, nperseg=self.num_points)
        ###一通道
        band_power_theta1 = np.trapz(
                power_spectrum1[(frequencies >= self.freq_band_theta[0]) & (frequencies <= self.freq_band_theta[1])],
                frequencies[(frequencies >= self.freq_band_theta[0]) & (frequencies <= self.freq_band_theta[1])])
        band_power_alpha1 = np.trapz(
                power_spectrum1[(frequencies >= self.freq_band_alpha[0]) & (frequencies <= self.freq_band_alpha[1])],
                frequencies[(frequencies >= self.freq_band_alpha[0]) & (frequencies <= self.freq_band_alpha[1])])
        band_power_beta1 = np.trapz(
                power_spectrum1[(frequencies >= self.freq_band_beta[0]) & (frequencies <= self.freq_band_beta[1])],
                frequencies[(frequencies >= self.freq_band_beta[0]) & (frequencies <= self.freq_band_beta[1])])
        ###二通道
        band_power_theta2 = np.trapz(
                power_spectrum2[(frequencies >= self.freq_band_theta[0]) & (frequencies <= self.freq_band_theta[1])],
                frequencies[(frequencies >= self.freq_band_theta[0]) & (frequencies <= self.freq_band_theta[1])])
        band_power_alpha2 = np.trapz(
                power_spectrum2[(frequencies >= self.freq_band_alpha[0]) & (frequencies <= self.freq_band_alpha[1])],
                frequencies[(frequencies >= self.freq_band_alpha[0]) & (frequencies <= self.freq_band_alpha[1])])
        band_power_beta2 = np.trapz(
                power_spectrum2[(frequencies >= self.freq_band_beta[0]) & (frequencies <= self.freq_band_beta[1])],
                frequencies[(frequencies >= self.freq_band_beta[0]) & (frequencies <= self.freq_band_beta[1])])
        θ = (band_power_theta1 + band_power_theta2) / 2
        α = (band_power_alpha1 + band_power_alpha2) / 2
        β = (band_power_beta1 + band_power_beta2) / 2
        T = θ + α + β

        power_values.append(θ,α,β,θ/T,α/T,β/T,θ/α,θ/β,θ/α+β)
        power = np.array(power_values)
        predict_label = self.loaded_clf.predict(power)
        return predict_label # 将数组转换成NumPy数组并返回
    def update_new(self):
        data = self.board_shim.get_current_board_data(self.num_points)  # 通过调用 get_current_board_data 方法获取当前板上的数据，其中 self.num_points 是要获取的数据点数。
        data_all.append(data)
        ratio2 = awareness.process(data[[self.channel_one,self.channel_two], :])
        # self.loaded_clf.predict(data)
        predict_label = self.process_arrays(data[[self.channel_one,self.channel_two], :])
        print(predict_label[0])
        if predict_label[0] == 0: #不集中
            self.n1 += 1
            if self.n1 >= self.N1:
                result_value = 0  # 3为daotui
                save_result_to_txt(result_value, 'outputvideo.txt')
                # print('0')
                self.n1 = 0
                self.n2 = 0
            # print(result_value)
        else:     #集中
            self.n2 += 1
            if self.n2 >= self.N2:
                result_value = 1  # 2为前进
                save_result_to_txt(result_value, 'outputvideo.txt')
                self.n1 = 0
                self.n2 = 0

        self.update_count += 1
        self.update_history.append((self.update_count, ratio2))
        self.ratio2_history.append(ratio2)
        self.save_to_file('data_file.csv','online_data_EEG.csv')

        if len(self.update_history) > self.max_update_history:
            self.update_history.pop(0)


        x_values, y_values = zip(*self.update_history)
        self.curve.setData(x=x_values, y=y_values)

        self.app.processEvents()

    def save_to_file(self, file_name1, file_name2):
        # Create a two-dimensional matrix with index and ratio2 values
        data_to_save = np.vstack((np.arange(1, len(self.ratio2_history) + 1), self.ratio2_history))
        # Save the matrix to a CSV file
        np.savetxt(file_name1, data_to_save.T, fmt='%.18e', delimiter=',')
        # print(data_all)



def plot_video2():
    BoardShim.enable_dev_board_logger()
    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default='0')
    parser.add_argument('--file', type=str, help='file', required=False, default='0')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default='-1')
    parser.add_argument('--other-info', type=str, help='master board id needs to be recorded in this parameter when board id is STREAMING_BOARD or PLAYBACK_FILE_BOARD',
                    required=False, default='-1')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = detect_serial_port()
    # params.serial_port = "COM3"
    params.file = args.file
    params.other_info = args.other_info

    board = BoardShim(args.board_id, params)  #创建一个名为 board 的 BoardShim 对象，使用给定的 args.board_id 和 params 参数。
    try:
        board.prepare_session()  #准备数据采集会话。
        board.start_stream()   # 开始数据流。
        Graph(board)  #创建一个 Graph 对象
    except BaseException:
        logging.warning('Exception', exc_info=True)   #捕获任何异常，并使用 logging.warning 记录异常信息。
    finally:
        with open('online_data_EEG.pkl', 'wb') as f:
            pickle.dump(data_all, f)
        logging.info('End')
        if board.is_prepared():
            logging.info('Releasing session')
            board.release_session()


if __name__ == '__main__':
    plot_video2()