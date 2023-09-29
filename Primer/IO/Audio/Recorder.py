import time, os, asyncio
import pyaudio
import wave
import json
from urllib.parse import quote
import websocket
import ssl

class Recorder:
    def __init__(self,pp):
        self.pp=pp
        config=pp.config['audio']
        self.soundcard=config['soundcard']
        self.wav_store_dir=config['wav_store_dir']
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.channels = 1
        self.fs = 16000
        self.sample_width = 2
        self.stream = None
        self.text = "TESTRECORD"
        self.is_recording = False
        self.device_index = None
        self.audio_dir = config['session_audio_dir']
        self.scorer_id=0

    async def stop_recording(self):
        self.append_frames()
        await self.write_audiofile(self.text)

    async def check_device(self):
        for i in range(self.p.get_device_count()):
            dev=p.get_device_info_by_index(i)
            if dev.name==self.soundcard:
                self.device_index=dev.index

    async def start_recording(self,text):
        self.stream = self.p.open(channels=self.channels,rate=self.fs,format=self.p.get_format_from_width(self.sample_width),input=True,input_device_index=self.device_index)
        self.text=text
        self.is_recording=True
        #print("startin recording")
        while self.is_recording:
            #print("recordin")
            await self.pp.loop.run_in_executor(None, self.append_frames)
            await asyncio.sleep(0.1)

    def append_frames(self):
        available_frames = self.stream.get_read_available()
        if available_frames > 0:
            self.frames.append(self.stream.read(available_frames))

    async def write_audiofile(self, text: str):
        self.stream.stop_stream()
        self.stream.close()
        #print('name: ' + text)
        audio_file=self.audio_dir+self.pp.student.session_id+'/'+text
        #print('write audiofile to %s' % audio_file)
        waveFile = wave.open(audio_file,'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(self.sample_width)))
        waveFile.setframerate(self.fs)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()
        await self.pp.queue['mikroserver'].put({'f':audio_file,'t':self.text})
        self.frames = []

