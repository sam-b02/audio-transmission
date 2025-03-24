import numpy as np
import pyaudio
import wave

class AudioManager:
    def __init__(self, sample_rate=44100, chunk_size=1024, record_file="recorded_audio.wav"):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.record_file = record_file
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
        print(f"Listening for {target_frequencies} Hz for {duration} seconds...")
        num_chunks = int((self.sample_rate / self.chunk_size) * duration)
        target_frequencies = set(target_frequencies)
        frames = []
        
        for _ in range(num_chunks):
            audio_data = self.input_stream.read(self.chunk_size)
            frames.append(audio_data)
            
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            fft_result = np.fft.rfft(audio_array)
            freqs = np.fft.rfftfreq(len(audio_array), d=1/self.sample_rate)
            
            magnitude = np.abs(fft_result)
            peak_freq = freqs[np.argmax(magnitude)]
            
            print(f"Detected frequency: {peak_freq:.2f} Hz")
            
            for target in target_frequencies:
                if abs(peak_freq - target) <= tolerance:
                    print(f"Matched {peak_freq:.2f} Hz (target: {target} Hz)")
                    self.save_recording(frames)
                    return True
        
        self.save_recording(frames)
        print("No matching frequency detected.")
        return False
    
    def save_recording(self, frames):
        with wave.open(self.record_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pyaudio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
        print(f"Recording saved to {self.record_file}")
    
    def close(self):
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        self.pyaudio.terminate()
