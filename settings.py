import pygame
from json import load

SETTINGS: dict = load(open("settings.json"))
pygame.display.init()

LINES = SETTINGS["lines"]
if LINES > 9:
    LINES = 9

if SETTINGS["height"] == "default":
    HEIGHT = pygame.display.Info().current_h
else:
    HEIGHT = SETTINGS["height"]

if SETTINGS["width"] == "default":
    if SETTINGS["fixed_width"]:
        WIDTH = HEIGHT * 0.5625
    else:
        WIDTH = HEIGHT * 0.140625 * LINES

else:
    WIDTH = SETTINGS["width"]

H_RATIO = HEIGHT / 1080
W_RATIO = WIDTH / HEIGHT / 0.5625
