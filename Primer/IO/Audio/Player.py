import asyncio
import simpleaudio as sa

class Player():
    def __init__(self,pp):
        self.pp=pp

    async def play_wav(self, audio_file: str):
        path=self.wav_store_dir+str(audio_file)+".wav"
        file_to_play = sa.WaveObject.from_wave_file(path)
        file_to_play.play()

    async def stop_player(self):
        sa.stop_all()
