import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def detect_bark(
    audio, sampling = 44100, freq_range = (1000, 2000),
    db_range = (0, 20), duration = (0.05, 0.3), 
    sensitivity = -26, clip = 15):
    """    
        Parameters (following the criteria on http://www.sciencepublishinggroup.com/journal/paperinfo?journalid=220&doi=10.11648/j.ijmea.20140201.14):
        audio (numpy array): Numpy array of the signal.
        sampling (int): Sampling rate of the stream.
        freq_range (tuple of ints): Range of frequencies for the dog bark. 
        db_range (tuple of ints): Range of bark sound level following.
        duration (tuple of floats): Standard duration of a bark.
        sensitivity (float): Microphone sensitivity (measured in dBFS).
        clip (float): The clip duration around audio to be saved.
    """
    times = np.arange(len(audio)) / sampling
    
    freqs, dbs = freqs_and_dbs(audio, sampling, sensitivity)
    time_regions = determine_time_regions(freqs, dbs, sampling, freq_range, db_range, duration)
    

def determine_time_regions(freqs, dbs, sampling, freq_range, db_range, duration):
    """
        Here we determine the number of regions where bark occurs.
    """
    freq_idxs = np.where((freqs >= freq_range[0]) & (freqs <= freq_range[1]))
    dbs_rel = dbs[freq_idxs]
    freq_bins, time_bins = np.where((dbs_rel >= db_range[0]) & (dbs_rel <= db_range[1]))    
    regions = []
    start_time = librosa.core.frames_to_time(time_bins[0], sr = sampling)
    # first_bin, frames = 0, []
    for idx, time_bin in enumerate(time_bins[:-1]):                
        if time_bins[idx + 1] - time_bin < 0:
            time = librosa.core.frames_to_time(time_bin, sr = sampling)
            diff = time - start_time
            # average_db = np.mean(dbs_rel[] >= 0)
            if diff >= duration[0] and diff <= duration[1]:
                regions.append((start_time, time)) #TODO: Not working
            start_time = librosa.core.frames_to_time(time_bins[idx + 1], sr = sampling)
    import ipdb; ipdb.set_trace()
    return np.vstack(regions)



def freqs_and_dbs(audio, sampling, sensitivity):
    """
        We calculate here the frequencies and dBs bins.
    """
    ffts = librosa.stft(audio)
    magnitude, phase = librosa.magphase(ffts)

    dbs = librosa.amplitude_to_db(magnitude, ref = sensitivity, top_db = None)

    # plt.figure(figsize = (14, 5))
    # librosa.display.specshow(dbs, sr = sampling, x_axis = "time", y_axis = "hz")
    # plt.colorbar()
    # plt.show()   

    # import ipdb; ipdb.set_trace() 

    freqs = librosa.display.__coord_fft_hz(ffts.shape[0], sr = sampling)
    return freqs, dbs