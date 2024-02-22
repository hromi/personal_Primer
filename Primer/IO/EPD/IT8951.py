import asyncio
from math import sqrt
#from IT8951 import display
from sys import path
from IT8951 import constants
from IT8951.EPD_functions import *
from IT8951.display import AutoEPDDisplay
from Primer.Graphics.FolioText import FolioText
from Primer.Graphics.FolioTextNew import create_text_image

from PIL import Image,ImageDraw,ImageFont

import asyncio
import yaml

class EInkDisplay:
    def __init__(self,pp):
        self.driver_config = pp.config['EPD']
        self.gfx_config = pp.config['gfx']
        self.rotate=self.driver_config['rotate']
        self.display = AutoEPDDisplay(
            vcom=self.driver_config['vcom'],
            rotate=self.rotate,
            spi_hz=self.driver_config['spi_hz']
        )
        self.pp=pp
        self.cache={'body':{},'title':{}}

        #epd = self.display.epd
        #print('  img buffer address: {:X}'.format(epd.img_buf_address))
        #epd._set_img_buf_base_addr(epd.img_buf_address+65536)
        #epd = self.display.epd
        #print('  img buffer address: {:X}'.format(epd.img_buf_address))
        #print('System info:')
        #print('  display size: {}x{}'.format(epd.width, epd.height))
        #print('  img buffer address: {:X}'.format(epd.img_buf_address))
        #print('  firmware version: {}'.format(epd.firmware_version))
        #print('  LUT version: {}'.format(epd.lut_version))
        clear_display(self.display)
        self.text_font=self.gfx_config['font']
        self.font=self.text_font
        self.emoji_font=self.gfx_config['emoji']
        self.word_pointers=[]
        self.folio = FolioText((int(self.display.height),int(self.display.width/1)), self.word_pointers)
        self.white_title = Image.new("1",(600,200),255) 
        self.black_title = Image.new("1",(600,200),0) 
        self.black_content = Image.new("1",(600,600),0) 
        self.white_content = Image.new("1",(600,600),255) 
    
    async def display_image(self, image_filename):
        # Load and display the image on e-ink screen
        display_image_8bpp(self.display, self.gfx_config['image_path']+image_filename)

    async def calculate_font_size(string_length, base_font_size=16, base_character_area=256, available_area=360000):
        """
        Calculate the font size needed to fit a string into a 600px x 600px square.
    
        :param string_length: The length of the string.
        :param base_font_size: The font size used for the base character area calculation.
        :param base_character_area: The estimated area (in pixels) occupied by a character at the base font size.
        :param available_area: The total area (in pixels) available for the text.
        :return: The calculated font size.
        """
        # Calculate the total character area required for the string at the base font size
        total_character_area = string_length * base_character_area
        # Calculate the ratio of the available area to the required character area
        area_ratio = available_area / total_character_area
        # Adjust the font size based on the square root of the area ratio
        new_font_size = base_font_size * (area_ratio ** 0.5)
        return new_font_size

    async def display_folio(self, message):
        print(message)
        if 't' in message and message['t']!=self.pp.folio.title_text:
            if message['t']=='':
                self.clear_title()
            self.font=self.emoji_font if 't_emoji' in message else self.text_font
            self.pp.folio.title_text=message['t']
            await self.display_title(message['t'])

        if 'b' in message and message['b'] and message['b']!=self.pp.folio.body_text:
            self.font=self.emoji_font if 'b_emoji' in message else self.text_font
            self.pp.folio.body_text=message['b']
            self.pp.folio.image_name=None
            await self.display_body(message['b'])

        if 'i' in message and message['i']!=self.pp.folio.image_name:
            display_image_8bpp(self.display, self.gfx_config['image_path']+'/600x800/'+message['i'])
            self.pp.folio.image_name=message['i']
            self.pp.folio.body_text=None

        self.display.draw_partial(constants.DisplayModes.DU)
 
    async def display_title(self, title, emoji=False):
        #print("display",title)
        self.title=create_text_image(title,600,200,font_path=self.font)
        self.display.frame_buf.paste(self.title, [0,0])

    async def clear_title(self):
        self.display.frame_buf.paste(self.white_title, [0,0])
        self.display.draw_partial(constants.DisplayModes.DU)
  
    async def clear_content(self):
        self.display.frame_buf.paste(self.white_content, [0,200])
        self.display.draw_partial(constants.DisplayModes.DU)

    async def display_body(self, content,emoji=False):
        if content in self.cache['body']:
            self.body=self.cache['body'][content]
        else:
            self.body=create_text_image(content,600,600,font_path=self.font)
            self.cache['body'][content]=self.body
        self.display.frame_buf.paste(self.body, [0,200])
 

