
import tkinter as tk
from tkinter import filedialog, messagebox
from models.music_player import MusicPlayer
from models.song import Song
from models.playlist import Playlist
from audio.player import init_audio

class MusicPlayerGUI:
    def __init__(self, root):
        init_audio()
        self.root = root
        self.root.title("Python Music Player")

        self.player = MusicPlayer()
        self.playlist = Playlist("GUI Playlist")

        self.song_listbox = tk.Listbox(root, width=60)
        self.song_listbox.pack(pady=10)

        control_frame = tk.Frame(root)
        control_frame.pack()

        self.play_button = tk.Button(control_frame, text="Play", command=self.play_song)
        self.pause_button = tk.Button(control_frame, text="Pause", command=self.pause_song)
        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_song)
        self.next_button = tk.Button(control_frame, text="Next", command=self.next_song)
        self.prev_button = tk.Button(control_frame, text="Previous", command=self.prev_song)
        self.add_button = tk.Button(root, text="Add Song", command=self.add_song)

        for btn in [self.play_button, self.pause_button, self.stop_button, self.next_button, self.prev_button]:
            btn.pack(side=tk.LEFT, padx=5, pady=5, in_=control_frame)

        self.add_button.pack(pady=5)

    def add_song(self):
        file_path = filedialog.askopenfilename(title="Select Audio File",
                                               filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if file_path:
            title = file_path.split("/")[-1]
            new_song = Song(title=title, artist="Unknown", album="Unknown", duration="Unknown", file_path=file_path)
            self.playlist.add_song(new_song)
            self.song_listbox.insert(tk.END, new_song.title)

    def play_song(self):
        index = self.song_listbox.curselection()
        if not index:
            messagebox.showwarning("Select Song", "Please select a song to play.")
            return
        self.player.load_playlist(self.playlist)
        self.player.current_index = index[0]
        self.player.play()

    def pause_song(self):
        self.player.pause()

    def stop_song(self):
        self.player.stop()

    def next_song(self):
        self.player.next_song()
        self.song_listbox.selection_clear(0, tk.END)
        self.song_listbox.selection_set(self.player.current_index)

    def prev_song(self):
        self.player.previous_song()
        self.song_listbox.selection_clear(0, tk.END)
        self.song_listbox.selection_set(self.player.current_index)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MusicPlayerGUI(root)
    root.mainloop()
