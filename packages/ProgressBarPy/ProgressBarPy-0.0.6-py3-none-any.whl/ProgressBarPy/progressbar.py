import tkinter as tk
from tkinter import ttk
import tempfile
import base64
import zlib

from exceptions import InvalidMaxProgress

class ProgressBar:
    def __init__(self, maxprogress, title="Progress bar", message=None):
        self.max_progress = maxprogress
        if self.max_progress <= 0:
            raise InvalidMaxProgress(maxprogress)
        self.title = title
        self.message = message
        self.current_progress = 0

        self.progress_window = tk.Tk()
        self.progress_window.title(self.title)

        _, self.icon_path = tempfile.mkstemp()
        with open(self.icon_path, 'wb') as icon_file:
            icon_file.write(zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
                                                             'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc=')))
        self.progress_window.iconbitmap(self.icon_path)

        window_width = 300
        window_height = 50 if not self.message else 100

        screen_width = self.progress_window.winfo_screenwidth()
        screen_height = self.progress_window.winfo_screenheight()
        position_top = int((screen_height - window_height) / 2)
        position_right = int((screen_width - window_width) / 2)

        self.progress_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.progress_window.resizable(False, False)
        if self.message:
            self.label = tk.Label(self.progress_window, text=self.message)
            self.label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=250, mode="determinate",
                                            maximum=self.max_progress)
        self.progress_bar.pack(pady=10)
        self.progress_bar['value'] = self.current_progress

    def display(self):
        self.progress_window.update()

    def destroy(self):
        self.progress_window.destroy()


    def update(self, value=1):
        if self.current_progress < self.max_progress:
            self.current_progress += value
            self.progress_bar['value'] = self.current_progress
            self.progress_window.update_idletasks()


# test
if __name__ == "__main__":
    import time

    max_progress = 100
    progressbar = ProgressBar(maxprogress=max_progress, title='Progress bar example', message='Processing...')
    progressbar.display()
    for _ in range(max_progress + 1):
        time.sleep(0.05)
        progressbar.update()

    progressbar.destroy()