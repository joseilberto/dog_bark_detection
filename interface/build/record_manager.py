from datetime import datetime
from os.path import join, dirname

import os

from pipelines.communication import create_body, send_files
from pipelines.detect import detect_bark_howl
from pipelines.io import load_audio, save_audio
from pipelines.record import record_segment
from pipelines.store import get_batches

from .constants import message


class RecordManager:
    def __init__(self, current_dir):
        self.current_dir = current_dir

    
    def continuous_recording(self, entries):
        configuration = self.process_entries(entries)
        while True:
            files = get_batches(configuration["temp_audio_path"], 
                                configuration["output_path_bark"], 
                                configuration["output_path_howl"], 
                                length = configuration["length"], 
                                n_files = configuration["n_files"], 
                                subsampling = 4, 
                                attempts = configuration["attempts"])
            if not files:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S on %d-%m-%Y")
                print("No files with bark stored at", current_time) #TODO Send to a small console below the buttons
                continue
            message.update({
                "body": create_body(files, message)
            })
            try:
                send_files(files, configuration["sender"], configuration["receiver"], configuration["message"])
            except:
                continue
    

    def process_entries(self, entries):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        configuration = {
            "date": date,
            "temp_audio_path": join(".", "data", "tmp", "tmp.wav"),
            "output_path": join(".", "data", "jojo_{}".format(date)),
        }

        for key, entry in entries.items():
            if key in ["n_files", "length", "attempts"]:                
                value = int(entry.get())                
                configuration[key] = value
            elif key == "sender":            
                configuration[key] = {
                    "email": entry.get()
                }
            elif key == "receiver":
                configuration[key] = {
                    "email": entry.get(),
                    "password": entries["sender_password"].get(),
                    "smtp_server": "smtp.gmail.com",
                    "port": 465,
                }

        configuration.update({
            "output_path_bark": join(configuration["output_path"], "bark_{}.wav"),
            "output_path_howl": join(configuration["output_path"], "howl_{}.wav"),
        })       
            
        configuration["message"] = message

        os.makedirs(dirname(configuration["temp_audio_path"]), exist_ok = True)
        os.makedirs(configuration["output_path"], exist_ok = True)
        
        return configuration


        

