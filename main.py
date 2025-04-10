import http.client, urllib
from pynput import keyboard
from dotenv import load_dotenv
import os
import time

class Cooldown:
    def __init__(self, duration):
        """Initializes the Cooldown object.

        Args:
            duration: The cooldown duration in seconds.
        """
        self.duration = duration
        self.last_used = 0

    def is_ready(self):
        """Checks if the cooldown has elapsed.

        Returns:
            True if the cooldown has elapsed, False otherwise.
        """
        return (time.time() - self.last_used) >= self.duration

    def start(self):
         """Starts the cooldown."""
         self.last_used = time.time()

load_dotenv()

cooldown = Cooldown(5)
def on_press(key):
    if cooldown.is_ready():
        cooldown.start()
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": os.getenv('TOKEN'),
            "user": os.getenv('USER'),
            "message": "Button has been pressed",
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
        #time.sleep(5)

keyboard_listener = keyboard.Listener(on_press=on_press)

keyboard_listener.start()

keyboard_listener.join()