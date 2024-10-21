import pygame

class SoundPlayer:
    def __init__(self, sound_file):
        # Initialize Pygame mixer
        pygame.mixer.init()
        self.sound_file = sound_file
        self.sound = pygame.mixer.Sound(self.sound_file)
        self.channel = None

    def play(self):
        """Plays the sound."""
        if not self.channel or not self.channel.get_busy():
            self.channel = self.sound.play()

    def pause(self):
        """Pauses the sound if it's playing."""
        if self.channel and self.channel.get_busy():
            pygame.mixer.pause()

    def is_playing(self):
        """Checks if the sound is currently playing."""
        return self.channel and self.channel.get_busy()

    def resume(self):
        """Resumes the paused sound."""
        pygame.mixer.unpause()

    def stop(self):
        """Stops the sound."""
        if self.channel:
            self.sound.stop()
            self.channel = None

    def set_volume(self, volume):
        """Sets the volume of the sound. Volume should be between 0.0 and 1.0."""
        self.sound.set_volume(volume)

    def get_volume(self):
        """Returns the current volume of the sound."""
        return self.sound.get_volume()
