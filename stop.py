#!/usr/bin/python3
#Displays a picture on e-ink (nice to run before shutdown)
#Co(d|mb)ed by Prof. Dr. Dr. Daniel Devatman Hromada as a second App of the digital Primer (fibel.digital) project
#Commercial use without explicit consent of the author prohibited
#Where appropriate, CC BY-NC-SA applies, in all other cases mrGPL
#UdK / ECDF / wizzion.com AE5006, June 2020
#Berlin, Deutschland, EU

#from io import BytesIO
#from time import sleep
from IT8951.display import AutoEPDDisplay
from IT8951.EPD_functions import *
#from PIL import Image
#import RPi.GPIO as GPIO
import yaml

with open('primer.yaml', 'r') as file:
    config = yaml.safe_load(file)
     
display = AutoEPDDisplay(vcom = config['EPD']['vcom'], rotate = config['EPD']['rotate'], spi_hz = config['EPD']['spi_hz'])
display_image_8bpp(display, config['gfx']['screensaver'])

