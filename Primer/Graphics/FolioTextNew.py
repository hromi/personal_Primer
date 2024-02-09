from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getsize(line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def create_text_image(text, image_width, image_height, font_path='arial.ttf'):
    """Create an image with text nicely typeset to fit within the given dimensions."""
    font_size = 70  # Starting font size
    font = ImageFont.truetype(font_path, font_size)
    lines = wrap_text(text, font, image_width)
    text_height = len(lines) * font.getsize(text)[1]
    
    # Adjust font size and re-wrap text until it fits the image height
    while (text_height > image_height and font_size > 1):
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(text, font, image_width)
        text_height = len(lines) * font.getsize(lines[0])[1]
    
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new('1', (image_width, image_height),color=255)
    draw = ImageDraw.Draw(img)
    y = (image_height - text_height) / 2  # Start y position to center the text vertically
    
    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x = (image_width - line_width) / 2  # Center each line
        draw.text((x, y), line, fill=0, font=font)
        #y += line_height
        y += font_size
    
    return img

