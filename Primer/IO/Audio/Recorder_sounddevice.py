import time, os, asyncio
import sounddevice as sd
import wave
import json
from urllib.parse import quote
import websocket
import ssl

class Recorder:
    def __init__(self, pp):
        self.pp = pp
        config = pp.config['audio']
        self.soundcard = config['soundcard']
        self.wav_store_dir = config['wav_store_dir']
        self.frames = []
        self.channels = 1
        self.fs = 16000
        self.sample_width = 2
        self.stream = None
        self.text = "TESTRECORD"
        self.is_recording = False
        self.device_index = 0
        self.audio_dir = config['session_audio_dir']
        self.scorer_id = 0

    async def stop_recording(self):
        self.append_frames()
        await self.write_audiofile(self.text)

    async def check_device(self):
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"Device {i}: {device['name']}")
            if device['name'] == self.soundcard:
                self.device_index = i

    async def start_recording(self, text):
        await self.check_device()
        print("DEVICE INDEX")
        print(self.device_index)
        self.stream = sd.InputStream(channels=self.channels, samplerate=self.fs, device=self.device_index)
        self.stream.start()
        self.text = text
        self.is_recording = True
        while self.is_recording:
            await self.pp.loop.run_in_executor(None, self.append_frames)
            await asyncio.sleep(0.1)

    def append_frames(self):
        available_frames = self.stream.read_available
        if available_frames > 0:
            frames, overflowed = self.stream.read(available_frames)
            if overflowed:
                print("Buffer overflow!")
            self.frames.append(frames.tobytes())

    async def write_audiofile(self, text: str):
        self.stream.stop()
        audio_file = os.path.join(self.audio_dir, self.pp.student.session_id, text)
        waveFile = wave.open(audio_file, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.sample_width)
        waveFile.setframerate(self.fs)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()
        await self.pp.queue['mikroserver'].put({'f': audio_file, 't': self.text})
        self.frames = []

