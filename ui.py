import os
import subprocess
import re
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListView
from ffmpeg_utils import video_exts, audio_exts, subtitle_exts, get_ffmpeg_path, generate_clean_movie_name

class DragDropList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setViewMode(QListView.ListMode)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                self.addItem(path)
            elif os.path.isdir(path):
                self.add_files_from_folder(path)

    def add_files_from_folder(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                if full_path.lower().endswith(video_exts + audio_exts + subtitle_exts):
                    self.addItem(full_path)

class ProcessThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, files, mode, delay, is_series=True):
        super().__init__()
        self.files = files
        self.mode = mode
        self.delay = delay
        self.is_series = is_series

    def run(self):
        processed = 0
        try:
            for i, file in enumerate(self.files):
                if file.lower().endswith(video_exts):
                    match = re.search(r"(s\d{2}e\d{2})", file, re.IGNORECASE)
                    if not match:
                        continue
                    tag = match.group(1).upper()
                    audio = next((f for f in self.files if f.lower().endswith(audio_exts) and tag in f.upper()), None)
                    subtitle = next((f for f in self.files if f.lower().endswith(subtitle_exts) and tag in f.upper()), None)
                    processed += self.run_ffmpeg(file, audio, subtitle)
                self.progress_signal.emit(int(((i + 1) / len(self.files)) * 100))
        finally:
            self.finished_signal.emit()

    def run_ffmpeg(self, video_path, audio_path, subtitle_path=None):
        delay = self.delay
        output_filename = generate_clean_movie_name(os.path.basename(video_path), self.mode)
        output_file = os.path.join(os.path.dirname(video_path), output_filename)

        delay_filter = ["-itsoffset", str(delay / 1000), "-i", audio_path] if audio_path else []
        subtitle_input = ["-i", subtitle_path] if subtitle_path else []

        map_options = ["-map", "0:v:0"]
        if self.mode == "dual" and audio_path:
            map_options += ["-map", "0:a:0", "-map", f"1:a:0"]
        elif audio_path:
            map_options += ["-map", f"1:a:0"]

        if subtitle_path:
            subtitle_input_index = 2 if audio_path else 1
            map_options += ["-map", f"{subtitle_input_index}:0"]

        command = [get_ffmpeg_path(), "-y", "-i", video_path] + delay_filter + subtitle_input + map_options + [
            "-c:v", "copy", "-c:a", "copy"
        ]

        if subtitle_path:
            ext = os.path.splitext(video_path)[1].lower()
            command += ["-c:s", "copy"] if ext == ".mkv" else ["-c:s", "mov_text"]
        else:
            command += ["-sn"]

        if self.mode == "dual":
            command += ["-metadata:s:a:0", "language=eng", "-metadata:s:a:1", "language=tur"]
            if subtitle_path:
                command += ["-metadata:s:s:0", "language=tur"]
        else:
            command += ["-metadata:s:a:0", "language=tur"]
            if subtitle_path:
                command += ["-metadata:s:s:0", "language=tur"]

        command.append(output_file)

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return 1
        except:
            return 0
