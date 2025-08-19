import tkinter as tk
from tkinter import filedialog
import pygame
import os

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("500x300")
        self.configure(bg="#f0f0f0")

        # Initialize PyGame mixer
        pygame.mixer.init()

        # Create widgets
        self.file_label = tk.Label(self, text="Select Audio File", font=('Arial', 16), bg="#f0f0f0")
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_music, bg="#4caf50", fg="white", font=('Arial', 12, 'bold'), relief=tk.FLAT)
        self.play_button = tk.Button(self, text='Play', command=self.play_music, state='disabled', bg="#2196f3", fg="white", font=('Arial', 12, 'bold'), relief=tk.FLAT)
        self.pause_button = tk.Button(self, text='Pause', command=self.pause_music, state='disabled', bg="#ff9800", fg="white", font=('Arial', 12, 'bold'), relief=tk.FLAT)
        self.stop_button = tk.Button(self, text='Stop', command=self.stop_music, state='disabled', bg="#f44336", fg="white", font=('Arial', 12, 'bold'), relief=tk.FLAT)

        # Pack widgets
        self.file_label.pack(pady=10)
        self.browse_button.pack(pady=5, padx=20, fill=tk.X)
        self.play_button.pack(pady=5, padx=20, fill=tk.X)
        self.pause_button.pack(pady=5, padx=20, fill=tk.X)
        self.stop_button.pack(pady=5, padx=20, fill=tk.X)

        # Initialize variables
        self.current_file = None
        self.playing = False

    def browse_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.current_file = file_path
            self.file_label.config(text=f"Selected Audio File: {self.current_file}")
            self.play_button.config(state='normal')
            self.pause_button.config(state='disabled')
            self.stop_button.config(state='disabled')
            self.playing = False

    def play_music(self):
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play(-1)
            self.play_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.stop_button.config(state='normal')
            self.playing = True

    def pause_music(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.config(state='normal')
            self.pause_button.config(state='disabled')
            self.playing = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.play_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.stop_button.config(state='disabled')
        self.playing = False

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
