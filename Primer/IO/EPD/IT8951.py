import asyncio
from math import sqrt
#from IT8951 import display
from sys import path
from IT8951 import constants
from IT8951.EPD_functions import *
from IT8951.display import AutoEPDDisplay
from Primer.Graphics.FolioText import FolioText
from PIL import Image,ImageDraw,ImageFont

import asyncio
import yaml

class EInkDisplay:
    def __init__(self,config):
        self.driver_config = config['EPD']
        self.gfx_config = config['gfx']
        self.display = AutoEPDDisplay(
            vcom=self.driver_config['vcom'],
            rotate=self.driver_config['rotate'],
            spi_hz=self.driver_config['spi_hz']
        )
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
        self.font=self.gfx_config['font']
        self.emoji_font=self.gfx_config['emoji']
        self.word_pointers=[]
        self.folio = FolioText((int(self.display.height),int(self.display.width/1)), self.word_pointers)
        self.white_title = Image.new("1",(600,200),255) 
        self.black_title = Image.new("1",(600,200),0) 
        self.black_content = Image.new("1",(600,600),0) 
        self.white_content = Image.new("1",(600,600),255) 

    async def display_folio(self, content, image_filename=None):
        # If there's an image filename provided, display the image
        print(content)
        await self.display_text(content)
        if image_filename:
            await self.display_image(image_filename)
    
    async def display_image(self, image_filename):
        # Load and display the image on e-ink screen
        display_image_8bpp(self.display, self.gfx_config['image_path']+image_filename)
    
    async def display_title(self, title, emoji=False):
        # Display text on e-ink screen
        # Note: Implement the logic based on your e-ink display's library
        self.folio = FolioText((600,200), self.word_pointers)
        font_size=int(sqrt(60000/(len(title)+1)))

        font=self.emoji_font if emoji else self.font

        self.folio.write_text('center',0, title, font_filename=font, font_size=font_size, max_width=500, max_height=80, color=0)
        self.display.frame_buf.paste(self.folio.image, [10,50])
        self.display.draw_partial(constants.DisplayModes.DU)
 
    async def clear_title(self):
        self.display.frame_buf.paste(self.white_title, [0,0])
        self.display.draw_partial(constants.DisplayModes.DU)
  
    async def clear_content(self):
        self.display.frame_buf.paste(self.white_content, [0,200])
        self.display.draw_partial(constants.DisplayModes.DU)
 

    async def display_content(self, content):
        #print("DISPLAYNAME"+content)
        # Display text on e-ink screen
        # Note: Implement the logic based on your e-ink display's library
        self.folio = FolioText((600,600), self.word_pointers)
        font_size=int(sqrt(180000/(len(content)+1)))
        self.folio.text_multiline(0,0, content, font_filename=self.font, font_size=font_size, place='justify')
        self.display.frame_buf.paste(self.folio.image, [10,200])
        self.display.draw_partial(constants.DisplayModes.DU)

