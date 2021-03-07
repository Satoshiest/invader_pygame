import pygame
from pygame.locals import *
import os

# settings and helper function for main game loop

START, PLAY, GAME_OVER = (0, 1, 2)  # game state
SCR_RECT = Rect(0, 0, 640, 480)  # screen size


def load_image(file):
    """load image"""
    if os.path.exists(os.path.join('images', file)):
        return pygame.image.load(os.path.join("images", file)).convert()
    raise SystemExit('Image not found')


def split_image(image, n):
    """split long image and return list of each"""
    image_list, w = list(), round(image.get_width())
    h, w2 = round(image.get_height()), round(w / n)
    for i in range(0, w, w2):
        surface = pygame.Surface((w2, h))
        surface.blit(image, (0, 0), Rect(i, 0, w2, h))
        surface.convert()
        image_list.append(surface)
    return image_list


def load_sound(file):
    """load sound"""
    if os.path.exists(os.path.join('sound', file)):
        return pygame.mixer.Sound(os.path.join("sound", file))
    raise SystemExit('Sound not found')
