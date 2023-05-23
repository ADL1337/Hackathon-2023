WIDTH = 1280
HEIGHT = 780
FPS = 60
TITLE = "Pizza Vigilante"
FONT_SIZE = 32
GRAVITY = 1
TILESIZE = 16

BUTTON = {
    "width": 200,
    "height": 50,
    "bgcolor": (192, 0, 0),
    "color": (255, 255, 255),
    "hover_color": (128, 0, 0),
    "centered": True,
    "spacing": 50
}

RES_PATH = "res/"

PATHS = {
    "img": RES_PATH + "img/",
    "sfx": RES_PATH + "sfx/",
    "music": RES_PATH + "music/",
    "config": RES_PATH + "config.json",
    "stats": RES_PATH + "stats.json",
    "font": RES_PATH + "game_font.ttf"
}

DEFAULT = {
    "config": {
        "HOTKEYS": {
            "K_space": "jump",
            "K_q": "left",
            "K_d": "right",
            "K_LSHIFT": "shoot",
            "K_ESCAPE": "pause",
            "K_BACKSPACE": "die"
        },
        "VOLUME": {
            "music": 0.5,
            "sfx": 0.5
        }
    },
    "stats": {
        "distance_travelled": 0, # pixels / 1 000
        "death_count": 0,
        "playtime": 0, # hours
        "jump_count": 0,
        "shots_fired": 0
    }
}