
from audio.player import init_audio
import sys

def launch_cli():
    from models.song import Song
    from models.playlist import Playlist
    from models.music_player import MusicPlayer
    from ui.cli import UserInterface
    import os

    init_audio()
    ui = UserInterface()
    player = MusicPlayer()

    sample_songs = [
        Song("Blinding Lights", "The Weeknd", "After Hours", "3:20", "audio/blinding_lights.mp3"),
        Song("Shape of You", "Ed Sheeran", "Divide", "3:53", "audio/shape_of_you.mp3")
    ]

    playlist = Playlist("My Playlist")
    for song in sample_songs:
        if os.path.exists(song.file_path):
            playlist.add_song(song)
        else:
            print(f"⚠️ File not found: {song.file_path}")

    player.load_playlist(playlist)

    while True:
        ui.display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            player.play()
            ui.display_current_song(playlist.songs[player.current_index])
        elif choice == "2":
            player.pause()
        elif choice == "3":
            player.stop()
        elif choice == "4":
            player.next_song()
            ui.display_current_song(playlist.songs[player.current_index])
        elif choice == "5":
            player.previous_song()
            ui.display_current_song(playlist.songs[player.current_index])
        elif choice == "6":
            print("Exiting music player...")
            break
        else:
            print("Invalid choice. Please try again.")

def launch_gui():
    from ui.gui import MusicPlayerGUI
    import tkinter as tk

    init_audio()
    root = tk.Tk()
    gui = MusicPlayerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("Select interface:")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical Interface (GUI)")
    interface = input("Enter choice (1 or 2): ").strip()

    if interface == "1":
        launch_cli()
    elif interface == "2":
        launch_gui()
    else:
        print("Invalid input. Exiting...")
        sys.exit(1)
