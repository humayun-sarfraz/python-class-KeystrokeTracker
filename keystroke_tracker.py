import os
import sys
import time
import logging
import json
from pynput import keyboard
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from threading import Timer, Thread
import statistics

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class KeystrokeTracker:
    def __init__(self, save_interval=60):
        self.keystroke_counts = {}
        self.typing_speeds = []
        self.start_time = None
        self.keystroke_track_dir = get_resource_path('app/tests/keystroke-tracking')
        self.listener = None
        self.save_interval = save_interval
        self.timer = None
        self._create_directory()
        self._start_save_timer()

    def _create_directory(self):
        try:
            os.makedirs(self.keystroke_track_dir, exist_ok=True)
            logging.debug("Keystroke tracking directory created successfully.")
        except Exception as e:
            logging.error(f"Error creating keystroke tracking directory: {e}")

    def start_tracking(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.start_time = time.time()
        logging.debug("Keystroke tracking started.")

    def stop_tracking(self):
        if self.listener:
            self.listener.stop()
            logging.debug("Keystroke tracking stopped.")
        self.stop_timer()

    def on_key_press(self, key):
        try:
            key_str = key.char if hasattr(key, 'char') else str(key)
        except AttributeError:
            key_str = str(key)
        self.keystroke_counts[key_str] = self.keystroke_counts.get(key_str, 0) + 1
        self._update_typing_speed()

    def _update_typing_speed(self):
        elapsed_time = time.time() - self.start_time
        words_typed = sum(self.keystroke_counts.values()) / 5
        typing_speed = (words_typed / elapsed_time) * 60
        self.typing_speeds.append(typing_speed)

    def save_keystroke_track(self):
        if not self.keystroke_counts:
            logging.debug("No keystrokes to save.")
            return
        timestamp = int(time.time())
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_path = os.path.join(self.keystroke_track_dir, f'keystroke_track_{timestamp}.png')
        json_path = os.path.join(self.keystroke_track_dir, f'keystroke_track_{timestamp}.json')
        self._save_keystroke_image(image_path, current_time)
        self._save_keystroke_json(json_path, current_time)
        self.keystroke_counts = {}
        self.typing_speeds = []
        self.start_time = time.time()

    def _save_keystroke_image(self, image_path, current_time):
        image = Image.new('RGB', (600, 800), 'white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), f'Timestamp: {current_time}', fill='black', font=font)
        avg_speed = statistics.mean(self.typing_speeds) if self.typing_speeds else 0
        draw.text((10, 30), f'Avg Typing Speed: {avg_speed:.2f} WPM', fill='black', font=font)
        x, y, column_width = 10, 60, 200
        count = 0
        for key, value in sorted(self.keystroke_counts.items()):
            draw.text((x, y), f'{key}: {value}', fill='black', font=font)
            y += 20
            count += 1
            if count % 10 == 0:
                x += column_width
                y = 60
        image.save(image_path)

    def _save_keystroke_json(self, json_path, current_time):
        with open(json_path, 'w') as json_file:
            json.dump({
                'timestamp': current_time,
                'keystrokes': self.keystroke_counts,
                'avg_typing_speed_wpm': statistics.mean(self.typing_speeds) if self.typing_speeds else 0
            }, json_file, indent=4)

    def _start_save_timer(self):
        self.timer = Timer(self.save_interval, self._periodic_save)
        self.timer.start()

    def stop_timer(self):
        if self.timer:
            self.timer.cancel()

    def _periodic_save(self):
        save_thread = Thread(target=self.save_keystroke_track)
        save_thread.start()
        save_thread.join()
        self._start_save_timer()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tracker = KeystrokeTracker(save_interval=60)
    tracker.start_tracking()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop_tracking()
