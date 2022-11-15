from io import BytesIO

import PIL
import numpy as np
import librosa.display
# import paddlex as pdx
import cv2
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import PIL.Image as Image
import librosa
import librosa.display
import os
import tensorflow as tf
from tensorflow.python.keras import models
from tensorflow.python.keras.applications.vgg16 import VGG16

from app.utils.cdemon import demon_amalysis_path_version


def Audio_classification(file_url):
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))

    parent_path = os.path.dirname(__file__)
    model_path = parent_path + "/MFCC_CNN_model.h5"
    model = models.load_model(model_path)
    music, sr = librosa.load(file_url, duration=2.97)
    mel_spect = librosa.feature.melspectrogram(y=music, sr=sr, n_mels=128)
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    librosa.display.specshow(mel_spect, y_axis='mel', fmax=8000, x_axis='time');
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.axis('off')
    plt.xticks([]), plt.yticks([])
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='jpg')
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize(size=(150, 150))
    data = np.asarray(dataPIL)
    data = data / 255
    feature = conv_base.predict(data[np.newaxis, :, :, :])
    buffer_.close()
    feature = np.reshape(feature, (1, 4 * 4 * 512))
    out = model.predict(feature)
    if (out[0][0] <= 0.5):
        return 'MerchantMarine', round(1 - out[0][0], 4)
    else:
        return 'FishingBoat', round(out[0][0], 4)


def Frequency_domain(file_url, f_sampling):
    music, sr = librosa.load(file_url)
    time = librosa.get_duration(filename=file_url)
    music_mean = np.mean(music)
    music = music - music_mean
    fs = sr
    num_sampling = sr // f_sampling
    f, t, zxx = signal.stft(music, nperseg=num_sampling, noverlap=num_sampling // 2)
    zxx = (abs(zxx)).tolist()
    time_x = (time * np.linspace(0, 1, len(t))).tolist()
    fre_y = (sr / 2 * np.linspace(0, 1, len(f))).tolist()
    return dict(zxx=zxx, time_x=time_x, fre_y=fre_y)


def Lofar_classification(video_path):
    conv_base = VGG16(weights='imagenet',
                 include_top=False,
                 input_shape=(150, 150, 3))
    parent_path = os.path.dirname(__file__)
    model_path = parent_path + "/Lofar_CNN_model.h5"
    model = models.load_model(model_path)
    f,t,lof_n = lofar_v1(video_path, 882)
    plt.pcolormesh(t,f,lof_n)
    plt.axis('off')
    plt.xticks([]),plt.yticks([])
    buffer_ = BytesIO()
    plt.savefig(buffer_,format = 'jpg')
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize(size = (150,150))
    data = np.asarray(dataPIL)
    data = data/255
    feature = conv_base.predict(data[np.newaxis,:,:,:])
    buffer_.close()
    feature = np.reshape(feature, (1, 4 * 4 * 512))
    out = model.predict(feature)
    if(out[0][0]>=0.5):
        return 'MerchantMarine',round(out[0][0],4)
    else:
        return 'FishingBoat',round(1-out[0][0],4)

#低频线谱函数
def nextpow2(n):
    return np.ceil(np.log2(np.abs(n))).astype('long')
def lofar_v1(file_path, nwin=882):
    xsignal, fs = librosa.load(file_path, duration=2.97)
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
    return f,t,lof_n


def bi_lstm_process_single(data_path):
    """
    利用双向LSTM模型对单一音频进行预测
    :param data_path:音频文件路径
    :return:(cls, score) cls:MerchantMarine/FishingBoat
    """
    parent_path = os.path.dirname(__file__)
    # model = pdx.deploy.Predictor(parent_path + '/P0004-T0006_export_model/inference_model', use_gpu=False)
    model_path = parent_path + "/lstm.h5"
    print(model_path)
    ship_dict = {0: "MerchantMarine", 1: "FishingBoat"}
    librosa_audio_data, librosa_sample_rate = librosa.load(data_path, offset=0.0, duration=3)  # 仅截取3秒，offset控制起始位置
    mfcc_data = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)  # (40,130)
    x_data = mfcc_data.reshape(1, mfcc_data.shape[0] * mfcc_data.shape[1])  # (1,5200)
    print(x_data.shape)
    x_data = x_data.reshape(x_data.shape[0], 1, x_data.shape[1])  # (1,1,5200)
    print(x_data.shape)
    model = tf.keras.models.load_model(model_path)
    result = model.predict(x_data)
    one_hot = result[0]
    print(one_hot)  # 商船(1,0) 渔船(0,1)
    return ship_dict[int(np.argmax(np.array(one_hot)))], np.max(np.array(one_hot))


def bi_lstm_dms_predict(data_path):
    """
    根据音频调制谱特征预测类别
    :return:
    """
    parent_path = os.path.dirname(__file__)
    # model = pdx.deploy.Predictor(parent_path + '/P0004-T0006_export_model/inference_model', use_gpu=False)
    model_path = parent_path + "/lstm_dms_0.9195402.h5"
    ship_dict = {0: "MerchantMarine", 1: "FishingBoat"}

    dms_freq, dms_amp = demon_amalysis_path_version(data_path, pred_flag=True)
    x_data = dms_amp.reshape(1, len(dms_amp))  # (1,500)
    print(x_data.shape)
    x_data = x_data.reshape(x_data.shape[0], 1, x_data.shape[1])  # (1,1,500)
    print(x_data.shape)
    model = tf.keras.models.load_model(model_path)
    result = model.predict(x_data)
    one_hot = result[0]
    print(one_hot)  # 商船(1,0) 渔船(0,1)
    return ship_dict[int(np.argmax(np.array(one_hot)))], np.max(np.array(one_hot))