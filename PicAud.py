import numpy as np
import pyaudio
import math
from scipy import signal

# Get array of notes (C-1 to G9 Equal temperament)
Notes = np.load("Notes.npy")
CONLEN = np.linspace(0, .0625, int(92000*.0625), endpoint=False)


# Called by CVAudio, takes in picture as array and uses pixel data to create waveforms
def picToAud(array):
    i = 0
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=92000, output=True)
    size = len(array)
    while size % 3 != 0:
        array.append(np.zeros(len(array[0])))
        size = len(array)
    starts = [0, size//3, 2*size//3]
    end = starts[1]
    while i < end:
        wave1 = genWave(array[starts[0] + i])
        wave2 = genWave(array[starts[1] + i])
        wave3 = genWave(array[starts[2] + i])
        i += 1
        sum([wave1, wave2, wave3])
        stream.write(wave_data.astype(np.int8))



    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()


def genWave(arr):
        r = 0
        b = 0
        wave_data = []
        for y in arr:
            r = Notes[y[2] % 64]
            b = (y[0] / 3)

        wave_data = signal.square(2 * math.pi * r * CONLEN) * b

        return wave_data




