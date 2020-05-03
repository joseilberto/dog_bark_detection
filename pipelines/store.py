from datetime import datetime

from .detect import detect_bark
from .io import load_audio, save_audio
from .record import record_segment


def get_batches(
    temp_audio_path, output_path, attempts = 15, 
    length = 30, n_files = 5, subsampling = 1):
    """
        Parameters:
            temp_audio_path (str): Path where we save temporary audio files to be processed.
            output_path (str): Output path pattern to be completed in this function.
            attempts (int): Number of recording to be processed as containing barks.
            length (float): Length of the recorded segment in seconds.
            n_files (int): Number of files audio files with barking to be stored.
            subsampling (int): Subsampling rate for the audio to reduce its final storage space.
    """
    files = []    
    for i in range(attempts):
        check = record_segment(temp_audio_path, length = length)
        if not check:
            continue
        audio, sampling = load_audio(temp_audio_path, sampling = None)
        bark, clipped_audio = detect_bark(audio, sampling)
        if not bark:
            continue
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y_%H_%M_%S")
        output = output_path.format(current_time)
        save_audio(output, clipped_audio[::subsampling], 
                            int(sampling / subsampling))
        files.append(output)
    return files