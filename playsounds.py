import numpy as np 
import sounddevice as sd
import soundfile as sf
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import sounddevice as sd


AUDIO_SAMPLE_RATE = 44100  # Hz



# generate a tone of the given duration (in seconds) at the given frequency
def gen_tone(amplitude,tone_duration, frequency):
    x = np.arange(AUDIO_SAMPLE_RATE * tone_duration)
    tone = amplitude*np.sin(2 * np.pi * frequency/AUDIO_SAMPLE_RATE * x)
    
    return tone


def play(tone):
    #scikits.audiolab.play(fs=AUDIO_SAMPLE_RATE)
    sd.play(tone, AUDIO_SAMPLE_RATE)
    sd.wait()
    sf.write('Tone.wav',tone, AUDIO_SAMPLE_RATE)

#fSK modulation 
def modulateFSK(list, tone1, tone2):
    sound = np.array([])
    for i in list:
        if i == 1:
            sound = np.append(sound, tone1)
        else:
            sound = np.append(sound, tone2)
    play(sound)


def main():
    tone1 = gen_tone(1,.0625, 900)
    tone2 = gen_tone(1,.0625, 300)
    
    while True:
        print("Please enter Message")
        array = [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]
        print(array)
        modulateFSK(array, tone1, tone2)
        message = input()

if __name__ == '__main__':
    main()