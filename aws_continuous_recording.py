from datetime import datetime
from os.path import join, dirname

import os

from data.aws_credentials import credentials
from pipelines.aws_communication import send_files
from pipelines.detect import detect_bark_howl
from pipelines.io import load_audio, save_audio
from pipelines.record import record_segment
from pipelines.store import get_batches


if __name__ == "__main__":
    n_files = 5
    attempts = 10
    length = 30

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")

    temp_audio_path = join(".", "data", "tmp", "tmp.wav")
    os.makedirs(dirname(temp_audio_path), exist_ok = True)

    output_path = join(".", "data", "jojo_{}".format(date))
    os.makedirs(output_path, exist_ok = True)
    output_path_bark = join(output_path, "bark_{}.wav")
    output_path_howl = join(output_path, "howl_{}.wav")
    
    while True:
        files = get_batches(temp_audio_path, output_path_bark, 
                            output_path_howl, length = length, 
                            n_files = n_files, subsampling = 4, 
                            attempts = attempts)
        if not files:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S on %d-%m-%Y")
            print("No files with bark stored at", current_time)
            continue
        try:
            send_files(files, credentials, credentials["bucket"])
        except:
            continue