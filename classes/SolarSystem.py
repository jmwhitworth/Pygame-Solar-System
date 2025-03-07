import random

import pygame

from .CameraSurface import CameraSurface
from .StellarObject import StellarObject


class SolarSystem:
    """Class which collects all StellarObject instances and manages their updates and drawing"""

    scales: dict = {
        "distance": 0.00000001,
        "velocity": 0.00000001,
        "size": 0.000001,
    }

    def __init__(self, bodies: dict) -> None:
        self.screen = pygame.display.get_surface()
        self.surface = CameraSurface(self.screen.get_size())

        self.main_body: StellarObject = StellarObject.create(
            bodies["milkyway"],
            SolarSystem.scales,
        )

    def tick(self) -> None:
        """Updates and draws the SolarSystem"""
        self.screen.blit(self.surface, (0, 0))
        self.surface.fill((0, 0, 0))

        self.main_body.update()
        self.main_body.draw(self.surface, (self.surface.x, self.surface.y))

    def handle_events(self, event: pygame.event.Event) -> None:
        """Handles events for the SolarSystem"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.surface.transform((0, -50))
            elif event.key == pygame.K_s:
                self.surface.transform((0, 50))
            elif event.key == pygame.K_a:
                self.surface.transform((-50, 0))
            elif event.key == pygame.K_d:
                self.surface.transform((50, 0))
            elif event.key == pygame.K_SPACE:
                self.surface.reset()
            elif event.key == pygame.K_1:
                target = random.choice(list(self.main_body.satellites))
                self.surface.x = target.x
                self.surface.y = target.y
