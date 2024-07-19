import asyncio
import simpleaudio as sa
import os.path
import subprocess
from urllib import request

class Player():
    def __init__(self,pp):
        self.pp = pp
        self.wav_store_dir = pp.config['audio']['wav_store_dir']
        self.ogg_store_dir = pp.config['audio']['ogg_store_dir']

    #if files start with annoying click, converting them to 48000Hz may help
    async def play_wav(self, audio_file: str):
        #wav_path=self.wav_store_dir+str(audio_file)+".wav"
        file_to_play = sa.WaveObject.from_wave_file(audio_file)
        file_to_play.play()

    async def stop_player(self):
        sa.stop_all()
