from os.path import join, dirname

import matplotlib.pyplot as plt
import os

from pipelines.detect import detect_bark
from pipelines.io import load_audio, save_audio
from pipelines.record import record_segment

if __name__ == "__main__":
    audio_path = join(".", "data", "youtube_sample1.mp3")
    os.makedirs(dirname(audio_path), exist_ok = True)
    # check = record_segment(audio_path, length = 5)
    audio, sampling = load_audio(audio_path, sampling = None)
    short_audio = audio[60*sampling:90*sampling]    
    bark, clipped_audio = detect_bark(short_audio)
    output_audio = audio_path.replace("sample1.mp3", "bark1.wav")
    save_audio(output_audio, clipped_audio)

