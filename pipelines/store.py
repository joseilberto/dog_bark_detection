from datetime import datetime

from .detect import detect_bark
from .io import load_audio, save_audio
from .record import record_segment


def get_batches(temp_audio_path, output_path, n_files = 5):
    files = []    
    while len(files) < n_files:
        check = record_segment(temp_audio_path, length = 30)
        if not check:
            continue
        audio, sampling = load_audio(temp_audio_path, sampling = None)
        bark, clipped_audio = detect_bark(audio, sampling)
        if bark:
            now = datetime.now()
            current_time = now.strftime("%d-%m-%Y_%H_%M")
            output = output_path.format(current_time)
            save_audio(output, clipped_audio)
            files.append(output)
    return files