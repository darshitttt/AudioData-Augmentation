import scipy.io.wavfile as wav
import numpy as np
import time
import os
import librosa
import soundfile
import math
import random
import sys

# Directory where clean data, which is to be augmented is stored
dir = sys.argv[1]

# Generate subfolders for augmented data inside the Clean data directory
bgdir = dir + 'CD_AN/'
os.mkdir(bgdir)
irdir = dir + 'CD_IR/'
os.mkdir(irdir)
combdir = dir + 'CD_IR_AN/'
os.mkdir(combdir)

#Takes in 2 n-dimensional arrays, CD and RIR, and returns convolved signal
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


# Used to generate sound that is to be added to the original signal.
# Takes in CD as input, the AN and the desired SNR, and outputs the noise!
def get_noise_from_sound(signal,noise,SNR):

    RMS_s=math.sqrt(np.mean(signal**2))
    #required RMS of noise
    RMS_n=math.sqrt(RMS_s**2/(pow(10,SNR/10)))

    #current RMS of noise
    RMS_n_current=math.sqrt(np.mean(noise**2))
    noise=noise*(RMS_n/RMS_n_current)

    return noise


# Scenario list: Can be changed depending on the random number of RIR and AN combinations you have!
# For this code, we have three combinations/scenarios
choice_list = [0,1,2]

# Loop that iterates through all the files in the given directory
# It will randomly choose from the choice_list, and will apply the RIR and Bg_noise combination to it
for d in os.listdir(dir):
    dd = os.path.join(dir, d)

    # Paths to the IR files and Bg_noise files
    # If you add more files, and you need more options, please add it to this list, in the correct order
    ir = ['RIR/h041_TrainStation_SouthStationBoston_4txts.wav', 'RIR/h107_Supermerket_1txts.wav', 'RIR/h123_WineBar_1txts.wav']
    bg = ['Bg_sound/train2.wav', 'Bg_sound/supermarkt.wav', 'Bg_sound/restaurant2.wav']


    if os.path.isfile(dd):

        # Loads the CD signal
        signal, rate = librosa.load(dd)

        # Randomly choosing a scenario
        temp = random.randrange(3)
        print(temp, ir[temp], bg[temp])

        # Loading the IR signals based on the randomly chosen scenario
        ir, ir_rate = librosa.load(ir[temp])
        # Convolving CD signals with IR signals
        con_sig = convolve_ir(signal, ir)

        # Writing the convolved signals into a wav file in a folder inside the given directory
        # We also have an identifier as the first character of filename just to identify which scenario was randomly chosen for this particular file.
        # For example: 0_filename.wav where 0 is the randomly chosen scenario
        out_fn = irdir + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, con_sig)

        # Loading the BGnoise signals based on the randomly chosen scenario
        bg, bg_rate = librosa.load(bg[temp])
        #Generating noise given CD, and the AN file, with appropriate SNR
        bg_noise = get_noise_from_sound(signal, bg, SNR=10)
        # Adjusting the length of the generated noise according to the file length, so it can add up
        if len(bg_noise)>len(signal):
            bg_noise = bg_noise[0:len(signal)]

        # Adding up the generated noise to the CD file, and writing it in a different folder.
        # The nomenclature of the file is same as explaind above
        bg_sig = bg_noise + signal
        out_fn = bgdir + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, bg_sig)

        # Now we generate noise for the convolved signals and the AN files
        # The procedure is still the same, just the input signals have changed
        comb_noise = get_noise_from_sound(con_sig, bg, SNR=10)
        if len(comb_noise)>len(con_sig):
            comb_noise = comb_noise[0:len(con_sig)]
        n1n2 = comb_noise + con_sig
        out_fn = combdir + str(temp) + '_' + os.path.basename(dd)
        wav.write(out_fn, rate, n1n2)
