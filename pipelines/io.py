import librosa
import numpy as np
import wavio

def load_audio(path, sampling = 44100, depth = 32):
    """
        Parameters:
        path (str): Path where the file will be stored.
        sampling (int): Sampling rate of the stream.
        depth (int): The limit values of the dynamic range (for 32bit the maximum value is 2.147.483.648 and minimum -2.147.483.648). 
    """    
    dtype = eval("np.float{}".format(depth))
    return librosa.load(path, sr = sampling, dtype = dtype)


def save_audio(path, array, sampling = 44100, sampling_width = 4):
    """
        Parameters:
        path (str): Path where to save the audio file.
        array (np.array of floats): Array to be saved.
        sampling (int): Sampling rate of the stream.
        sampling_width (int): Sampling width of the stream.
    """
    wavio.write(path, array, rate = sampling, sampwidth = sampling_width)
