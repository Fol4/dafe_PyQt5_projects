import pygame
from globalConstants import *


class Player:
    def __init__(self):
        self._radius = 30
        self._size = int(Pi * self._radius ** 2)
        self._position_x = WIDTH / 2
        self._position_y = HEIGHT / 2
        self._colour = LIME
        self._nickname = 'player'

    def draw(self, screen):
        pygame.draw.circle(screen, self._colour, (self._position_x, self._position_y), self._radius)
        font = pygame.font.Font(None, int(self._radius * 0.55))
        text = font.render(self._nickname, True, (0, 0, 0))
        rect = text.get_rect(center=(self._position_x, self._position_y))
        screen.blit(text, rect)

    def checking_for_death(self, enemies, background):
        for enemy in enemies:
            if ((enemy._position_x - background._position_x) ** 2 + (
                    enemy._position_y - background._position_y) ** 2) ** 0.5 + self._radius < enemy._radius and self._radius + DifferenceToEat < enemy._radius:
                return False
        return True
