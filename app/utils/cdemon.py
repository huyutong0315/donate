import numpy as np
from scipy import fftpack
import math
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal


# 调制谱类
class CDEMON():
    def __init__(self, fftn, datan, window, avgn, freqmax, bandfreq, fs, ds):
        self.FFTN = fftn
        self.DataN = datan
        self.AvgN = int(avgn)
        self.FreqMax = freqmax
        self.BandFreq = bandfreq
        self.Fs = fs
        self.BPP = 4
        self.DS = ds
        self.FreqIndexEnd = int(np.floor(self.FreqMax / self.Fs * ds * self.FFTN))
        self.FreqIndex = [i for i in range(1, int(self.FreqIndexEnd) + 1)]
        self.FreqN = int(self.FreqIndexEnd)
        self.FreqV = np.array([i for i in range(0, self.FreqIndexEnd)]) * self.Fs / ds / self.FFTN
        self.PSCache = np.zeros((self.FreqN * self.AvgN, self.DataN))
        self.Weight = np.ones((self.FFTN, 1))

    def process(self, InputData):

        BF_F = np.array(self.BandFreq) / self.Fs * 2
        BF_P = self.BPP
        b, a = signal.butter(BF_P, BF_F, 'bandpass')
        DataF = signal.filtfilt(b, a, InputData)

        DataF = DataF * DataF
        LF_F = self.FreqMax / self.Fs * 2
        LF_P = 4
        b, a = signal.butter(LF_P, LF_F, 'lowpass')
        DataF = signal.filtfilt(b, a, DataF)
        PS = np.zeros((self.FreqN, self.DataN))

        for i in range(0, self.DataN):
            # A = DataF*self.Weight
            A = DataF
            A = A - np.mean(A)
            B = fftpack.fft(A, self.FFTN)
            PS = np.array(abs(B[self.FreqIndex]))
        OutputData = np.zeros((self.FreqN, self.DataN))
        if (self.AvgN > 1):
            self.PSCache = np.append(PS, np.array(self.PSCache[1:(self.AvgN - 1) * self.FreqN + 1]))
            for i in range(0, self.DataN):
                A = np.reshape(self.PSCache[:], (self.FreqN, self.AvgN), order="F")
                OutputData = np.mean(A, 1)
                OutputData[0:2] = np.zeros((2))
        else:
            OutputData = PS
            OutputData[1:2] = np.zeros(2, self.DataN)
        return OutputData

def demon_amalysis1(Data,Fs):
    #Data,Fs = librosa.load(file_url)
    #Data = Data[Fs-1:]
    T = Data.shape[0]/Fs
    Datan=1
    window=1
    fs = Fs
    f_demon = 0.1
    N_d = Fs/f_demon
    T_d = 1/f_demon
    Nz_d = int(np.floor(T/T_d))
    avgn = 8
    fftn_d = int(N_d)
    freqmax = 50
    bandfreq = [2000,10000]
    ds = 1
    DMN = CDEMON(fftn_d,Datan,window,avgn,freqmax,bandfreq,fs,ds)
    OutputData2 = DMN.process(Data[0:fftn_d+1])
    return DMN.FreqV.tolist(), OutputData2.tolist()

# 调制谱更新版本，返回值DMN.FreqV为横坐标，OutputData_2 为纵坐标
def demon_amalysis_new(Data,Fs):
    #Data, Fs = librosa.load(file_url)
    # Data = Data[2 * Fs - 1:]
    T = Data.shape[0] / Fs
    Datan = 1
    window = 1
    fs = Fs
    f_demon = 0.1
    N_d = Fs / f_demon
    T_d = 1 / f_demon
    Nz_d = int(np.floor(T / T_d))
    avgn = 8
    fftn_d = int(N_d)
    freqmax = 50
    bandfreq = [2000, 10000]
    ds = 1
    DMN = CDEMON(fftn_d, Datan, window, avgn, freqmax, bandfreq, fs, ds)
    outputData2 = np.zeros((Nz_d, DMN.FreqN))
    for i in range(1, Nz_d + 1):
        outputData2 = DMN.process(Data[fftn_d * (i - 1) + 1:fftn_d * i + 1])
        # plt.plot(DMN.FreqV, outputData2)
        # plt.show()
    return DMN.FreqV.tolist(), outputData2.tolist()


def demon_amalysis_path_version(file_url, pred_flag=False):
    if pred_flag:
        Data, Fs = librosa.load(file_url, offset=0.0, duration=3)
    else:
        Data, Fs = librosa.load(file_url)
    #Data = Data[Fs-1:]
    T = Data.shape[0]/Fs
    Datan=1
    window=1
    fs = Fs
    f_demon = 0.1
    N_d = Fs/f_demon
    T_d = 1/f_demon
    Nz_d = int(np.floor(T/T_d))
    avgn = 8
    fftn_d = int(N_d)
    freqmax = 50
    bandfreq = [2000,10000]
    ds = 1
    DMN = CDEMON(fftn_d,Datan,window,avgn,freqmax,bandfreq,fs,ds)
    OutputData2 = DMN.process(Data[0:fftn_d+1])
    return DMN.FreqV,OutputData2