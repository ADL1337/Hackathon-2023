from utils import load_config

WIDTH = 1280
HEIGHT = 780
FPS = 60
TITLE = "Pizza Vigilante"

CONFIG_PATH = "res/config.json"

config = load_config(CONFIG_PATH)

VOLUME = config.get("volume")