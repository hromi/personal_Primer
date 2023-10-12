from PIL import Image
import os,re
import time
from IT8951 import constants
from IT8951.EPD_functions import *
from IT8951.display import AutoEPDDisplay
# Your e-ink library might go here
#import eink_library
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def load_images(directory):
    images = []
    for filename in sorted(os.listdir(directory),key=natural_keys):
        print(filename)
        if filename.endswith(".bmp"):
            filepath = os.path.join(directory, filename)
            img = Image.open(filepath)
            images.append(img)
    return images

def display_images(images, epd):
    for img in images:
        # Your e-ink display code goes here. This is a generalized placeholder.
        # eink_library.send_to_display(img)
        # eink_library.refresh_display()
        epd.frame_buf.paste(img, [0,50])
        epd.draw_partial(constants.DisplayModes.DU)
 

        # Here, delay defines how long we wait (in seconds) before showing the next image.
        #time.sleep(delay)

# Example usage:
directory = "/home/fibel/data/animations/xmas/bmp/"
epd= AutoEPDDisplay(vcom=-2.37,rotate="CCW",spi_hz=80000000)
images = load_images(directory)
display_images(images,epd)

