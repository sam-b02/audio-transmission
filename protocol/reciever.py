import time

def receive(audio_util):
    print("Listening for incoming transmission...")
    detected_signal = False
    
    while not detected_signal:
        detected_signal = audio_util.listen_for_tones([850], duration=5)
        
        if detected_signal:
            print("Engagement signal detected!")
            print("Sending acknowledgment...")
            audio_util.play_tone(750, 1)
            
            ack_detected = audio_util.listen_for_tones([750], duration=3)
            if ack_detected:
                print("Handshake established!")
            else:
                print("Sender didn't acknowledge. Listening again...")
                detected_signal = False
        else:
            print("No transmission detected. Continuing to listen...")