import json
from IT8951 import constants
import random
import os
import asyncio
from Primer.IO.EPD.IT8951 import EInkDisplay
from Primer.Folio import Folio
from PIL import Image, ImageDraw, ImageFont

class QuoteDisplayer():
    def __init__(self, config_path, json_path):
        import yaml
        self.json_path=json_path
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.font=self.config['gfx']['font']
        self.font_path=self.config['gfx']['font_path']
        self.display = EInkDisplay(self)

    async def display_quote(self):
        # Load quotes from JSON file
        with open(self.json_path, 'r') as file:
            quotes = json.load(file)

        # Pick a random quote to display
        quote = random.choice(quotes)
        print(quote)
        text = f'"{quote["quote"]}"\n\n- {quote["author_of_quote"]}'

        # Display the quote on the e-ink screen
        #await self.display.display_folio({'b':text})
        await self.display.display_body(text)
        self.display.display.draw_partial(constants.DisplayModes.DU)