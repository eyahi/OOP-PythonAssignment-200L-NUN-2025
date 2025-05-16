
class MusicPlayer:
    def __init__(self):
        self.current_playlist = None
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False

    def load_playlist(self, playlist):
        self.current_playlist = playlist
        self.current_index = 0

    def play(self):
        if self.current_playlist:
            self.is_playing = True
            self.current_playlist.songs[self.current_index].play()

    def pause(self):
        self.is_paused = True
        self.current_playlist.songs[self.current_index].pause()

    def stop(self):
        self.is_playing = False
        self.current_playlist.songs[self.current_index].stop()

    def next_song(self):
        self.current_index = (self.current_index + 1) % len(self.current_playlist.songs)
        self.play()

    def previous_song(self):
        self.current_index = (self.current_index - 1) % len(self.current_playlist.songs)
        self.play()
