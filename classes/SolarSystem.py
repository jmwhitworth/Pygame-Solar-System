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

        self.main_body: StellarObject = StellarObject.create_from_dictionary(
            self.bodies,
            self.scales,
        )

    def tick(self) -> None:
        """Updates and draws the SolarSystem"""
        self.screen.blit(self.surface, (0, 0))
        self.surface.fill((0, 0, 0))

        self.main_body.update(self.surface.zoom)
        self.main_body.draw(self.surface, self.surface.offset)

        if self.focus:
            # Set the camera's position to the body, accounting for the zoom level
            self.surface.position = (
                self.focus.x // self.surface.zoom,
                self.focus.y // self.surface.zoom,
            )

    def handle_events(self, event: pygame.event.Event) -> None:
        """Handles events for the SolarSystem"""
        if event.type == pygame.MOUSEMOTION and self.surface.dragging:
            self.set_focus(None)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.set_focus(None)
        self.surface.handle_event(event)

    def reset(self):
        self.set_focus(None)
        self.surface.reset()

    def set_focus(self, body: StellarObject | None):
        self.focus = body
