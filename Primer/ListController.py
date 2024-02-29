class ListController:
    def __init__(self, voices, start_voice=None, start_font=None):
        self.voices = voices
        self.fonts={'Great Vibes':'open/GreatVibes-Regular.ttf','Miama':'open/Miama.ttf','Schola':'open/schola.ttf','Samarkan':'licensed/samarkan.ttf'}
        self.voices_iterator = iter(voices.keys())
        self.fonts_iterator = iter(self.fonts.keys())
        self.current_voice = None
        self.current_font = None

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
