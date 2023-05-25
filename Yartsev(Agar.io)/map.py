import pygame
from globalConstants import *


class Map:
    def __init__(self):
        self._position_x = WIDTH * 73 // 100
        self._position_y = HEIGHT // 25
        self._width = WIDTH // 4
        self._height = HEIGHT // 4

    def draw(self, screen, background, player, enemies, food):
        pygame.draw.rect(screen, WHITE, (self._position_x, self._position_y, self._width, self._height))
        pygame.draw.rect(screen, BLACK, (self._position_x, self._position_y, self._width, self._height), 2)
        pygame.draw.circle(screen, player._colour,
                           (self._position_x + self._width // 2, self._position_y + self._height // 2),
                           player._radius // 8)

        for enemy in enemies:
            if (abs(background._position_x - enemy._position_x) < WIDTH) and (
                    abs(background._position_y - enemy._position_y) < HEIGHT):
                pos_x = self._position_x + (WIDTH - background._position_x + enemy._position_x - enemy._radius) // 8
                pos_y = self._position_y + (HEIGHT - background._position_y + enemy._position_y - enemy._radius) // 8
                pygame.draw.ellipse(screen, enemy._colour, (pos_x, pos_y, enemy._radius // 4, enemy._radius // 4))

        for yummy in food:
            if (abs(background._position_x - yummy._position_x) < WIDTH) and (
                    abs(background._position_y - yummy._position_y) < HEIGHT):
                pos_x = self._position_x + (WIDTH - background._position_x + yummy._position_x - yummy._radius) // 8
                pos_y = self._position_y + (HEIGHT - background._position_y + yummy._position_y - yummy._radius) // 8
                pygame.draw.ellipse(screen, RED, (pos_x, pos_y, yummy._radius // 4, yummy._radius // 4))
