import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import statistics
import pickle
from scipy.stats import norm
import numpy as np
from scipy.signal import welch
from scipy import signal
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import matplotlib.pyplot as plt

# from test2 import VideoPlayer


class awarenessProcessor():
    def __init__(self, srate=250, freqNotch=50, threshold=0.35, Qualityfactor=20,
                 group_size=4500, zhuanhua=0, chixu=1000, yaoya=750, start_index=250):
        self.srate = srate
        # self.numloop = 50
        self.freqNotch = freqNotch
        self._reSrate = 250
        self.Qualityfactor = Qualityfactor
        self.preprocessFilterCoef = dict(b=[], a=[])
        self.group_size = group_size
        self.zhuanhua = zhuanhua
        self.chixu = chixu
        self.yaoya = yaoya
        self.start_index = start_index
        # self.baselineBuffer = list(np.ones(3)*threshold)
        self.awareOutput = 4.5
        self.lowcut = 4  # 低通滤波频率
        self.highcut = 30  # 高通滤波频率
        self.fs = 250  # 采样频率
        self.order = 2  # 滤波阶数
        self.nyq = 0.5 * self.fs
        self.low = self.lowcut / self.nyq
        self.high = self.highcut / self.nyq
        self.b, self.a = signal.butter(self.order, [self.low, self.high], btype='band')
        ###频段筛选
        self.freq_band_theta = (4, 7)
        self.freq_band_alpha = (8, 13)  # 希望提取的频段为8-12Hz
        self.freq_band_beta = (14, 30)
        ####划分数据段
        self.group_size = 4500
        self.chixu = 2500
        self.yaoya = 750
        self.start_index = 250

    def dataacquisition(self):  # 数据获取函数，打开txt文件，并读取所有内容
        data_EEG = np.load('data_EEG.npy')
        data_EEG = data_EEG[[1, 2], :]
        data_attention = []
        data_noattention = []
        shape = data_EEG.shape
        numloop = int(shape[1] / 9000)

        for i in range(numloop * 2):
            star_idx = i * 4500
            end_idx = (i + 1) * 4500
            loop_data = data_EEG[:, star_idx:end_idx]
            loop_data = np.delete(loop_data, np.s_[:1000], axis=1)
            loop_data = np.delete(loop_data, np.s_[3000:3500], axis=1)
            split_arr = np.split(loop_data, 3, axis=1)
            # 重新调整形状为（3，2，1000）
            data_split = np.stack(split_arr, axis=0)
            if i % 2 == 0:
                data_attention.append(data_split)
            else:
                data_noattention.append(data_split)

        return data_attention[0], data_noattention[0]
    def process_arrays(self, all_arrays):
        power_values = []  # 新建一个数组来存储功率值
        for single_array in all_arrays:
            filtered_data1 = signal.lfilter(self.b, self.a, single_array[0]) ###
            filtered_data2 = signal.lfilter(self.b, self.a, single_array[1])
            frequencies, power_spectrum1 = welch(filtered_data1, fs=250, nperseg=1000)
            frequencies, power_spectrum2 = welch(filtered_data2, fs=250, nperseg=1000)
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

            # print("theta频段的功率为：", (band_power_theta1+band_power_theta2)/2, '\n'
            #       "alpha频段的功率为：", (band_power_alpha1+band_power_alpha2)/2,'\n'
            #       "beta频段的功率为：", (band_power_beta1+band_power_beta2)/2, '\n'
            #       "专注度",(band_power_beta1+band_power_beta2) / (band_power_alpha1+band_power_alpha2+band_power_theta1+band_power_theta2))

            power_values.append([
                (band_power_theta1 + band_power_theta2) / 2,
                (band_power_alpha1 + band_power_alpha2) / 2,
                (band_power_beta1 + band_power_beta2) / 2,])
            power = np.array(power_values)
        return power  # 将数组转换成NumPy数组并返回
    # def change(self, array_2d, dim1=50, dim2=1, dim3=3):
    #     # 将二维数组转换为三维数组
    #     array_3d = array_2d[:, np.newaxis, :]
    #     # array_3d = np.array(array_2d).reshape(dim1, dim2, dim3)
    #     return array_3d
    def classifier(self, eigenvalue_3d):
        # 取得特征
        iris_X = eigenvalue_3d
        # 取得标签
        label = np.zeros(iris_X.shape[0])
        half = iris_X.shape[0] // 2  # 数组的一半长度

        label[:half] = 1

        # 进行数据集划分
        # X_train, X_test, y_train, y_test = train_test_split(iris_X, label, test_size=0.2,random_state=0)
        # 利用K聚类算法进行分类

        clf = svm.SVC(gamma='scale', C=70, decision_function_shape='ovr', kernel='rbf')
        clf.fit(iris_X, label)
        print(iris_X)
        with open('svm_classifier.pkl', 'wb') as f:
            pickle.dump(clf, f)
        # 加载分类器
        # with open('svm_classifier.pkl', 'rb') as f:
        #     loaded_clf = pickle.load(f)

        # 使用加载的分类器进行预测
        # result = loaded_clf.predict(X_test)
        # # knn = KNeighborsClassifier()
        # # knn.fit(X_train, y_train)
        # # number_right = y_test-knn.predict(X_test)
        # num_right=y_test-(clf.predict(X_test))
        # count_of_zeros = np.sum(num_right == 0)
        # count_of_all = len(num_right)
        # print(y_test)
        # print(clf.predict(X_test))
        # print(num_right)
        # print("分类准确率=",count_of_zeros/count_of_all)

def train_threshold():
    # 创建awarenessProcessor实例
    awareness = awarenessProcessor()
    # 获取数据

    data_attention, data_noattention = awareness.dataacquisition()
    data_all = np.concatenate((data_attention, data_noattention), axis=0)
    eigenvalue = awareness.process_arrays(data_all)
    # eigenvalue_3d = awareness.change(eigenvalue)
    awareness.classifier(eigenvalue)




if __name__ == "__main__":
    train_threshold()