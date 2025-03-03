from utils import image_encoding
from utils import audio_util

mode = input("Do you want to (T)ransmit or (R)ecieve?")

if mode == "T":
    image = image_encoding.encode_image(input(r"please enter image path"), True)
    print("image has been successfully encoded!")

    print("sending out engagement signal...")

    audio_util.play_tone(850, 0.5)
    audio_util.play_tone(650, 0.5)