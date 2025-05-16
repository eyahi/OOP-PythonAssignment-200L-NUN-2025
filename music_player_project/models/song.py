
import pygame

class Song:
    def __init__(self, title, artist, album, duration, file_path):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.file_path = file_path

    def play(self):
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()
