import scipy.io.wavfile as wav
import numpy as np
import time
import os
import librosa
import soundfile
import math
import random

dir = '/work/dpandya/LibriVox_Kaggle/meisterfloh/'

def convolve_ir(x, y):
    t0 = time.time()
    X = np.fft.fft(x, len(x)+len(y)-1)
    Y = np.fft.fft(y, len(x)+len(y)-1)
    Z = X * Y
    z = np.real(np.fft.ifft(Z))
    t1 = time.time()

    print ("Time for frequency-domain convolution: ", t1-t0)

    z = 0.5 * z / np.abs(np.max(z))
    return z



def get_noise_from_sound(signal,noise,SNR):

    RMS_s=math.sqrt(np.mean(signal**2))
    #required RMS of noise
    RMS_n=math.sqrt(RMS_s**2/(pow(10,SNR/10)))

    #current RMS of noise
    RMS_n_current=math.sqrt(np.mean(noise**2))
    noise=noise*(RMS_n/RMS_n_current)

    return noise


choice_list = [0,1,2]


for d in os.listdir(dir):
    dd = os.path.join(dir, d)
    ir = ['/work/dpandya/LibriVox_Kaggle/RIR/h041_TrainStation_SouthStationBoston_4txts.wav', '/work/dpandya/LibriVox_Kaggle/RIR/h107_Supermerket_1txts.wav', '/work/dpandya/LibriVox_Kaggle/RIR/h123_WineBar_1txts.wav']
    bg = ['/work/dpandya/LibriVox_Kaggle/BGnoise/train2.wav', '/work/dpandya/LibriVox_Kaggle/BGnoise/supermarkt.wav', '/work/dpandya/LibriVox_Kaggle/BGnoise/restaurant2.wav']


    if os.path.isfile(dd):

        signal, rate = librosa.load(dd)
        temp = random.randrange(3)
        print(temp, ir[temp], bg[temp])
        ir, ir_rate = librosa.load(ir[temp])
        con_sig = convolve_ir(signal, ir)
        out_fn = dir + 'ir_noise/' + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, con_sig)

        bg, bg_rate = librosa.load(bg[temp])
        bg_noise = get_noise_from_sound(signal, bg, SNR=10)
        if len(bg_noise)>len(signal):
            bg_noise = bg_noise[0:len(signal)]

        bg_sig = bg_noise + signal
        out_fn = dir + 'bg_noise/' + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, bg_sig)

        comb_noise = get_noise_from_sound(con_sig, bg, SNR=10)
        if len(comb_noise)>len(con_sig):
            comb_noise = comb_noise[0:len(con_sig)]
        n1n2 = comb_noise + con_sig
        out_fn = dir + 'n1n2/' + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, n1n2)
