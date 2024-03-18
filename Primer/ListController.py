import os
class ListController:
    def __init__(self, font_path, voices, start_voice=None, start_font=None):
        self.voices = voices
        self.voices_iterator = iter(voices.keys())
        self.current_voice = None
        self.current_font = None
        self.fonts={}
        self.populate_fonts_from_directory(font_path,'open')
        self.populate_fonts_from_directory(font_path,'licensed')
        print(self.fonts)
        self.fonts_iterator = iter(self.fonts.keys())

        #VOICE RELATED
        if start_voice and start_voice in self.voices:
            while True:
                try:
                    self.current_voice = next(self.voices_iterator)
                    if self.current_voice == start_voice:
                        break
                except StopIteration:
                    # Reset the iterator if the start_voice is not found; this is a failsafe
                    self.voices_iterator = iter(self.voices.keys())
                    break
        # Optionally, handle the case where start_voice is not in voices

    def populate_fonts_from_directory(self, directory, prefix=''):
        """
        Populates the fonts dictionary with font files from the specified directory.
        
        :param directory: The directory to scan for font files.
        :param prefix: The prefix to add before the font file path (e.g., 'open/' or 'licensed/').
        """
        for item in os.listdir(f'{directory}/{prefix}'):
            # Construct full path to item
            full_path = os.path.join(directory, prefix,item)
            print(full_path)
            # Check if it's a file
            if os.path.isfile(full_path):
                # Extract the file name without extension
                font_name, extension = os.path.splitext(item)
                if extension in ['.ttf', '.otf']:
                    # Use file name as key and full path as value
                    self.fonts[font_name] = f'{prefix}/{item}'
                    print(f'{prefix}/{item}')

    def next_voice(self):
        try:
            # Attempt to get the next key from the iterator
            self.current_voice = next(self.voices_iterator)
        except StopIteration:
            # If the end is reached, reset the iterator and try to get the next key again
            self.voices_iterator = iter(self.voices.keys())
            try:
                self.current_voice = next(self.voices_iterator)
            except StopIteration:
                # This ensures that if the dictionary is empty, the code does not fail
                self.current_voice = None
        return self.current_voice

        #FONT RELATED
        if start_font and start_font in self.fonts:
            while True:
                try:
                    self.current_font = next(self.fonts_iterator)
                    if self.current_font == start_font:
                        break
                except StopIteration:
                    # Reset the iterator if the start_font is not found; this is a failsafe
                    self.fonts_iterator = iter(self.fonts.keys())
                    break
        # Optionally, handle the case where start_font is not in fonts

    def next_font(self):
        try:
            # Attempt to get the next key from the iterator
            self.current_font = next(self.fonts_iterator)
        except StopIteration:
            # If the end is reached, reset the iterator and try to get the next key again
            self.fonts_iterator = iter(self.fonts.keys())
            try:
                self.current_font = next(self.fonts_iterator)
            except StopIteration:
                # This ensures that if the dictionary is empty, the code does not fail
                self.current_font = None
        return self.fonts[self.current_font]
