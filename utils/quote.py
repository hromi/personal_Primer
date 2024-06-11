import sys
root_dir='/home/fibel/personal_Primer'
sys.path.append(root_dir)

import asyncio
from Primer.Graphics.QuoteDisplayer import QuoteDisplayer

from PIL import Image, ImageDraw, ImageFont
if __name__ == "__main__":
    config_path = f'{root_dir}/primer.yaml'
    json_path = f'{root_dir}/assets/quotes.json'
    quote_displayer = QuoteDisplayer(config_path, json_path)
    asyncio.run(quote_displayer.display_quote())