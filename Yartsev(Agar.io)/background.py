import pygame
from globalConstants import *


class Background:
    def __init__(self):
        self._width = 10000
        self._height = 10000
        self._position_x = self._width // 2
        self._position_y = self._height // 2

    def update(self, player):
        pos = pygame.mouse.get_pos()
        if ((pos[0] - player._position_x) ** 2 + (pos[1] - player._position_y) ** 2) ** 0.5 > player._radius:
            speed_x, speed_y = pos[0] - player._position_x, pos[1] - player._position_y
            max_speed = abs(speed_x) + abs(speed_y)
            speed = 300 / player._radius
            speed_x, speed_y = speed * (speed_x / max_speed), speed * (speed_y / max_speed)
            self._position_x += speed_x
            self._position_y += speed_y

            self._position_x = 0 if (self._position_x <= 0) else self._position_x
            self._position_x = self._width if (self._position_x >= self._width) else self._position_x
            self._position_y = 0 if (self._position_y <= 0) else self._position_y
            self._position_y = self._height if (self._position_y >= self._height) else self._position_y

    def draw(self, screen):
        start_x = int(50 - ((self._position_x - WIDTH) % 50))
        start_y = int(50 - ((self._position_y - HEIGHT) % 50))
        end_x = WIDTH
        end_y = HEIGHT
        start_for_x = 0
        start_for_y = 0

        if (WIDTH // 2) >= self._position_x:
            start_x = int(WIDTH // 2 - self._position_x)
            start_for_y = start_x

        if self._position_x >= self._width - (WIDTH // 2):
            end_x = int(WIDTH // 2 + self._width - self._position_x)

        if self._position_y <= (HEIGHT // 2):
            start_y = int(HEIGHT // 2 - self._position_y)
            start_for_x = start_y

        if self._position_y >= self._height - (HEIGHT // 2):
            end_y = int(HEIGHT // 2 + self._height - self._position_y)

        for i in range(start_x, end_x + 1, 50):
            pygame.draw.line(screen, GRAY, (i, start_for_x), (i, end_y), 2)

        for j in range(start_y, end_y + 1, 50):
            pygame.draw.line(screen, GRAY, (start_for_y, j), (end_x, j), 2)
