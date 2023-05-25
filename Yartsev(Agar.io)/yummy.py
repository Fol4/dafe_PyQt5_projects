import pygame
import random
from globalConstants import *


class Yummy:
    def __init__(self, background):
        self._radius = 10
        self._size = int(Pi * self._radius ** 2)
        self._position_x = random.randint(0, background._width)
        self._position_y = random.randint(0, background._height)

    def update(self, background, player, enemies):
        if ((background._position_x - self._position_x) ** 2 + (
                background._position_y - self._position_y) ** 2) ** 0.5 < player._radius:
            self._position_x = random.randint(0, background._width)
            self._position_y = random.randint(0, background._height)
            player._size += self._size
            player._radius = int((player._size / Pi) ** 0.5)

        for enemy in enemies:
            if ((enemy._position_x - self._position_x) ** 2 + (
                    enemy._position_y - self._position_y) ** 2) ** 0.5 < enemy._radius:
                self._position_x = random.randint(0, background._width)
                self._position_y = random.randint(0, background._height)
                enemy._size += self._size
                enemy._radius = int((enemy._size / Pi) ** 0.5)

    def draw(self, screen, background):
        if (abs(background._position_x - self._position_x) < WIDTH // 2) and (
                abs(background._position_y - self._position_y) < HEIGHT // 2):
            pos_x = WIDTH // 2 - background._position_x + self._position_x
            pos_y = HEIGHT // 2 - background._position_y + self._position_y
            pygame.draw.ellipse(screen, RED,
                                (pos_x - self._radius, pos_y - self._radius, 2 * self._radius, 2 * self._radius))
