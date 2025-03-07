import random
from typing import Optional

import pygame

from .CameraSurface import CameraSurface
from .StellarObject import StellarObject


class SolarSystem:
    """Class which collects all StellarObject instances and manages their updates and drawing"""

    def __init__(self, name: str, bodies: dict, scales: dict) -> None:
        self.name: str = name
        if self.name not in bodies:
            raise ValueError(f"'{self.name}' not found in bodies")
        self.bodies: dict = bodies[self.name]
        self.scales: dict = scales

        self.screen = pygame.display.get_surface()
        self.focus: Optional[StellarObject] = None
        self.surface = CameraSurface(self.screen.get_size())

        self.main_body: StellarObject = StellarObject.create(
            self.bodies,
            self.scales,
        )

    def tick(self) -> None:
        """Updates and draws the SolarSystem"""
        self.screen.blit(self.surface, (0, 0))
        self.surface.fill((0, 0, 0))

        self.main_body.update()
        self.main_body.draw(self.surface, self.surface.offset)

        if self.focus:
            self.surface.position = (self.focus.x, self.focus.y)

    def handle_events(self, event: pygame.event.Event) -> None:
        """Handles events for the SolarSystem"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.focus = None
                self.surface.transform((0, -50))
            elif event.key == pygame.K_s:
                self.focus = None
                self.surface.transform((0, 50))
            elif event.key == pygame.K_a:
                self.focus = None
                self.surface.transform((-50, 0))
            elif event.key == pygame.K_d:
                self.focus = None
                self.surface.transform((50, 0))
            elif event.key == pygame.K_SPACE:
                self.focus = None
                self.surface.reset()
            elif event.key == pygame.K_1:
                self.focus = random.choice(list(self.main_body.satellites))
