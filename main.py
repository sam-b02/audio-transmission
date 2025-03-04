from protocol import reciever
from protocol import transmitter
from utils import image_encoding

from utils import audio_util


def main():
    audio_manager = audio_util.AudioManager(44100)
    
    mode = input("Do you want to (T)ransmit or (R)eceive? ").upper()
    
    try:
        if mode == "T":
            image = image_encoding.encode_image(input("Please enter image path: "), True)
            print("Image has been successfully encoded!")
            transmitter.transmit(audio_manager, image)
        elif mode == "R":
            reciever.receive(audio_manager)
        else:
            print("Invalid mode. Please choose T or R.")
    finally:
        audio_manager.close()

if __name__ == "__main__":
    main()