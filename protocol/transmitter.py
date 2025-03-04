import time

def transmit(audio_util, image, max_retries=10):

    detected_signal = False
    counter = 0

    while not detected_signal and counter <= max_retries:
        audio_util.play_tone(850, 1)
        
        print("Listening for receiver response...")
        detected_signal = audio_util.listen_for_tones([750], duration=1)
        counter += 1
        
        if detected_signal:
            print("Detected receiver! Starting handshake...")
            audio_util.play_tone(750, 1)
            break
        else:
            print("No response detected. Trying again in 2 seconds...")
            time.sleep(2)
    
    if not detected_signal:
        print("Max retries reached. Transmission failed.")