from math import sqrt
from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    lines = []
    if not text:
        return lines
    words = text.split()
    while words:
        line = ' '
        while words and font.getsize(line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def draw_outline(draw, position, text, font, outline_width, outline_color):
    x, y = position
    # Draw text in outline mode by drawing it in several positions
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

def create_text_image(text, image_width, image_height, font_path, font_size=70, outline=False):
    font = ImageFont.truetype(font_path, font_size)
    if not text:
        text = " "
    font_size/=sqrt(len(text))
    font_size=int(font_size)+50
    print(font_size)
    """Create an image with text nicely typeset to fit within the given dimensions."""
    font = ImageFont.truetype(font_path, font_size)
    lines = wrap_text(text, font, image_width)

    text_height = len(lines) * font.getsize(text)[1]
    # Adjust font size and re-wrap text until it fits the image height
    while text_height > image_height and font_size > 1:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(text, font, image_width)
        text_height = len(lines) * font.getsize(lines[0])[1]

    font = ImageFont.truetype(font_path, font_size)
    img = Image.new('1', (image_width, image_height), color=255)
    draw = ImageDraw.Draw(img)
    y = (image_height - text_height) / 2  # Start y position to center the text vertically

    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x = (image_width - line_width) / 2  # Center each line

        words = line.split()
        word_x = x
        for word in words:
            idx = 0
            while idx < len(word):
                if idx > 0 and word[idx].isupper() and outline:
                    # Draw the outline part
                    outline_text = word[idx].lower()
                    outline_font = ImageFont.truetype(font_path, font_size)
                    draw_outline(draw, (word_x, y), outline_text, outline_font, outline_width=1, outline_color=0)
                    draw.text((word_x, y), outline_text, fill=255, font=outline_font)
                    word_x += font.getsize(outline_text)[0]
                else:
                    draw.text((word_x, y), word[idx], fill=0, font=font)
                    word_x += font.getsize(word[idx])[0]
                idx += 1
            word_x += font.getsize(' ')[0]

        y += font_size
    return img
