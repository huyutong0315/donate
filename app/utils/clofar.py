import numpy as np
from scipy import fftpack
import math
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import cv2

class CLOFAR():
    def __init__(self, fftn, datan, window, avgn, freq, fs):
        self.FFTN = int(fftn)
        self.DataN = datan
        self.AvgN = int(avgn)
        self.Freq = freq
        self.Fs = fs
        self.FreqIndex = [int(np.floor(self.Freq[i] / self.Fs * self.FFTN)) for i in range(0, len(self.Freq))]
        self.FreqN = int(self.FreqIndex[1] - self.FreqIndex[0] + 1)
        self.FreqV = [i for i in range(int(self.FreqIndex[0]), int(self.FreqIndex[1] + 1))]
        self.PSCache = np.zeros((self.FreqN * self.AvgN, self.DataN))
        self.Weight = np.ones((self.FFTN, 1))

    def process(self, InputData):
        PS = np.zeros((self.FreqN, self.DataN))
        for i in range(0, self.DataN):
            A = InputData
            B = fftpack.fft(A, self.FFTN)
            PS = np.array(abs(B[self.FreqV] * B[self.FreqV].conjugate()))
            # print(PS)
        OutputData = np.zeros((self.FreqN, self.DataN))
        self.PSCache = np.append(PS, np.array(self.PSCache[1:(self.AvgN - 1) * self.FreqN + 1]))
        for i in range(0, self.DataN):
            A = np.reshape(self.PSCache, (self.FreqN, self.AvgN), order="F")

            OutputData = np.mean(A, 1)
            # print(OutputData)
        return OutputData


def lofar_v1_new(Data, Fs):
    # Data, Fs = librosa.load(file_url)
    T = Data.shape[0] / Fs
    f_lofar = 1
    N_l = int(Fs / f_lofar)
    T_l = 1 / f_lofar
    Nz_l = int(np.floor(T / T_l))
    fftn_l = N_l
    Datan = 1
    window = 1
    avgn = 8
    freq = [10, 1000]
    fs = Fs
    LFR = CLOFAR(fftn_l, Datan, window, avgn, freq, fs)
    fk = np.linspace(freq[0], freq[1], int((freq[1] - freq[0] + 1) / f_lofar), dtype=int)
    y_l = [i for i in range(1, Nz_l + 1)]
    OutputData1 = np.zeros((Nz_l, len(fk)))
    for i in range(0, Nz_l):
        OutputData_1 = LFR.process(Data[fftn_l * (i) + 1:fftn_l * (i + 1)])
        OutputData1[Nz_l - i - 1, :] = OutputData_1
    plt.pcolormesh(fk, y_l, OutputData1)
    # plt.show()
    zip = False
    #超过8w开始返回压缩数据
    l0 = 0
    for i in range(len(OutputData1)):
        l0 += len(OutputData1[i])
    if l0>80000:
        # 缩放参数确定：
        # 目标数据 暂定8w
        N = l0
        n = 80000
        scale = N / n
        print(np.ceil(scale ** 0.5))
        scale = np.ceil(scale ** 0.5)
        OutputData1 = cv2.resize(OutputData1, None, fx=1 / scale, fy=1 / scale)
        shape = OutputData1.shape
        print(shape)
        list1 = []
        for i in range(shape[0]):
            list1.append(scale * i)

        list2 = []
        for i in range(shape[1]):
            list2.append(scale * i)
        fk = np.array(list2)
        y_l = list1
        plt.pcolormesh(fk, y_l, OutputData1)
        # plt.show()
        zip = True
    return fk.tolist(), y_l, OutputData1.tolist(), zip
