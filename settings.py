import pygame
from json import load

_SETTINGS = load(open("settings.json"))
pygame.display.init()

LINES = _SETTINGS["lines"]

if _SETTINGS["height"] == "default":
    HEIGHT = pygame.display.Info().current_h
else:
    HEIGHT = _SETTINGS["height"]

if _SETTINGS["width"] == "default":
    if _SETTINGS["fixed_width"]:
        WIDTH = HEIGHT * 0.5625
    else:
        WIDTH = HEIGHT * 0.140625 * LINES

else:
    WIDTH = _SETTINGS["width"]

H_RATIO = HEIGHT / 1080
W_RATIO = WIDTH / HEIGHT / 0.5625
