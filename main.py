from os.path import join, dirname

import os

from pipelines.record import record_segment
from pipelines.load import load_audio

if __name__ == "__main__":
    audio_path = join(".", "data", "sample1.wav")
    os.makedirs(dirname(audio_path), exist_ok = True)
    check = record_segment(audio_path, length = 5)
    audio, sampling = load_audio(audio_path)

