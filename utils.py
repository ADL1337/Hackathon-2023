from json import load, dumps
    
class GameConfig:
    default = {
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
    }

    def __init__(self, path=None):
        self.path = path
        self.config = self.load(path)

    def __getitem__(self, key):
        return self.config[key]

    @classmethod
    def load(cls, path):
        if path is None:
            return cls.default
        with open(path) as f:
            return load(f)

    def save(self, path):
        with open(path, "w") as f:
            return f.write(dumps(self.config))

    def reset_config(self):
        self.config = self.load()


if __name__ == "__main__":
    from game_data import CONFIG_PATH
    
    def print_dict(d):
        [print(f"{i}: {k}") for i, k in d.items()]
    
    test_config = GameConfig(CONFIG_PATH)
    print_dict(test_config["VOLUME"])
    print_dict(test_config["HOTKEYS"])