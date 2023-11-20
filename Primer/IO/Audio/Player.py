import asyncio
import simpleaudio as sa
import os.path
import subprocess
from urllib import request

class Player():
    def __init__(self,pp):
        self.pp=pp
        self.wav_store_dir=pp.config['audio']['wav_store_dir']
        self.ogg_store_dir=pp.config['audio']['ogg_store_dir']

    #if files start with annoying click, converting them to 48000Hz may help
    async def play_wav(self, audio_file: str):
        wav_path=self.wav_store_dir+str(audio_file)+".wav"
        #check the wav cache
        if not os.path.isfile(wav_path):
            ogg_path=self.ogg_store_dir+str(audio_file)+".ogg"
            #check the ogg cache
            if not os.path.isfile(ogg_path):
                request.urlretrieve(self.pp.config['audio']['external_store_url']+str(audio_file)+".ogg",ogg_path)
            subprocess.run(['opusdec', ogg_path, wav_path], check=True)

        file_to_play = sa.WaveObject.from_wave_file(wav_path)
        file_to_play.play()

    async def stop_player(self):
        sa.stop_all()
