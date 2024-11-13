#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
import random
from pathlib import Path

class MTSP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MTSP v0.1.4")
        self.root.configure(bg='black')
        self.root.minsize(400, 500)  # Set minimum window size
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # Initialize variables
        self.current_track = -1
        self.is_playing = False
        self.playlist = []
        self.volume = 1.0
        self.repeat = False
        self.shuffle = False
        
        # Set up end of track event
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.setup_ui()
        self.setup_event_handler()
    
    def setup_event_handler(self):
        def check_music_end():
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.handle_track_end()
            self.root.after(100, check_music_end)
        
        self.root.after(100, check_music_end)
    
    def handle_track_end(self):
        if self.repeat:
            self.play_track(self.current_track)
        elif self.shuffle:
            next_track = random.randint(0, len(self.playlist) - 1)
            while next_track == self.current_track and len(self.playlist) > 1:
                next_track = random.randint(0, len(self.playlist) - 1)
            self.play_track(next_track)
        else:
            if self.current_track < len(self.playlist) - 1:
                self.play_track(self.current_track + 1)
            else:
                self.stop_playback()
    
    def setup_ui(self):
        # ASCII Art Logo
        ascii_art = """
        ███╗   ███╗████████╗███████╗██████╗ 
        ████╗ ████║╚══██╔══╝██╔════╝██╔══██╗
        ██╔████╔██║   ██║   ███████╗██████╔╝
        ██║╚██╔╝██║   ██║   ╚════██║██╔═══╝ 
        ██║ ╚═╝ ██║   ██║   ███████║██║     
        ╚═╝     ╚═╝   ╚═╝   ╚══════╝╚═╝     
        """
        art_label = tk.Label(self.root, text=ascii_art, fg='#00ff00', bg='black', font=('Courier', 10))
        art_label.pack(pady=10)
        
        # Main Controls Frame
        controls_frame = tk.Frame(self.root, bg='black')
        controls_frame.pack(pady=10)
        
        # Control Buttons
        style = ttk.Style()
        style.configure('Custom.TButton', padding=5)
        
        prev_btn = tk.Button(controls_frame, text="◀◀", command=self.previous_track,
                            width=3, height=1)
        prev_btn.pack(side=tk.LEFT, padx=2)
        
        self.play_button = tk.Button(controls_frame, text="▶", command=self.toggle_play,
                                   width=3, height=1)
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        next_btn = tk.Button(controls_frame, text="▶▶", command=self.next_track,
                            width=3, height=1)
        next_btn.pack(side=tk.LEFT, padx=2)
        
        # Shuffle and Repeat Buttons
        self.shuffle_btn = tk.Button(controls_frame, text="🔀", command=self.toggle_shuffle,
                                   width=3, height=1)
        self.shuffle_btn.pack(side=tk.LEFT, padx=2)
        
        self.repeat_btn = tk.Button(controls_frame, text="🔁", command=self.toggle_repeat,
                                  width=3, height=1)
        self.repeat_btn.pack(side=tk.LEFT, padx=2)
        
        # Volume Control
        volume_frame = tk.Frame(self.root, bg='black')
        volume_frame.pack(pady=5)
        
        tk.Label(volume_frame, text="🔈", bg='black', fg='#00ff00').pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=100)
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, variable=self.volume_var,
                                command=self.change_volume, orient=tk.HORIZONTAL, length=200)
        volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(volume_frame, text="🔊", bg='black', fg='#00ff00').pack(side=tk.LEFT)
        
        # Track Information Display
        self.track_info = tk.Label(self.root, text="No track playing", fg='#00ff00',
                                 bg='black', font=('Arial', 10, 'bold'), wraplength=350)
        self.track_info.pack(pady=5)
        
        # Playlist Area
        playlist_frame = tk.Frame(self.root, bg='black', bd=1)
        playlist_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        # Scrollbar for playlist
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Playlist listbox
        self.playlist_box = tk.Listbox(playlist_frame, bg='black', fg='#00ff00',
                                     selectmode=tk.SINGLE, yscrollcommand=scrollbar.set,
                                     font=('Arial', 9), selectbackground='#004400',
                                     selectforeground='#ffffff', height=10)
        self.playlist_box.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_box.yview)
        
        # Bind double-click in playlist
        self.playlist_box.bind('<Double-Button-1>', lambda e: self.play_selected())
        
        # File Control Buttons
        file_frame = tk.Frame(self.root, bg='black')
        file_frame.pack(pady=10)
        
        tk.Button(file_frame, text="Add Files", command=self.add_files,
                 width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Load Playlist", command=self.load_playlist,
                 width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Save Playlist", command=self.save_playlist,
                 width=10).pack(side=tk.LEFT, padx=2)
        
    def toggle_play(self):
        if not self.playlist:
            return
            
        if self.current_track == -1:
            self.play_track(0)
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_button.config(text="▶")
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.play_button.config(text="⏸")
            self.is_playing = True
    
    def play_track(self, index):
        if not 0 <= index < len(self.playlist):
            return
            
        try:
            pygame.mixer.music.load(self.playlist[index])
            pygame.mixer.music.play()
            self.current_track = index
            self.is_playing = True
            self.play_button.config(text="⏸")
            
            # Update UI
            self.track_info.config(text=f"Now Playing: {os.path.basename(self.playlist[index])}")
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(index)
            self.playlist_box.see(index)
            
        except pygame.error as e:
            self.track_info.config(text=f"Error playing track: {str(e)}")
            
    def play_selected(self):
        selection = self.playlist_box.curselection()
        if selection:
            self.play_track(selection[0])
    
    def stop_playback(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.config(text="▶")
        self.track_info.config(text="No track playing")
    
    def previous_track(self):
        if not self.playlist:
            return
            
        if self.shuffle:
            self.play_track(random.randint(0, len(self.playlist) - 1))
        else:
            new_index = self.current_track - 1 if self.current_track > 0 else len(self.playlist) - 1
            self.play_track(new_index)
    
    def next_track(self):
        if not self.playlist:
            return
            
        if self.shuffle:
            next_track = random.randint(0, len(self.playlist) - 1)
            while next_track == self.current_track and len(self.playlist) > 1:
                next_track = random.randint(0, len(self.playlist) - 1)
            self.play_track(next_track)
        else:
            self.play_track((self.current_track + 1) % len(self.playlist))
    
    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        self.shuffle_btn.config(bg='#004400' if self.shuffle else 'SystemButtonFace')
    
    def toggle_repeat(self):
        self.repeat = not self.repeat
        self.repeat_btn.config(bg='#004400' if self.repeat else 'SystemButtonFace')
    
    def change_volume(self, value):
        try:
            self.volume = float(value) / 100
            pygame.mixer.music.set_volume(self.volume)
        except:
            pass
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            if os.path.exists(file):
                self.playlist.append(file)
                self.playlist_box.insert(tk.END, os.path.basename(file))
    
    def save_playlist(self):
        if not self.playlist:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".m3u",
            filetypes=[("M3U Playlist", "*.m3u"), ("Text File", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for track in self.playlist:
                        f.write(f"{track}\n")
            except Exception as e:
                self.track_info.config(text=f"Error saving playlist: {str(e)}")
    
    def load_playlist(self):
        file_path = filedialog.askopenfilename(
            title="Load Playlist",
            filetypes=[
                ("M3U Playlist", "*.m3u"),
                ("Text File", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.playlist = []
                    self.playlist_box.delete(0, tk.END)
                    
                    for line in f:
                        track_path = line.strip()
                        if track_path and os.path.exists(track_path):
                            self.playlist.append(track_path)
                            self.playlist_box.insert(tk.END, os.path.basename(track_path))
                
                self.current_track = -1
                self.stop_playback()
            except Exception as e:
                self.track_info.config(text=f"Error loading playlist: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = MTSP()
        app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
