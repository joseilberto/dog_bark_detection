from datetime import datetime
from time import sleep
from os.path import join, dirname

import matplotlib.pyplot as plt
import os

from data.config import *
from pipelines.communication import create_body, send_files
from pipelines.detect import detect_bark
from pipelines.io import load_audio, save_audio
from pipelines.record import record_segment


if __name__ == "__main__":
    audio_path = join(".", "data", "youtube_sample1.mp3")
    os.makedirs(dirname(audio_path), exist_ok = True)
    # check = record_segment(audio_path, length = 5)
    audio, sampling = load_audio(audio_path, sampling = None)
    extract = 20 * sampling
    base_output = join(".", "data", "youtube_folder{}", "bark_{}.wav").format
    nfiles, cur_folder, count = 5, 1, 0
    files = []
    for idx in range(int(len(audio) / extract)):
        short_audio = audio[idx*extract:(idx + 1)*extract]    
        bark, clipped_audio = detect_bark(short_audio)
        if not bark:
            continue
        sleep(2)
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y_%H_%M_%S")
        output_audio = base_output(cur_folder, current_time)
        os.makedirs(dirname(output_audio), exist_ok = True)
        files.append(output_audio)
        save_audio(output_audio, clipped_audio[::4], int(sampling / 4))
        count += 1
        if count % nfiles == 0:
            cur_folder += 1
            message["body"] = create_body(files, message)
            send_files(files, sender, receiver, message)
            files = []
            break
