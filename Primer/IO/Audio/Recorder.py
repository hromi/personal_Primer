import time, os, asyncio
import alsaaudio
import wave
import numpy as np

class Recorder:
    def __init__(self, pp):
        self.pp = pp
        config = pp.config['audio']
        self.soundcard = config['soundcard']
        self.wav_store_dir = config['wav_store_dir']
        self.frames = bytearray()
        self.channels = 2
        self.fs = config['rate']
        self.sample_width = 2
        self.stream = None
        self.text = "TESTRECORD"
        self.is_recording = False
        self.audio_dir = config['session_audio_dir']
        self.scorer_id = 0

    async def stop_recording(self):
        self.stream.close()
        await self.write_audiofile(self.text)

    async def check_device(self):
        # In ALSA, devices are usually referred to by their names or "plughw:index,subindex"
        # You can list all devices using "arecord -L" in the terminal
        # Here, we just print the configured soundcard name
        print(f"Using ALSA soundcard: {self.soundcard}")

    def median_filter(self,signal, kernel_size=3):
        # Ensure the kernel size is odd
        kernel_size = max(3, kernel_size | 1)
    
        # Pad the signal at the beginning and end to handle edge cases
        padded_signal = np.pad(signal, kernel_size // 2, mode='edge')
    
        # Apply the median filter
        filtered_signal = np.array([
            np.median(padded_signal[i:i + kernel_size]) for i in range(len(signal))
        ])
        return filtered_signal

    async def start_recording(self, text):
        await self.check_device()
        print("Starting recording")
        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device=self.soundcard, rate=self.fs, channels=self.channels,periodsize=512)
        self.text = text
        self.is_recording = True
        while self.is_recording:
            await self.pp.loop.run_in_executor(None, self.append_frames)
            await asyncio.sleep(0.01)

    def append_frames(self):
        length,data = self.stream.read()
        if length > 0:
            print(length)
            samples = np.frombuffer(data, dtype=np.int16)
            # Reshape the array to have two columns, one for each channel
            samples = samples.reshape((-1, 2))
            # Average the two channels
            mono_samples = samples.mean(axis=1).astype(np.int16)
            self.frames+=bytearray(mono_samples)
    def apply_moving_average(self,audio_bytes, sample_width=2, window_size=3):
        # Convert the bytearray to a numpy array of the appropriate type
        if sample_width == 2:
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
        elif sample_width == 4:
            audio_array = np.frombuffer(audio_bytes, dtype=np.int32)
        else:
            raise ValueError("Unsupported sample width")

        # Apply the moving average filter
        filtered_array = self.moving_average_filter(audio_array, window_size=window_size)

        # Convert the numpy array back to bytes
        filtered_bytes = filtered_array.tobytes()

        return filtered_bytes

    def moving_average_filter(self,data, window_size=3):
        cumsum = np.cumsum(data, dtype=float)
        cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
        return np.round(cumsum[window_size - 1:] / window_size).astype(data.dtype)

    async def write_audiofile(self, text: str):
        print("Stopping recording")
        audio_file = os.path.join(self.audio_dir, self.pp.student.session_id, text)
        wave_file = wave.open(audio_file, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(self.sample_width)
        wave_file.setframerate(self.fs)
        #filtered = self.apply_moving_average(self.frames)

        wave_file.writeframes(self.frames)
        #wave_file.writeframes(filtered)
        wave_file.close()
        await self.pp.queue['mikroserver'].put({'f': audio_file, 't': self.text})
        self.frames = bytearray()

