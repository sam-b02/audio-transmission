from utils import image_encoding

mode = input("Do you want to (T)ransmit or (R)ecieve?")

if mode == "T":
    image = image_encoding.encode_image(input(r"please enter image path"), True)
    print("image has been successfully encoded!")