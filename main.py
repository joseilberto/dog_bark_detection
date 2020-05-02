from os.path import join, dirname

import os

from acquisition.record import record_segment


if __name__ == "__main__":
    audio_path = join(".", "data", "sample1.wav")
    os.makedirs(dirname(audio_path), exist_ok = True)
    check = record_segment(audio_path, length = 5)
    
