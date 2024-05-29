import asyncio
import alsaaudio
import os.path
import subprocess
import wave
from urllib import request

class Player():
    def __init__(self,pp):
        self.pp = pp
        config = pp.config['audio']
        self.wav_store_dir = config['wav_store_dir']
        self.ogg_store_dir = config['ogg_store_dir']
        self.soundcard = config['soundcard']
        self.device = None
        self.wav = None
        self.period_size = 512

    def get_alsa_format(self,wav_file):
        # This function maps wave file format to ALSA format
        width = wav_file.getsampwidth()
        if width == 1:
            return alsaaudio.PCM_FORMAT_S8
        elif width == 2:
            return alsaaudio.PCM_FORMAT_S16_LE
        elif width == 3:
            return alsaaudio.PCM_FORMAT_S24_LE
        elif width == 4:
            return alsaaudio.PCM_FORMAT_S32_LE
        else:
            raise ValueError("Unsupported format")

    async def play_wav(self, audio_file: str):
        self.device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL,device=self.soundcard)
        wav_path = f"{self.wav_store_dir}{str(audio_file)}.wav"
        #check the wav cache
        if not os.path.isfile(wav_path):
            ogg_path = f"{self.ogg_store_dir}{str(audio_file)}.ogg"
            #check the ogg cache
            if not os.path.isfile(ogg_path):
                request.urlretrieve(f"{self.pp.config['audio']['external_store_url']}{str(audio_file)}.ogg", ogg_path)
            subprocess.run(['opusdec', ogg_path, wav_path], check=True)

        #file_to_play = sa.WaveObject.from_wave_file(wav_path)
        #file_to_play.play()
        self.wav=wave.open(wav_path,'rb')
        channels = self.wav.getnchannels()
        rate = self.wav.getframerate()
        self.device.setchannels(channels)
        self.device.setrate(rate)
        self.device.setformat(self.get_alsa_format(self.wav))
        self.device.setperiodsize(self.period_size)
        await self.pp.loop.run_in_executor(None, self.playback)

    def playback(self):
        while data := self.wav.readframes(self.period_size):
            # Write data to device
            self.device.write(data)
        self.wav.close()

    async def stop_player(self):
        #sa.stop_all()
        if self.device:
            print("closing stream")
            self.device.close()
