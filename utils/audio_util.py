import pyaudio
import numpy as np

class AudioManager:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.pyaudio = pyaudio.PyAudio()
        self.output_stream = None
        self.input_stream = None
        self.tone_cache = {}
    
    def generate_tone(self,frequency, duration, volume=0.5):
        cache_key = (frequency, duration, volume)
        if cache_key not in self.tone_cache:
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples, False)
            tone = volume * np.sin(2 * np.pi * frequency * t)
            audio_data = tone.astype(np.float32).tobytes()
            self.tone_cache[cache_key] = audio_data
        return self.tone_cache[cache_key]
    
    def play_tone(self,frequency, duration, volume=0.5):
        if not self.output_stream:
            self.output_stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                output=True
            )
        
        audio_data = self.generate_tone(frequency, duration, volume)
        self.output_stream.write(audio_data)
        print(f"Played {frequency}Hz tone for {duration} seconds")

    def listen_for_tones(self, target_frequencies, duration=5, threshold=0.5):
        """Listen for specific frequencies, reusing input stream"""
        # Open input stream if not already open
        if not self.input_stream:
            self.input_stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=1024
            )
        
        # Read frames
        frames = []
        for _ in range(0, int(self.sample_rate / 1024 * duration)):
            data = self.input_stream.read(1024)
            frames.append(data)
        
        # Convert frames to numpy array for processing
        signal = np.frombuffer(b''.join(frames), dtype=np.float32)
        
        # FFT frequency detection
        fft_result = np.abs(np.fft.rfft(signal))
        freqs = np.fft.rfftfreq(len(signal), 1/self.sample_rate)
        
        detected = []
        for freq in target_frequencies:
            # Find the closest frequency bin
            idx = np.argmin(np.abs(freqs - freq))
            if fft_result[idx] > threshold:
                detected.append(freq)
        
        return detected == target_frequencies
    
    def close(self):
        """Close all streams and PyAudio instance"""
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        self.pyaudio.terminate()