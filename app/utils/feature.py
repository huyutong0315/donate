import numpy as np
from scipy import fftpack
import math
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import cv2
#调制谱函数
def demon_amalysis(file_path, NFFT=500):
    x, fs = librosa.load(file_path)
    y_demon = abs(fftpack.hilbert(x))
    Y_demon = abs(fftpack.fft(y_demon, NFFT))/NFFT*2
    fftf = (fs/2*np.linspace(0,1,math.floor(NFFT/2)+1)).tolist()
    Y_demon = Y_demon[0: math.floor(NFFT/2)+1]
    Y_demon[0:10] = 0
    Y_demon = (Y_demon/np.max(Y_demon)).tolist()
    return fftf, Y_demon

#低频线谱函数
def nextpow2(n):
    return np.ceil(np.log2(np.abs(n))).astype('long')
def lofar_v1(file_path, nwin=882):
    xsignal, fs = librosa.load(file_path)
    wind = signal.kaiser(nwin, beta=18)
    nlap = np.floor(0.5*nwin)
    nfft = 2**nextpow2(nwin)
    f, t, lof = signal.stft(xsignal,window = wind,nperseg = nwin, noverlap = nlap, nfft=nfft, fs=fs)
    lof = abs(lof)
    [m, n] = lof.shape
    lof_n = (lof-np.min(lof,0))/(np.max(lof,0)-np.min(lof,0))
    for i in range(0, m):
        for j in range(1,n-1):
            y2 = lof_n[i, j+1] - lof_n[i, j]
            y3 = lof_n[i, j] - lof_n[i, j-1]
            if y2*y3<0:
                lof_n[i, j] = 0
            if (lof_n[i, j]<lof_n[i,j+1]) and (lof_n[i, j] < lof_n[i,j-1]):
                lof_n[i, j] = 0
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print("最高频率")
    print(f[len(f)-1] + (f[len(f)-1]-f[len(f)-2]))
    print("原始长度")
    l0 = 0
    for i in range(len(lof_n)):
        l0 += len(lof_n[i])
    print(l0)
    #原始图
    plt.figure()
    plt.title("原始图像 数据量：123120（5s）")
    plt.pcolormesh(t, f, lof_n)
    plt.show()
    #进行一次卷积
    fil = np.array([[1, 1, 1],  # 这个是设置的滤波，也就是卷积核
                    [1, 1, 1],
                    [1, 1, 1]])

    lof_n1 = cv2.filter2D(lof_n, -1, fil)
    plt.title("一次卷积图像 数据量：123120（5s）")
    plt.pcolormesh(t, f, lof_n1)
    plt.show()
    print("一次卷积长度")
    l1 = 0
    for i in range(len(lof_n1)):
        l1 += len(lof_n1[i])
    print(l1)
    #缩放参数确定：
    #目标数据 暂定8w
    N = l0
    n = 80000
    scale = N / n
    print(np.ceil(scale ** 0.5))
    scale = np.ceil(scale ** 0.5)
    #直接缩放
    lof_n2 = cv2.resize(lof_n, None, fx=1/scale, fy=1/scale)
    shape = lof_n2.shape
    print("n2Shape")
    print(shape)
    print(len(t))
    print(len(lof_n))
    list1 = []
    for i in range(shape[0]):
        list1.append(2*i)
    list2 = []
    for i in range(shape[1]):
        list2.append(2 * i)
    l2 = 0
    for i in range(len(lof_n2)):
        l2 += len(lof_n2[i])
    print("最终结果长度")
    print(l2)
    plt.title("线性插值缩放 数据量：30720（5s）")
    #这里好像做了个转置啥的，不太明白，或有bug
    plt.pcolormesh(list2, list1, lof_n2)
    plt.show()
    # return str(f.tolist()),str(t.tolist()),str(lof_n.tolist())
    return f.tolist(),t.tolist(),lof_n.tolist()

