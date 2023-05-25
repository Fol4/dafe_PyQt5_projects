import pygame
import random
from globalConstants import *


class Enemy:
    def __init__(self, background):
        self._radius = random.randint(30, 300)
        self._size = int(Pi * self._radius ** 2)
        self._position_x = random.randint(0, background._width)
        self._position_y = random.randint(0, background._height)
        self._colour = ENEMY_COLOURS[random.randint(0, len(ENEMY_COLOURS) - 1)]
        self._nickname = ENEMY_NICKNAMES[random.randint(0, len(ENEMY_NICKNAMES) - 1)]

    def update(self, enemies, food, player, background):
        min_radius = background._width
        max_radius = 0
        speed_away_x, speed_away_y = 0, 0
        speed_toward_x, speed_toward_y = 0, 0

        if (abs(background._position_x - self._position_x) - player._radius < WIDTH // 2) and (
                abs(background._position_y - self._position_y) - player._radius < HEIGHT // 2):

            if self._radius + DifferenceToEat < player._radius <= min_radius:
                min_radius = player._radius
                speed_away_x, speed_away_y = self._position_x - background._position_x, self._position_y - background._position_y

            elif self._radius - DifferenceToEat > player._radius >= max_radius:
                max_radius = player._radius
                speed_toward_x, speed_toward_y = background._position_x - self._position_x, background._position_y - self._position_y

        for enemy in enemies:
            if self._position_x != enemy._position_x and self._position_y != enemy._position_y:
                if (abs(self._position_x - enemy._position_x) - enemy._radius < WIDTH // 2) and (
                        abs(self._position_y - enemy._position_y) - enemy._radius < HEIGHT // 2):

                    if self._radius + DifferenceToEat < enemy._radius <= min_radius:
                        min_radius = enemy._radius
                        speed_away_x, speed_away_y = self._position_x - enemy._position_x, self._position_y - enemy._position_y

                    elif self._radius - DifferenceToEat > enemy._radius >= max_radius:
                        max_radius = enemy._radius
                        speed_toward_x, speed_toward_y = enemy._position_x - self._position_x, enemy._position_y - self._position_y

        if min_radius != background._width:
            speed_x, speed_y = speed_away_x, speed_away_y
        elif max_radius != 0:
            speed_x, speed_y = speed_toward_x, speed_toward_y
        else:
            min_distance = (background._width ** 2 + background._height ** 2) ** 0.5
            for dot in food:
                if ((self._position_x - dot._position_x) ** 2 + (
                        self._position_y - dot._position_y) ** 2) ** 0.5 < min_distance:
                    min_distance = ((self._position_x - dot._position_x) ** 2 + (
                            self._position_y - dot._position_y) ** 2) ** 0.5
                    speed_x, speed_y = dot._position_x - self._position_x, dot._position_y - self._position_y

        max_speed = abs(speed_x) + abs(speed_y)
        coefficient = 300 / self._radius
        speed_x, speed_y = coefficient * (speed_x / max_speed), coefficient * (speed_y / max_speed)
        self._position_x += speed_x
        self._position_y += speed_y

        self._position_x = 0 if (self._position_x <= 0) else self._position_x
        self._position_x = background._width if (self._position_x >= background._width) else self._position_x
        self._position_y = 0 if (self._position_y <= 0) else self._position_y
        self._position_y = background._height if (self._position_y >= background._height) else self._position_y

    def draw(self, screen, background):
        if (abs(background._position_x - self._position_x) - self._radius < WIDTH // 2) and (
                abs(background._position_y - self._position_y) - self._radius < HEIGHT // 2):
            pos_x = WIDTH // 2 - background._position_x + self._position_x
            pos_y = HEIGHT // 2 - background._position_y + self._position_y
            pygame.draw.ellipse(screen, self._colour,
                                (pos_x - self._radius, pos_y - self._radius, 2 * self._radius, 2 * self._radius))
            font = pygame.font.Font(None, int(self._radius * 2 / 3))
            text = font.render(self._nickname, True, (0, 0, 0))
            rect = text.get_rect(center=(pos_x, pos_y))
            screen.blit(text, rect)

    def checking_for_death(self, enemies, background, player):
        if ((background._position_x - self._position_x) ** 2 + (
                background._position_y - self._position_y) ** 2) ** 0.5 + self._radius < player._radius and self._radius + DifferenceToEat < player._radius:
            player._size += self._size
            player._radius = int((player._size / Pi) ** 0.5)
            self._position_x = random.randint(0, background._width)
            self._position_y = random.randint(0, background._height)
            self._radius = random.randint(30, 200)
            self._size = int(Pi * self._radius ** 2)

        for enemy in enemies:
            if self._position_x != enemy._position_x and self._position_y != enemy._position_y:
                if ((enemy._position_x - self._position_x) ** 2 + (
                        enemy._position_y - self._position_y) ** 2) ** 0.5 + self._radius < enemy._radius and self._radius + DifferenceToEat < enemy._radius:
                    enemy._size += self._size
                    enemy._radius = int((enemy._size / Pi) ** 0.5)
                    self._radius = random.randint(30, 200)
                    self._size = int(Pi * self._radius ** 2)
                    self._position_x = random.randint(0, background._width)
                    self._position_y = random.randint(0, background._height)
