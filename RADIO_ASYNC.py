from __future__ import division
from rtlsdr import RtlSdr
import numpy as np  
import scipy.signal as signal
import scipy.io.wavfile as sio
import sounddevice as sd
import matplotlib  
import binascii
import itertools
import matplotlib.pyplot as plt

#import matlab.engine


sdr = RtlSdr(0)

F_station = int(89.2e6)   #Radio Disney  
F_offset = 250000         #Offset 
Fc = F_station - F_offset #center frequency  
Fs = int(1140000)         #Sample rate  1140000
N = int(8192000)          #Samples to capture  8192000
f_bw = 200000
n_taps = 64
audio_freq = 44100.0
tone_len = 0.125
filter_freq = 600
amp_thresh = 1.5  #1.5 on computer, 0.46 far away

#configure
sdr.sample_rate = Fs 
sdr.center_freq = Fc
sdr.gain = 'auto'

#Read samples
print('Starting Audio Stream')
samples = sdr.read_samples(N)
print('Ending Audio Stream')
#print(samples)

# Clean up
sdr.close()  
del(sdr)

#numpy array
x1 = np.array(samples).astype("complex64")

fc1 = np.exp(-1.0j*2.0*np.pi* F_offset/Fs*np.arange(len(x1)))
x2 = x1 * fc1

# Use Remez algorithm to design filter coefficients
lpf = signal.remez(n_taps, [0, f_bw, f_bw+(Fs/2-f_bw)/4, Fs/2], [1,0], Hz=Fs)  
x3 = signal.lfilter(lpf, 1.0, x2)

dec_rate = int(Fs / f_bw)  
x4 = x3[0::dec_rate]  
# Calculate the new sampling rate
Fs_y = Fs/dec_rate  

y5 = x4[1:] * np.conj(x4[:-1])  
x5 = np.angle(y5)

d = Fs_y * 75e-6   #Calculate the samples
x = np.exp(-1/d)   #decay 
b = [1-x]          #filter coefficients  
a = [1,-x]  
x6 = signal.lfilter(b,a,x5)

dec_audio = int(Fs_y/audio_freq)  
Fs_audio = Fs_y / dec_audio

x7 = signal.decimate(x6, dec_audio)

# Scale audio
#x7 *= 10000 / np.max(np.abs(x7))  
unfilt = x7;
sd.play(x7, audio_freq, blocking=True)

#butterworth filter
nyq = Fs_audio*.5
ws = filter_freq/nyq

b,a = signal.butter(6,ws, 'highpass')
tempf = signal.filtfilt(b,a,x7)

filt = np.convolve(abs(tempf), np.ones((50,))/50, mode='valid')
tempf = filt

data = []
tone_samples = 2828; #2618
print('before tone sample')

# Find beginning of audio clip - skip first 1000 samples


array = np.array(tempf)
# Binary Morphology of Bitstream
for i in range(len(tempf)):
    if array[i] >= amp_thresh:
        array[i] = 1
    elif array[i] >= amp_thresh * 0.175:
        array[i] = 0
    else:
        array[i] = -1


# Finding beginning of data stream, as well as period
findstart = True
findperiod = False
findend = False
startsample = 0
periodstart = 0
periodend = 0

it = np.nditer(array, flags=['f_index'])
while not it.finished:
    if findstart:
        if it.value == 1:
            startsample = int(it.index)
            findstart = False
            findperiod = True
    if findperiod:
        if it.value == 0:
            periodstart = int(it.index)
            findperiod = False
            findend = True
    if findend:
        if it.value == 1:
            periodend = int(it.index)
            findend = False
    it.iternext()

tone_samples = int((periodend - periodstart)/6)  # Period of one tone found above

print('Start: ' + str(periodstart) + '|End: ' + str(periodend) + '|Period: ' + str(tone_samples))

array = np.array(array[periodend+tone_samples+33:len(array)])  # Trims initial data
data = []

# Find bits using tone period above
for i in range(len(array)-tone_samples):
    if (np.remainder(i, tone_samples)) == 0:
        if array[i + int(tone_samples / 2)] != 1:
            data.append(0)
        else:
            data.append(1)

data = ''.join(format(x, '') for x in data)     # Concatenate Data Array
print('Encrypted Data Received: ' + data)
length = int(data[1:8], 2)                      # Length of Message
print('Length of Data: ' + str(length))
crc32 = int(data[9:40])                         # CRC Code of Message
print('CRC String:' + str(crc32))
data = data[40:40+length*8]

# Turn data string into list of decimal values
hex_data = []
for i in range(1, len(data), 8):
    hex_data.append(int(data[i:i+7], 2))
string_data_uu = ''.join(chr(i) for i in hex_data)
print('Encrypted Payload:   ' + string_data_uu)

key = [63, 94, 78, 114, 58, 73, 111, 119, 51, 99, 121, 25, 16, 62, 100, 85, 79, 38, 110, 27, 40, 2, 18, 57, 69, 61,
       86, 47, 76, 74, 67, 41, 54, 13, 81, 125, 50, 109, 84, 48, 44, 30, 55, 65, 89, 4, 59, 24, 118, 82, 66, 124,
       102, 83, 35, 91, 37, 12, 22, 39, 60, 7, 28, 122, 101, 75, 92, 77, 115, 72, 116, 90, 33, 97, 34, 3, 71, 32,
       53, 106, 8, 15, 36, 19, 68, 109, 70, 112, 49, 6, 10, 31, 113, 95, 103, 21, 117, 11, 127, 96, 29, 120, 50]
hex_data = [a ^ b for (a, b) in zip(bytes(hex_data), bytes(key))]


string_data = ''.join(chr(i) for i in hex_data)

print('Unencrypted Payload: ' + string_data)

fig = plt.figure()
plt.subplot(3, 1, 1)
plt.plot(array)
plt.title('Array')
plt.subplot(3, 1, 2)
plt.plot(filt)
plt.title('Butterworth Highpass' + r'$w_c = 600 Hz')
plt.subplot(3, 1, 3)
plt.plot(unfilt)
plt.title('Unfiltered Audio')
plt.show()




