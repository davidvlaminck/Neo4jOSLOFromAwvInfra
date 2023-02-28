import json
from pathlib import Path


class SettingsManager:
    def __init__(self, settings_path: Path = None):
        self.settings: dict = {}
        if settings_path is not None:
            self.load_settings(settings_path)

    def load_settings(self, settings_path: Path = None):
        with open(str(settings_path)) as settings_file:
            self.settings = json.load(settings_file)
