from os.path import join, dirname

import matplotlib.pyplot as plt
import os

from pipelines.detect import detect_bark
from pipelines.load import load_audio
from pipelines.record import record_segment

if __name__ == "__main__":
    audio_path = join(".", "data", "youtube_sample1.mp3")
    os.makedirs(dirname(audio_path), exist_ok = True)
    # check = record_segment(audio_path, length = 5)
    audio, sampling = load_audio(audio_path, sampling = None)
    short_audio = audio[:15*sampling]    
    detect_bark(short_audio)

