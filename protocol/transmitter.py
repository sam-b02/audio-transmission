import time

def transmit(audio_util, image, max_retries=10):

    detected_signal = False
    counter = 0

    while not detected_signal and counter <= max_retries:
        audio_util.play_tone(850, 1)
        
        print("Listening for receiver response...")
        detected_signal = audio_util.listen_for_tones([750], duration=3)
        counter += 1
        
        if detected_signal:
            print("Detected receiver! Starting handshake...")
            audio_util.play_tone(750, 1)
            break #BRO TS THE TWO GENERALS PROBLEM THEY DONT ACTUALLY KNOW
        else:
            print("No response detected. Trying again...")
    
    if not detected_signal:
        print("Max retries reached. Transmission failed.")