import librosa
import numpy as np


def load_audio(path, sampling = 44100, depth = 32):
    """
        Parameters:
        path (str): Path where the file will be stored.
        sampling (int): Sampling rate of the stream.
        depth (int): The limit values of the dynamic range (for 32bit the maximum value is 2.147.483.648 and minimum -2.147.483.648). 
    """    
    dtype = eval("np.float{}".format(depth))
    return librosa.load(path, sr = sampling, dtype = dtype)