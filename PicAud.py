import numpy as np
import pyaudio
import math
import midiutil
from scipy import signal


count = 0
Notes = np.load("Notes.npy")


def picToAud(array):
    wave_data = ''
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=92000, output=True)

    for x in array:
        for y in x:
            r = getFreq((y[2] % 64) + 10)
            g = np.linspace(0, y[1] / 128, 92000, endpoint=False)

            b = (y[0] / 3)

            wave_data = signal.square(2 * math.pi * r * g) * b
            print(wave_data)


            stream.write(wave_data.astype(np.int8))
    stream.stop_stream()
    stream.close()
    p.terminate()





def getFreq(num):
    global Notes
    print(Notes[num])
    return Notes[num]
