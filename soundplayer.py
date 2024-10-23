import pygame

class SoundPlayer:
    def __init__(self, sound_file):
        pygame.mixer.init()
        self.sound_file = sound_file
        self.sound = pygame.mixer.Sound(self.sound_file)
        print(sound_file + " loaded!")
        self.channel = None

    def play(self):
        if not self.channel or not self.channel.get_busy():
            self.channel = self.sound.play()

    def pause(self):
        if self.channel and self.channel.get_busy():
            pygame.mixer.pause()

    def is_playing(self):
        return self.channel and self.channel.get_busy()

    def resume(self):
        pygame.mixer.unpause()

    def stop(self):
        if self.channel:
            self.sound.stop()
            self.channel = None

    def set_volume(self, volume):
        self.sound.set_volume(volume)

    def get_volume(self):
        return self.sound.get_volume()
