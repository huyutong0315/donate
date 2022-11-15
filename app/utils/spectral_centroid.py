import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import math
import scipy.signal as signal
import cv2
from scipy.fftpack import fft, fftshift, ifft
from scipy.stats import pearsonr
#谱质心
def spectral_centroid(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x))
    length = len(x)
    freqs = np.abs(np.fft.fftfreq(length, 1.0/samplerate)[:length//2+1])
    return np.sum(magnitudes*freqs) / np.sum(magnitudes)
#谱质心带宽
def spectral_centroid_width(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x)) # magnitudes of positive frequencies
    length = len(x)
    freqs = np.abs(np.fft.fftfreq(length, 1.0/samplerate)[:length//2+1]) # positive frequencies
    centroid=np.sum(magnitudes*freqs) / np.sum(magnitudes) # return weighted mean
    i =int(centroid//(freqs[1]-freqs[0]))
    return np.sum(magnitudes[i+1:freqs.shape[0]]*freqs[i+1:freqs.shape[0]]) / np.sum(magnitudes[i+1:freqs.shape[0]])-np.sum(magnitudes[0:i+1]*freqs[0:i+1]) / np.sum(magnitudes[0:i+1])
#谱包络面积
def spectral_area(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x))
    length = len(x)
    freqs = np.abs(np.fft.fftfreq(length, 1.0/samplerate)[:length//2+1])
    energy=np.sum(magnitudes) *(freqs[1]-freqs[0])
    return energy
#谱斜率
def spectral_slope(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x))
    N = len(magnitudes)
    length = len(x)
    freqs = np.abs(np.fft.fftfreq(length, 1.0/samplerate)[:length//2+1])
    En_num = np.sum(magnitudes)
    fn_num = np.sum(freqs)
    Enfn_num = np.sum(magnitudes*freqs)
    fn2_num = np.sum(freqs*freqs)
    spectral_slope = (N*Enfn_num - En_num*fn_num)/((N*fn2_num - fn_num*fn_num)*En_num)
    return spectral_slope
#谱下降图
def spectral_decline(x, samplerate=44100):
    # E(n)
    magnitudes = np.abs(np.fft.rfft(x))
    #下降值是一种描述谱倾斜程度的量值，是指功率谱累积幅度在X%（X一般取位0.85或0.6）以下的频率值
    X = 0.8
    length = len(x)
    freqs = np.abs(np.fft.fftfreq(length, 1.0 / samplerate)[:length // 2 + 1])
    return X*np.sum(magnitudes)
#谱不规律性 Irregularity
def spectral_Irregularity(x, samplerate=44100):
    # E(n)
    magnitudes = np.abs(np.fft.rfft(x))
    #magnitudes = np.array([1,2,3,4])
    length = len(magnitudes)
    i=1
    result = 0
    while i<length:
        A=magnitudes[i]-magnitudes[i-1]
        A = pow(A,2)
        result = result+A
        i=i+1
    arr = np.sum(magnitudes**2)
    return result/arr
#谱不平整性Uneven
def spectral_Uneven(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x))
    a = np.array([-1,2,3,-4])
    N = len(magnitudes)
    arr1=np.power(abs(magnitudes),1/N)
    T1=np.prod(arr1)
    T2=np.sum(abs(magnitudes))/N
    result=10*math.log10(T1/T2)
    return result
#谱熵
def spectral_entropy(x, samplerate=44100):
    magnitudes = np.abs(np.fft.rfft(x))
    T1=np.sum(magnitudes)
    i=0
    result=0
    while i<len(magnitudes):
        result=result+(magnitudes[i]/T1)*(math.log(magnitudes[i]/T1))
        i=i+1
    return -result

def Frequency_domain(music,sr,time,f_sampling):
    music_mean = np.mean(music)
    music = music - music_mean
    fs = sr
    num_sampling = sr // f_sampling
    f, t, zxx = signal.stft(music, nperseg=num_sampling, noverlap=num_sampling // 2)
    zxx = abs(zxx)
    # zxx = librosa.power_to_db(zxx ** 2)
    zxx = librosa.power_to_db(zxx ** 2, ref=np.max)
    bxx = np.around(zxx, decimals=0, out=None)
    time_x = time * np.linspace(0, 1, len(t))
    fre_y = sr / 2 * np.linspace(0, 1, len(f))
    plt.pcolormesh(time_x, fre_y, bxx)
    # plt.show()
    #大于80000
    zip = False
    l0 = 0
    for i in range(len(zxx)):
        l0 += len(zxx[i])
    if l0>80000:
        # 缩放参数确定：
        # 目标数据 暂定8w
        N = l0
        n = 80000
        scale = N / n
        scale = np.ceil(scale ** 0.5)
        bxx = cv2.resize(bxx, None, fx=1 / scale, fy=1 / scale)
        shape = bxx.shape
        list1 = []
        for i in range(shape[0]):
            list1.append(scale * i)

        list2 = []
        for i in range(shape[1]):
            list2.append(scale * i)
        # f = np.array(list2)
        # t = np.array(list1)
        max_f = fre_y[len(fre_y)-1]
        max_t = time_x[len(time_x)-1]

        f = np.linspace(0,max_f,shape[0])
        t = np.linspace(0,max_t,shape[1])
        plt.pcolormesh(t, f, bxx)
        # plt.show()
        zip = True
        l0 = 0
        for i in range(len(bxx)):
            l0 += len(bxx[i])
    return bxx, t, f, zip

def pccsdata(zxx):
    Frames_data = np.transpose(zxx)
    pccsdata = []
    for i in range(len(Frames_data)-1):
        pccs = pearsonr(Frames_data[i], Frames_data[i+1])
        pccs = pccs[0]
        if np.isnan(pccs):
            pccsdata.append(1.0)
        else:
            pccsdata.append(pccs)
    return pccsdata
#动态支持
def clip_time(y,time,t):

    print(time)
    div = time // t
    mod = time % t
    if mod!=0.0:
        div+=1
    list = []
    list.append(y)
    length = len(y)
    n = int(div)
    for i in range(n):
        one_list = y[math.floor(i / n * length):math.floor((i + 1) / n * length)]
        list.append(one_list)
    return list

def clip_time_new(y,time,t,type):
    if type == 2:
        print("2222222")
        print("Mel_Spectrogram_type")
        grip = 5
        every_time2frame = len(y) / time
        print(every_time2frame)
        datalist = []
        timelist = []
        timelist.append([0, time])
        datalist.append(y)
        for i in range(math.floor(time/grip)):
            if (i*grip * every_time2frame + t * every_time2frame) > len(y):
                one_list = y[math.floor(i*grip * every_time2frame):len(y) - 1]
                pertime_list = [i*grip, math.floor(time)]
                datalist.append(one_list)
                timelist.append(pertime_list)
                break
            one_list = y[math.floor(i*grip * every_time2frame):math.floor(i*grip * every_time2frame + t * every_time2frame)]
            pertime_list = [i*grip, i*grip + t]
            datalist.append(one_list)
            timelist.append(pertime_list)

        return datalist, timelist

    print(time/t)
    datarange = math.floor(time/t)
    datarange += 1
    every_time2frame = len(y)/time
    print(every_time2frame)
    datalist = []
    timelist = []
    timelist.append([0, time])
    timegrip = []
    timegrip.append(t/len(y))
    datalist.append(y)
    # for i in range(datarange):
    for i in range(math.floor(time)):
        if (i*every_time2frame + t*every_time2frame) > len(y):
            one_list = y[math.floor(i*every_time2frame):len(y)-1]
            pertime_list = [i, math.floor(time)]
            pertimegrip = t / len(one_list)
            datalist.append(one_list)
            timelist.append(pertime_list)
            timegrip.append(pertimegrip)
            break
        one_list = y[math.floor(i*every_time2frame):math.floor(i*every_time2frame + t*every_time2frame)]
        pertime_list = [i, i+t]
        pertimegrip = t/len(one_list)
        datalist.append(one_list)
        timelist.append(pertime_list)
        timegrip.append(pertimegrip)
    if type == 1:
        print("1111111")
        return datalist, timelist
    print("00000000")
    return datalist

def one_three(music,f_one_third):
    num_fft = 25000
    # 快速傅里叶变换
    Y = fft(music, num_fft)
    Y = np.abs(Y)
    # 确定频率上下限
    fsAll = []
    for num in range(0, len(f_one_third)):
        fs = f_one_third[num]
        fs_low = fs / math.pow(2, 1 / 6)
        fs_hight = fs * math.pow(2, 1 / 6)
        fsAll.append(fs)
        fsAll.append(fs_low)
        fsAll.append(fs_hight)
    fsAll_p = []
    print(fsAll)
    for num in range(0, len(f_one_third)):
        n = fsAll.index(f_one_third[num])
        start = int(fsAll[n + 1])
        end = int(fsAll[n + 2])

        sum_pow2 = 0
        for num1 in range(start, end):
            sum_pow2 = math.pow(Y[num1], 2) + sum_pow2
        fsAll_p.append(sum_pow2 / num_fft)
    print(fsAll_p)
    # y轴数据
    fsAll_p = 20 * np.log10(fsAll_p)
    fsAll_p1 = []
    where_are_inf = np.isinf(fsAll_p)
    for i in range(len(fsAll_p)):
        if where_are_inf[i] == True:
            fsAll_p1.append(-99999)
        if where_are_inf[i] == False:
            fsAll_p1.append(fsAll_p[i])
    res = (f_one_third, fsAll_p1)
    return res