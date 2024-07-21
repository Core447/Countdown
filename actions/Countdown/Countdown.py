# Import StreamController modules
from math import floor
import time
from src.backend.DeckManagement.InputIdentifier import Input, InputEvent
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

from .progress import create_progress_ring

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class Countdown(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.duration = 30
        self.start_time = None
        self.paused_time = None

    def get_remaining_time(self) -> int:
        if self.start_time is None:
            return self.duration
        
        if self.paused_time is not None:
            return max(self.duration - (self.paused_time - self.start_time), 0)
        
        return max(self.duration - (time.time() - self.start_time), 0)
        
    def show(self) -> None:
        remaining_time = self.get_remaining_time()

        remaining_hours = int(remaining_time / 3600)
        remaining_minutes = int((remaining_time - remaining_hours * 3600) / 60)
        remaining_seconds = int(remaining_time - remaining_hours * 3600 - remaining_minutes * 60)

        if remaining_hours > 0:
            time_string = f"{remaining_hours:02}:{remaining_minutes:02}:{remaining_seconds:02}"
        else:
            time_string = f"{remaining_minutes:02}:{remaining_seconds:02}"

        self.set_center_label(time_string)


        progress = remaining_time / self.duration
        if remaining_seconds + remaining_minutes * 60 + remaining_hours * 3600 == 0:
            progress = 0
        progress_ring = create_progress_ring(floor(progress * 100) / 100, ring_color=(0, 147, 255), ring_thickness=15)
        self.set_media(image=progress_ring)
        
    def on_ready(self) -> None:
        settings = self.get_settings()
        self.duration = settings.get("duration", 30)
        self.on_tick()

    def on_tick(self) -> None:
        self.show()

    def event_callback(self, event: InputEvent, data) -> None:
        if event in (Input.Key.Events.SHORT_UP, Input.Dial.Events.SHORT_UP, Input.Dial.Events.SHORT_TOUCH_PRESS):
            if self.start_time is None:
                # start
                self.start_time = time.time()
                self.paused_time = None

            else:
                # pause/resume
                if self.paused_time is None:
                    # pause
                    self.paused_time = time.time()
                else:
                    # resume
                    self.start_time = time.time() - (self.paused_time - self.start_time)
                    self.paused_time = None

        elif event in (Input.Key.Events.HOLD_START, Input.Dial.Events.HOLD_START, Input.Dial.Events.LONG_TOUCH_PRESS):
            # reset and stop/pause
            self.start_time = None
            self.paused_time = None

        elif event == Input.Dial.Events.TURN_CW:
            self.duration = self.duration + 1
            settings = self.get_settings()
            settings["duration"] = self.duration
            self.set_settings(settings)
            self.show()

        elif event == Input.Dial.Events.TURN_CCW:
            self.duration = self.duration - 1
            settings = self.get_settings()
            settings["duration"] = self.duration
            self.set_settings(settings)
            self.show()

        else:
            return
        self.show()        

    def get_config_rows(self) -> list:
        self.time_row = Adw.SpinRow.new_with_range(min=0, max=99*60*60+59*60+59, step=1)
        self.time_row.set_title("Duration (seconds)")
        self.time_row.set_subtitle("Duration of the countdown")

        self.load_config_values()

        self.time_row.connect("changed", self.on_time_row_changed)

        return [self.time_row]
    
    def load_config_values(self) -> None:
        settings = self.get_settings()

        self.time_row.set_value(settings.get("duration", 30))

    def on_time_row_changed(self, *args) -> None:
        settings = self.get_settings()
        self.duration = round(self.time_row.get_value())

        settings["duration"] = self.duration
        self.set_settings(settings)

        self.show()