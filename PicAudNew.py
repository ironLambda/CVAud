import numpy as np
import pyaudio
import math
from scipy import signal

# Get array of notes (C-1 to G9 Equal temperament)
Notes = np.load("Notes.npy")


# Called by CVAudio, takes in picture as array and uses pixel data to create waveforms
def picToAud(array):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=92000, output=True)

    for x in array:
        for y in x:
            # The red value of the pixel is used to control the frequency, the green controls the length, and the blue
            # is used to control the volume of the note
            r = getFreq((y[2] % 64))
            g = np.linspace(0, y[1] / 128, 92000, endpoint=False)
            b = (y[0] / 3)
            # Note: openCV returns pixel data in the order of blue green red

            # Generate wave
            wave_data = signal.square(2 * math.pi * r * g) * b

            # Write to pyaudio stream
            stream.write(wave_data.astype(np.int8))

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()


# Function that gets frequency value from array of frequencies, index of frequency is corresponding midi note
def getFreq(num):
    return Notes[num]

def noteTest(frequency):
	l = np.linspace(0, 2, 384000, endpoint=False)
	wave_data = signal.square(2 * math.pi * frequency * l)
	return(wave_data)

def playNotes():
	wave_data = sum([noteTest(523.25113060119), noteTest(659.25511382575), noteTest(783.99087196355)])
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=192000, output=True)
	stream.write(wave_data.astype(np.int8))

playNotes()
