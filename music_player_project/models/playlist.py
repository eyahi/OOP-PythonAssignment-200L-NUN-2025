
import random

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def shuffle(self):
        random.shuffle(self.songs)

    def repeat(self):
        self.songs *= 2

    def play_playlist(self):
        for song in self.songs:
            song.play()
