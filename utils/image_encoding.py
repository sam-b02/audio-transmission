import numpy as np
from PIL import Image

def encode_image(image_path, image_average):
    print("loading image...")

    image_array = np.array(Image.open(image_path).convert("L"))
    threshold = np.mean(image_array) if image_average else 128

    print("image loaded!")

    return process_image_to_bits(image_array, threshold)

def process_image_to_bits(array, threshold):
    print("processing image...")
    return [get_streaks(row, threshold) for row in array]

def get_streaks(row, threshold):
    binary = (row < threshold).astype(int)
    change_points = np.where(np.diff(binary))[0]
    
    streaks = []
    start = 0
    current_val = int(binary[0])
    
    for point in change_points:
        streaks.append([int(point - start + 1), current_val])
        start = point + 1
        current_val = 1 - current_val
    
    streaks.append([int(len(binary) - start), current_val])
    return streaks
