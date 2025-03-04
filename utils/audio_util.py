import numpy as np
import pyaudio

class AudioManager:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.pyaudio = pyaudio.PyAudio()
        self.tone_cache = {}
        
        self.output_stream = self.pyaudio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True
        )
        
        self.input_stream = self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
    
    def generate_tone(self, frequency, duration, volume=0.5):
        cache_key = (frequency, duration, volume)
        if cache_key not in self.tone_cache:
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples, False)
            tone = volume * np.sin(2 * np.pi * frequency * t)
            audio_data = tone.astype(np.float32).tobytes()
            self.tone_cache[cache_key] = audio_data
        return self.tone_cache[cache_key]
    
    def play_tone(self, frequency, duration, volume=0.5):
        audio_data = self.generate_tone(frequency, duration, volume)
        self.output_stream.write(audio_data)
        print(f"Played {frequency}Hz tone for {duration} seconds")
    
    def listen_for_tones(self, target_frequencies, duration=3, tolerance=10):
        """Listen for specific frequencies within a given duration."""
        print(f"Listening for {target_frequencies} Hz for {duration} seconds...")
        num_chunks = int((self.sample_rate / self.chunk_size) * duration)
        target_frequencies = set(target_frequencies)
        
        for _ in range(num_chunks):
            audio_data = np.frombuffer(self.input_stream.read(self.chunk_size), dtype=np.int16)
            fft_result = np.fft.rfft(audio_data)
            freqs = np.fft.rfftfreq(len(audio_data), d=1/self.sample_rate)
            
            peak_freq = freqs[np.argmax(np.abs(fft_result))]
            
            for target in target_frequencies:
                if abs(peak_freq - target) <= tolerance:
                    print(f"Detected {peak_freq:.2f} Hz (target: {target} Hz)")
                    return True
        
        print("No matching frequency detected.")
        return False
    
    def close(self):
        """Close all streams and PyAudio instance."""
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        self.pyaudio.terminate()
