import pygame
import os
import time


class VoiceAlert:

    def __init__(self, language="english"):

        pygame.mixer.init()

        self.base = os.path.join(
            os.path.dirname(__file__),
            "sounds"
        )
 
        self.language = language.lower()

        self.last_warning = 0
        self.last_critical = 0
        self.last_missing = 0

        # Critical waits for warning audio
        self.critical_pending = False

        self.load_language()

    # ---------------------------------
    # Load selected language
    # ---------------------------------

    def load_language(self):

        language_folder = os.path.join(
            self.base,
            self.language
        )

        self.warning = os.path.join(
            language_folder,
            "warning.mp3"
        )

        self.critical = os.path.join(
            language_folder,
            "critical.mp3"
        )

        self.missing = os.path.join(
            language_folder,
            "missing.mp3"
        )

    # ---------------------------------
    # Change language
    # ---------------------------------

    def set_language(self, language):

        self.language = language.lower()

        self.load_language()

        print(
            "Voice Language :",
            self.language.upper()
        )

    # ---------------------------------
    # Check audio playing
    # ---------------------------------

    def is_playing(self):

        return pygame.mixer.music.get_busy()

    # ---------------------------------
    # Play audio
    # ---------------------------------

    def play(self, file):

        if not os.path.exists(file):

            print(
                "Voice file not found:",
                file
            )

            return False

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        return True

    # ---------------------------------
    # Update audio queue
    # ---------------------------------

    def update(self):

        # If audio is still playing,
        # do nothing
        if self.is_playing():

            return

        # Warning has finished.
        # Now play pending Critical.
        if self.critical_pending:

            self.critical_pending = False

            self.play(self.critical)

    # ---------------------------------
    # Warning
    # ---------------------------------

    def speak_warning(self):

        now = time.time()

        if now - self.last_warning < 8:

            return

        self.last_warning = now

        # Never interrupt another audio
        if self.is_playing():

            return

        self.play(self.warning)

    # ---------------------------------
    # Critical
    # ---------------------------------

    def speak_critical(self):

        now = time.time()

        if now - self.last_critical < 5:

            return

        self.last_critical = now

        # If Warning is playing,
        # Critical waits for it.
        if self.is_playing():

            self.critical_pending = True

            return

        # Nothing is playing
        self.play(self.critical)

    # ---------------------------------
    # Missing Driver
    # ---------------------------------

    def speak_missing(self):

        now = time.time()

        if now - self.last_missing < 8:

            return

        self.last_missing = now

        # Never interrupt another audio
        if self.is_playing():

            return

        self.play(self.missing)