from sklearn.preprocessing import minmax_scale

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def detect_bark_howl(
    audio, sampling = 44100, freq_range = (1000, 2000),
    db_range = (90, 140), duration = [0.08, 0.16, 0.32], 
    sensitivity = -26, clip = 15, silence_before = 1):
    """    
        Parameters (following the criteria on http://www.sciencepublishinggroup.com/journal/paperinfo?journalid=220&doi=10.11648/j.ijmea.20140201.14):
        audio (numpy array): Numpy array of the signal.
        sampling (int): Sampling rate of the stream.
        freq_range (tuple of ints): Range of frequencies for the dog bark. 
        db_range (tuple of ints): Range of bark sound level following.
        duration (list of floats): Typical durations (in seconds) of barks to create grid searches.
        sensitivity (float): Microphone sensitivity (measured in dBFS).
        clip (float): The clip duration around audio to be saved.
        silence_before (float): Silence time before clipped audio.
    """
    times = np.arange(len(audio)) / sampling

    centroids, freq_bins, dbs = freqs_and_dbs(audio, sampling, sensitivity)
    time_regions = determine_time_regions(centroids, freq_bins, dbs, 
                            sampling, freq_range, db_range, duration)
    if np.any(time_regions):
        min_time = time_regions[0, 0] - silence_before
        idxs = np.where((times >= min_time) & (times <= min_time + clip))
        return True, audio[idxs]
    else:
        return False, None


def determine_time_regions(centroids, freq_bins, dbs, sampling, 
                            freq_range, db_range, duration):
    """
        Here we determine the number of regions where bark occurs.
    """
    freq_idxs = np.where((freq_bins >= freq_range[0]) & (freq_bins <= freq_range[1]))
    dbs_rel = dbs[freq_idxs]
    dbs_averaged = np.mean(dbs_rel, axis = 0)    
    
    center_idx = int(len(duration) / 2)
    for idx, grid in enumerate(duration):
        cur_regions = find_regions(centroids, dbs_averaged, sampling, 
                                freq_range, db_range, grid)            
        if idx >= int(len(duration) / 2):
            if len(cur_regions) >= 5:
                return cur_regions  
            elif len(previous_regions) >= 5:
                return previous_regions            
        previous_regions = cur_regions
    return     


def find_regions(centroids, dbs, sampling, freq_range, db_range, w_size):
    """
        Find the regions where barks potentially occur.
    """
    t_centroids = librosa.frames_to_time(range(len(centroids)), sr = sampling)
    time_step = t_centroids[1] - t_centroids[0]
    bins = int(w_size / time_step)
    regions = []
    t_centroids = t_centroids[::bins]
    for idx, time in enumerate(t_centroids[:-1]):
        freqs = centroids[idx*bins:(idx + 1)*bins]
        db = dbs[idx*bins:(idx + 1)*bins]
        freqs_occupancy = occupancy_in_range(freqs, freq_range)
        db_occupancy = occupancy_in_range(db, db_range)
        if freqs_occupancy >= 0.7 and db_occupancy >= 0.7:
            regions.append((time, t_centroids[idx + 1]))
    return np.array(regions)


def freqs_and_dbs(audio, sampling, sensitivity):
    """
        We calculate here the frequencies and dBs bins.
    """
    centroids = librosa.feature.spectral_centroid(audio, sr = sampling)[0]
    ffts = librosa.stft(audio)
    magnitude, phase = librosa.magphase(ffts)

    dbs = librosa.amplitude_to_db(magnitude, ref = sensitivity, top_db = None)
    dbs += abs(dbs.min())
    freq_bins = librosa.display.__coord_fft_hz(ffts.shape[0], sr = sampling)
    return centroids, freq_bins, dbs


def occupancy_in_range(array, range):
    """
        Calculates the proportion of values in the given range.
    """
    idxs = np.where((array >= range[0])  & (array <= range[1]))[0]
    return len(idxs) / len(array)
    