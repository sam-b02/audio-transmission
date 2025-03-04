from utils import image_encoding
from utils import audio_util

audio_util = audio_util.AudioManager(44100)
mode = input("Do you want to (T)ransmit or (R)ecieve?")
max_retries = 10
counter = 0

if mode == "T":
    image = image_encoding.encode_image(input(r"please enter image path"), True)
    print("image has been successfully encoded!")

    print("sending out engagement signal...")
    detected_signal = False

    while not detected_signal and counter <= max_retries:
        audio_util.play_tone(850, 0.5)
        audio_util.play_tone(650, 0.5)
        
        print("Listening for receiver response...")
        detected_signal = audio_util.listen_for_tones([750], duration=3)
        counter += 1
        
        if detected_signal:
            print("Detected receiver! Starting handshake...")
            audio_util.play_tone(750, 0.5)
            break
        else:
            print("No response detected. Trying again in 2 seconds...")
            import time
            time.sleep(2)
    
elif mode == "R":
    print("Listening for incoming transmission...")
    detected_signal = False
    
    while not detected_signal:
        detected_signal = audio_util.listen_for_tones([850, 650], duration=5)
        
        if detected_signal:
            print("Engagement signal detected!")
            print("Sending acknowledgment...")
            audio_util.play_tone(750, 0.5)

            time.sleep(0.25)
            
            ack_detected = audio_util.listen_for_tones([750], duration=3)
            if ack_detected:
                print("Handshake established!")
            else:
                print("Sender didn't acknowledge. Listening again...")
                detected_signal = False
        else:
            print("No transmission detected. Continuing to listen...")