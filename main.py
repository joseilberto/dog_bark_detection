from datetime import datetime
from time import sleep
from os.path import join, dirname

import matplotlib.pyplot as plt
import os

from data.config import *
from pipelines.communication import create_body, send_files
from pipelines.detect import detect_bark_howl
from pipelines.io import load_audio, save_audio
from pipelines.record import record_segment


if __name__ == "__main__":
    audio_path = join(".", "data", "youtube_sample2.mp3")
    os.makedirs(dirname(audio_path), exist_ok = True)
    # check = record_segment(audio_path, length = 5)
    audio, sampling = load_audio(audio_path, sampling = None)
    extract = 20 * sampling
    base_output_bark = join(".", "data", "youtube_folder{}", "bark_{}.wav").format
    base_output_howl = join(".", "data", "youtube_folder{}", "howl_{}.wav").format
    nfiles, cur_folder, count = 5, 1, 0
    files = []
    for idx in range(int(len(audio) / extract)):
        short_audio = audio[idx*extract:(idx + 1)*extract]    
        bark, clipped_audio = detect_bark_howl(short_audio)
        howl, clipped_audio_howl = detect_bark_howl(audio, freq_range = (200, 800))
        if not bark and not howl:
            continue
        sleep(2)
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y_%H_%M_%S")
        if not bark and howl:
            output_audio = base_output_howl(cur_folder, current_time)
            clipped_audio = clipped_audio_howl
        else:
            output_audio = base_output_bark(cur_folder, current_time)            
        os.makedirs(dirname(output_audio), exist_ok = True)
        files.append(output_audio)
        save_audio(output_audio, clipped_audio[::4], int(sampling / 4))
        count += 1
        if count % nfiles == 0:
            cur_folder += 1
            message["body"] = create_body(files, message)
            send_files(files, sender, receiver, message, send_all = True)
            files = []
            break
