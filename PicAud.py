import numpy as np
import pyaudio
import math
from scipy import signal

# Get array of notes (C-1 to G9 Equal temperament)
Notes = np.load("Notes.npy")
CONLEN = np.linspace(0, .0625, int(92000*.0625), endpoint=False)


# Called by CVAudio, takes in picture as array and uses pixel data to create waveforms
def picToAud(array):
    start = 0
    p = pyaudio.PyAudio()
    #array = np.random.randint(48, 61, (6, 300, 3))
    array = np.full((6, 300), 48)
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=92000, output=True)
    size = len(array)
    while size % 3 != 0:
        array = np.append(array, [np.zeros(len(array[0]))])
        size = len(array)
    starts = [0, size//3, 2*size//3]
    data1 = array[0:starts[1]]
    data2 = array[starts[1]:starts[2]]
    data3 = array[starts[2]:]
    end = starts[1]
    wave_data = []
    for i in range(len(data1)):
        while start < len(data1[0]):
            wave1 = genWave(data1[i][start:start+32])
            wave2 = genWave(data2[i][start:start+32])
            wave3 = genWave(data3[i][start:start+32])
            start += 32
            wave_data = sum([wave1, wave2, wave3])
            stream.write(wave_data.astype(np.int8))



    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()


def genWave(arr):
        r = 0
        b = 0
        i = 0
        wave_data = np.array([])
        for y in arr:
            print(i)
            r = Notes[y % 64]
            b = 60
            note = signal.square(2 * math.pi * r * CONLEN) * b
            wave_data = np.append(wave_data, [note], axis=None)
            i+=1
        return wave_data


picToAud([])