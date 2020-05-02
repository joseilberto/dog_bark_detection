import os
import pyaudio
import wave

def record_segment(
        path, length = 30, sampling = 44100, depth = 32, 
        channels = 1, chunk = 1024
        ):
    """
        path (str): Path where the file will be stored.
        length (float): Length of the recorded segment in seconds.
        sampling (int): Sampling rate of the stream.
        depth (int): The limit values of the dynamic range (for 32bit the maximum value is 2.147.483.648 and minimum -2.147.483.648). 
        channels (int): Number of channels being recorded.
        chunk (int): The chunk size that is read from a buffer.
    """    
    nsteps = int((sampling / chunk) * length)
    audio_format = eval("pyaudio.paInt{}".format(depth))

    audio = pyaudio.PyAudio()
    stream = audio.open(format = audio_format, channels = channels, 
                        rate = sampling, input = True, 
                        frames_per_buffer = chunk)
    frames = [stream.read(chunk) for i in range(0, nsteps)]

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return save_segment(path, frames, length, sampling, depth, channels, 
                    audio.get_sample_size(audio_format))


def save_segment(
        path, frames, length = 30, sampling = 44100, 
        depth = 32, channels = 1, sampling_width = 4):
    """
        path (str): Path where the file will be stored.
        frames (list of binary strings): A list containing the data we want to save in the file.
        length (float): Length of the recorded segment in seconds.
        sampling (int): Sampling rate of the stream.
        depth (int): The limit values of the dynamic range (for 32bit the maximum value is 2.147.483.648 and minimum -2.147.483.648). 
        channels (int): Number of channels being recorded.
        sampling_width (int): The sampling width with which we want to record the file.
    """
    output = wave.open(path, "wb")
    output.setnchannels(channels)
    output.setsampwidth(sampling_width)
    output.setframerate(sampling)
    output.writeframes(b"".join(frames))
    output.close()
    return os.path.isfile(path)