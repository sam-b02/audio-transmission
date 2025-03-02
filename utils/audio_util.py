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