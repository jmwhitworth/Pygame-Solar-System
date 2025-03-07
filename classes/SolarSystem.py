import pygame

from .StellarBody import StellarBody


class SolarSystem:
    """Class which collects all StellarBody instances and manages their updates and drawing"""

    def __init__(self, bodies: dict) -> None:
        self.screen = pygame.display.get_surface()
        self.surface = pygame.Surface(self.screen.get_size())
        self.main_body = StellarBody.create(bodies["milkyway"])

        # Used as a 'camera' to move the SolarSystem around
        self.x: int = 0
        self.y: int = 0

    @property
    def offset(self) -> tuple[int, int]:
        """Returns the offset of the SolarSystem
        the x and y coordinates are reversed to move the SolarSystem in the opposite direction
        This means that setting x to 300, will have our 'camera' be positioned to look at that point
        """
        return -self.x, -self.y

    def tick(self) -> None:
        """Updates and draws the SolarSystem"""
        self.screen.blit(self.surface, (0, 0))
        self.surface.fill((0, 0, 0))
        self.main_body.update()
        self.main_body.draw(self.surface, self.offset)

    def handle_events(self, event: pygame.event.Event) -> None:
        """Handles events for the SolarSystem"""
        print(type(event))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.y += 50
            if event.key == pygame.K_s:
                self.y -= 50
            if event.key == pygame.K_a:
                self.x += 50
            if event.key == pygame.K_d:
                self.x -= 50
