#!/usr/bin/python3
#Displays a picture on e-ink (nice to run before shutdown)
#Co(d|mb)ed by Prof. Dr. Dr. Daniel Devatman Hromada as a second App of the digital Primer (fibel.digital) project
#Commercial use without explicit consent of the author prohibited
#Where appropriate, CC BY-NC-SA applies, in all other cases mrGPL
#UdK / ECDF / wizzion.com AE5006, June 2020
#Berlin, Deutschland, EU

from io import BytesIO
from time import sleep
#import Fibel.drivers.it8951 as driver_it8951
from IT8951.display import AutoEPDDisplay
from IT8951.EPD_functions import *
from PIL import Image
import RPi.GPIO as GPIO

display = AutoEPDDisplay(vcom = -1.72, rotate = "CCW", spi_hz = 80000000)

display_image_8bpp(display, "/home/fibel/personal_Primer/data/assets/buddha.png")

