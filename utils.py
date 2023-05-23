from pygame import Surface
from json import load, dumps

from game_data import DEFAULT


class CustomLoader:
    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        with open(self.path, "r") as f:
            self.data = load(f)

    def save(self):
        with open(self.path, "w") as f:
            f.write(dumps(self.data, indent=4))

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        if isinstance(value, dict):
            self.__data = value
        else:
            raise TypeError("data must be a dict")

    def reset(self):
        self.data = DEFAULT[self.path.split("/")[-1].split(".")[0]] # "config.json" -> "config"

def draw_text(surf, text, font, pos, color=(255, 255, 255), centered=True):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if centered:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    surf.blit(text_surf, text_rect)

def draw_button(surf, text, font, pos, width, height, bgcolor=(255, 0, 0), color=(255, 255, 255), centered=True):
    button_surf = Surface(width, height)
    button_surf.fill(bgcolor)
    draw_text(button_surf, text, font, pos, color, centered)
    button_rect = button_surf.get_rect()
    if centered:
        button_rect.center = pos
    else:
        button_rect.topleft = pos
    surf.blit(button_surf, button_rect)


if __name__ == "__main__":
    from game_data import PATHS

    def print_dict(d):
        [print(f"{i}: {k}") for i, k in d.items()]

    test_config = CustomLoader(PATHS["config"])
    test_config.load()
    print_dict(test_config["VOLUME"])
    print_dict(test_config["HOTKEYS"])
    test_config["VOLUME"]["music"] = 0.1
    print(type(test_config))
    test_config["HOTKEYS"]["K_a"] = "left"
    test_config["HOTKEYS"]["K_z"] = "right"
    print_dict(test_config["HOTKEYS"])
    test_config.save()
    test_config.reset()
