import json
import os

SETTINGS_FILE = "settings.json"


def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        default = {
            "language": "en"
        }

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)

        return default

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(data):

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_language():

    settings = load_settings()

    return settings.get("language", "en")


def save_language(language):

    settings = load_settings()

    settings["language"] = language

    save_settings(settings)