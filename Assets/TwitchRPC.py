import json
import logging
import threading
import time

import customtkinter as ctk
from pypresence import Presence

from Assets.TwitchRPCbk import get_twitch_title

CONFIG_FILE = 'config.json'


class TwitchRichPresence(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.tabs_frame = None
        self.save_button = None
        self.client_id_entry = None
        self.tab_frames = None
        self.content_frame = None
        self.title("Twitch Rich Presence")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.client_id = None
        self.load_config()

        self.create_tabs()

        self.running = False
        self.thread = None
        self.start_time = None

    def create_tabs(self):
        self.tabs_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.tabs_frame.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.tab_frames = {
            "home": ctk.CTkFrame(self.content_frame),
            "config": ctk.CTkFrame(self.content_frame)
        }

        self.create_tab_button("Home", self.tabs_frame, self.tab_frames["home"])
        self.create_tab_button("Configuration", self.tabs_frame, self.tab_frames["config"])

        for name, frame in self.tab_frames.items():
            frame.pack(side="top", fill="both", expand=True)
            if name == "config":
                self.add_config_content(frame)
            elif name == "home":
                self.add_home_content(frame)

        self.raise_frame(self.tab_frames["home"])

    def create_tab_button(self, text, parent, frame):
        button = ctk.CTkButton(parent, text=text, command=lambda: self.raise_frame(frame))
        button.pack(pady=10, padx=10, fill="x")

    def add_home_content(self, frame):
        ctk.CTkLabel(frame, text="Twitch Rich Presence Control").pack(pady=20)

        start_button = ctk.CTkButton(frame, text="Start", command=self.start_presence)
        start_button.pack(pady=10)

        stop_button = ctk.CTkButton(frame, text="Stop", command=self.stop_presence)
        stop_button.pack(pady=10)

    def add_config_content(self, frame):
        ctk.CTkLabel(frame, text="Configuration").pack(pady=20)

        self.client_id_entry = ctk.CTkEntry(frame, placeholder_text="Enter Discord Client ID")
        if self.client_id:
            self.client_id_entry.insert(0, self.client_id)
        self.client_id_entry.pack(pady=10)

        self.save_button = ctk.CTkButton(frame, text="Save", command=self.save_config)
        self.save_button.pack(pady=10)

    def raise_frame(self, frame):
        frame.tkraise()
        for tab_frame in self.tab_frames.values():
            tab_frame.pack_forget()
        frame.pack(side="top", fill="both", expand=True)

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                self.client_id = config.get('client_id')
        except (FileNotFoundError, json.JSONDecodeError):
            self.client_id = None

    def save_config(self):
        self.client_id = self.client_id_entry.get()
        with open(CONFIG_FILE, 'w') as file:
            json.dump({'client_id': self.client_id}, file)

    def start_presence(self):
        if not self.running and self.client_id:
            self.client = Presence(self.client_id)
            self.running = True
            self.thread = threading.Thread(target=self.run_presence, daemon=True)
            self.thread.start()

    def stop_presence(self):
        if self.running:
            self.running = False
            self.client.clear()
            self.client.close()

    def update_presence(self, streamer_name, status):
        if status == "On Twitch":
            self.client.update(
                details="On Twitch",
                state=f"Time Elapsed: {self.format_time_elapsed()}",
                large_image="twitch",
                small_image="twitch",
                small_text="Twitch"
            )
        elif streamer_name:
            # Convert streamer name to lowercase for asset matching
            lower_streamer_name = streamer_name.lower()
            large_image = lower_streamer_name if self.client.is_asset(lower_streamer_name) else "twitch"
            small_image = "twitch" if large_image != "twitch" else None

            self.client.update(
                details=f"{status} {streamer_name}",
                state=f"Time Elapsed: {self.format_time_elapsed()}",
                large_image=large_image,
                small_image=small_image,
                small_text="Twitch" if small_image else None,
                buttons=[{"label": "Watch now on Twitch", "url": f"https://twitch.tv/{streamer_name}"}]
            )
        else:
            self.client.clear()

    def run_presence(self):
        try:
            self.client.connect()
            last_streamer_name = None
            while self.running:
                current_streamer_name, status = get_twitch_title()

                if current_streamer_name != last_streamer_name:
                    self.start_time = time.time()
                    last_streamer_name = current_streamer_name

                self.update_presence(current_streamer_name, status)
                time.sleep(1)  # Update every second
        except Exception as e:
            logging.error(f"Error in run_presence: {e}")

    def format_time_elapsed(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return "00:00:00"


def main():
    logging.basicConfig(level=logging.INFO)
    app = TwitchRichPresence()
    app.mainloop()


if __name__ == "__main__":
    main()
