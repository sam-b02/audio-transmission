import pyaudio
import numpy as np

#TO ADD - CACHING OF PARTICULAR FREQUENCIES, STOP CLOSING AND REOPENING STREAM

def play_tone(frequency=1000, duration=3, volume=0.5):

    p = pyaudio.PyAudio()

    sample_rate = 44100  # CD quality
    samples = int(duration * sample_rate)

    t = np.linspace(0, duration, samples, False)
    tone = volume * np.sin(2 * np.pi * frequency * t)
    
    audio_data = tone.astype(np.float32).tobytes()

    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=sample_rate,
        output=True
    )

    stream.write(audio_data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print(f"Played {frequency}Hz tone for {duration} seconds")

def listen_for_tones(target_frequencies, duration=5, threshold=0.5):
    """Listen for specific frequencies in the audio input."""
    p = pyaudio.PyAudio()
    
    sample_rate = 44100
    chunk_size = 1024
    
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )
    
    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Convert frames to numpy array for processing
    signal = np.frombuffer(b''.join(frames), dtype=np.float32)
    
    # Use FFT to detect frequencies
    # This is a simplified approach - you might need more robust detection
    fft_result = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
    
    detected = []
    for freq in target_frequencies:
        # Find the closest frequency bin
        idx = np.argmin(np.abs(freqs - freq))
        if fft_result[idx] > threshold:
            detected.append(freq)
    
    return detected == target_frequencies