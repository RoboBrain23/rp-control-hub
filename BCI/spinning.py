import math
import pygame

from pygame.locals import *


class SpinningCircle(pygame.surface.Surface):
    '''
    Class which make a spinning circle
    Usage:
    >>> cirlce = SpinningCircle(100, (255, 0, 0))
    >>> circle.update()
    '''

    def __init__(self, radius, color, speed=0.5):
        self.color = color
        self.radius = radius
        self.angle = 0
        self.speed = speed
        self.thickness = int(self.radius / 3.)
        self.portion = 360
        self.update()

    def update(self):
        super(SpinningCircle, self).__init__((self.radius * 2, self.radius * 2), SRCALPHA)

        portion = int(self.angle) % 360
        angle = math.radians(portion)

        pygame.draw.arc(self, self.color, (
        self.thickness, self.thickness, self.radius * 2 - self.thickness * 2, self.radius * 2 - self.thickness * 2), 0,
                        angle, self.thickness)

        self.angle += self.speed
