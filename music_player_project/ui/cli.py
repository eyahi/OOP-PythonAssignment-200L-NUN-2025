
class UserInterface:
    def display_menu(self):
        print("1. Play\n2. Pause\n3. Stop\n4. Next\n5. Previous\n6. Exit")

    def display_current_song(self, song):
        print(f"Now Playing: {song.title} - {song.artist}")

    def display_playlist(self, playlist):
        print("Playlist:")
        for song in playlist.songs:
            print(f"- {song.title} by {song.artist}")
