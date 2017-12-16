#Code that deals with image manipulation and waveform generation. 
#Ryan, Ben, William

import numpy as np
import pyaudio
import math
from scipy import signal
from threading import Thread
import time

# Get array of notes (C-1 to G9 Equal temperament)
Notes = np.load("Notes.npy")
CONLEN = np.linspace(0, .3, 28800, endpoint=False)
CONLEN2 = np.linspace(0, .02, 1920, endpoint=False)
waves = []

# Called by CVAudio, takes in picture as array and uses pixel data to create waveforms
def picToAud(array):
    global waves
    p = pyaudio.PyAudio()
    
    size = len(array)
    while size % 3 != 0:
        array = np.append(array, [np.zeros(len(array[0]))])
        size = len(array)
    
    starts = [0, size//3, 2*size//3]
    proc = Thread(target = genWaveProc, args=(array[0:starts[1]],array[starts[1]:starts[2]],array[starts[2]:],))
    proc.start()
    time.sleep(2)
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=96000, output=True)
    for wave in waves:
        stream.write(wave.astype(np.int8))
    stream.stop_stream()
    stream.close()
    p.terminate()

    

# Wave generation with shorter waveforms
def genWaveRealtime(arr):
    v = 12
    n = Notes[int((arr[1]/640) * 128)]
    print(n)
    note = signal.square(2 * math.pi * n * CONLEN2)*v
    return note.astype(np.int16)

#main function that takes in values and makes waves
def genWave(arr):
        r = 0
        b = 0
        wave_data = np.array([])
        for y in arr:
            r = Notes[y[2] % 128]
            b = y[0] 
            note = signal.square(2 * math.pi * r * CONLEN) * b
            wave_data = np.append(wave_data, [note], axis=None)

        
        return wave_data.astype(np.int16)

#used by the thread to keep a buffer to play. Threading is needed due to the pi audio drivers breaking when input is lost. 
def genWaveProc(ar1, ar2, ar3):
    global waves
    start = 0
    for i in range(len(ar1)):
        while start < len(ar1[0]):
            wave1 = genWave(ar1[i][start:start+2])
            wave2 = genWave(ar2[i][start:start+2])
            wave3 = genWave(ar3[i][start:start+2])
            start += 2
            wave_data = sum([wave1, wave2, wave3])
            print(wave_data)
            waves.append(wave_data)
            
        
    


