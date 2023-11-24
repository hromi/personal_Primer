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
    
    async def display_image(self, image_filename):
        # Load and display the image on e-ink screen
        display_image_8bpp(self.display, self.gfx_config['image_path']+image_filename)
    
    async def display_folio(self, message):
        #print(message)
        if 't' in message and message['t'] and message['t']!=self.pp.folio.title_text:
            self.title = FolioText((600,200), self.word_pointers)
            #first title
            font_size=int(sqrt(60000/(len(message['t'])+1)))
            font=self.emoji_font if 't_emoji' in message else self.font
            self.title.write_text('center',0, message['t'], font_filename=font, font_size=font_size, max_width=500, max_height=80, color=0)
            self.pp.folio.title_text=message['t']
            self.display.frame_buf.paste(self.title.image, [10,10])

        if 'b' in message and message['b'] and message['b']!=self.pp.folio.body_text:
            #then content
            self.body = FolioText((600,600), self.word_pointers)
            font_size=int(sqrt(150000/(len(message['b'])+1)))
            font=self.emoji_font if 'b_emoji' in message else self.font
            self.body.text_multiline(0,0, message['b'], font_filename=self.font, font_size=font_size, place='justify')
            self.pp.folio.body_text=message['b']
            self.display.frame_buf.paste(self.body.image, [10,200])

        if 'i' in message and message['i']!=self.pp.folio.image_name:
            display_image_8bpp(self.display, self.gfx_config['image_path']+message['i'])
            self.pp.folio.image_name=message['i']
            self.pp.folio.body_text=None

        self.display.draw_partial(constants.DisplayModes.DU)
 
    async def display_title(self, title, emoji=False):
        self.folio = FolioText((600,200), self.word_pointers)
        font_size=int(sqrt(60000/(len(title)+1)))
        font=self.emoji_font if emoji else self.font
        self.folio.write_text('center',0, title, font_filename=font, font_size=font_size, max_width=500, max_height=80, color=0)
        self.display.frame_buf.paste(self.folio.image, [10,50])
        self.display.draw_partial(constants.DisplayModes.DU,segment='title')
 
    async def clear_title(self):
        self.display.frame_buf.paste(self.white_title, [0,0])
        self.display.draw_partial(constants.DisplayModes.DU)
  
    async def clear_content(self):
        self.display.frame_buf.paste(self.white_content, [0,200])
        self.display.draw_partial(constants.DisplayModes.DU)
 

    async def display_body(self, content,emoji=False):
        self.folio = FolioText((600,600), self.word_pointers)
        font_size=int(sqrt(180000/(len(content)+1)))
        font=self.emoji_font if emoji else self.font
        self.folio.text_multiline(0,0, content, font_filename=self.font, font_size=font_size, place='justify')
        self.display.frame_buf.paste(self.folio.image, [10,200])
        self.display.draw_partial(constants.DisplayModes.DU)
 

