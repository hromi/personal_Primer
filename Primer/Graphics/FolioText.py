#!/usr/bin/env python
# coding: utf-8

# Requirement: PIL <http://www.pythonware.com/products/pil/>
# Copyright 2011 Álvaro Justen [alvarojusten at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

from PIL import Image,ImageDraw,ImageFont

class FolioText(object):
    def __init__(self, filename_or_size, pointers, mode='1', background=255, encoding='utf8'):
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding
        self.pointers = pointers

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, x, y, text, font_filename, font_size=11,
                   max_width=None, max_height=None, color=0):
        #if isinstance(text, str):
        #    text = text.decode(self.encoding)
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font)
        #self.draw_text(x, y, text, font=font, outline_width=3)
        #print(x,y)
        # print(int(text_size[0]),int(text_size[1]))
        # self.display.load_image(x,y,image,img_addr=pageList(self.display.img_addr,0))
        # self.display.display_buffer_area(x,y,text_size[0],text_size[1],2,pageList(img_addr,num_img))
        # print(text)
        # print(int(x),int(y),int(text_size[0]), int(text_size[1]))
        self.pointers.append((int(x),int(y),int(text_size[0]), int(text_size[1]),text))
        return text_size

    # Function to find the last vowel in a word
    def find_last_vowel(self,word):
        vowels = 'aeiouAEIOU'
        last_vowel_index = None
        for index, char in enumerate(word):
            if char in vowels:
                last_vowel_index = index
        return last_vowel_index

    # Function to draw text with the last vowel outlined
    def draw_text(self, x,y, word, font, outline_width=1):
        #text_width, text_height = ImageDraw.Draw(Image.new('RGB', (1, 1))).multiline_textsize(word, font)
        #image = Image.new('RGB', (text_width, text_height), 'white')
        #draw = ImageDraw.Draw(image)
    
        # Draw the entire word
        self.draw.text((x, y), word, font=font, fill='black')
    
        # Find the position of the last vowel
        last_vowel_index = self.find_last_vowel(word)
        if last_vowel_index is not None:
            prefix_width, _ = self.draw.textsize(word[:last_vowel_index], font=font)
            vowel_width, _ = self.draw.textsize(word[last_vowel_index], font=font)
        
        # Redraw the last vowel with an outline
        self.draw.text((x+prefix_width, 0), word[last_vowel_index], font=font, fill='white', stroke_width=outline_width, stroke_fill='black')
        #self.draw.text((prefix_width, 0), word[last_vowel_index], font=font, fill='black')
    
        # Show the image
        #return image

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def text_multiline(self, x, y, text, font_filename, font_size=11, box_width=580, color=0, place='justify', justify_last_line=False):
        lines = []
        line = []
        words = text.split(' ')
        for word in words:
            print(word)
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            if word!="\n" and size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        height = y
        for index, line in enumerate(lines):
            height += text_height
            if place == 'left':
                self.write_text(x, height, line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                ##### check with daniel what these lines are for
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text(x, height, line, font_filename, font_size,
                                    color)
                    continue
                #######
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:    #why words[:-1]
                    self.write_text(start_x, height, word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    print(start_x,word_size[0],space_width)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text(last_word_x, height, words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)
