class VoiceController:
    def __init__(self, voices, start_key=None):
        self.voices = voices
        self.keys_iterator = iter(voices.keys())
        self.current_key = None

        if start_key and start_key in self.voices:
            while True:
                try:
                    self.current_key = next(self.keys_iterator)
                    if self.current_key == start_key:
                        break
                except StopIteration:
                    # Reset the iterator if the start_key is not found; this is a failsafe
                    self.keys_iterator = iter(self.voices.keys())
                    break
        # Optionally, handle the case where start_key is not in voices

    def next_voice(self):
        try:
            # Attempt to get the next key from the iterator
            self.current_key = next(self.keys_iterator)
        except StopIteration:
            # If the end is reached, reset the iterator and try to get the next key again
            self.keys_iterator = iter(self.voices.keys())
            try:
                self.current_key = next(self.keys_iterator)
            except StopIteration:
                # This ensures that if the dictionary is empty, the code does not fail
                self.current_key = None
        return self.current_key
