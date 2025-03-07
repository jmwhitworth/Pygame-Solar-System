from math import cos, pi, radians, sin
from random import uniform

import pygame


class StellarObject:
    def __init__(self, data: dict, scales: dict) -> None:
        # Relationships
        self.parent: "StellarObject" = None
        self.satellites: set["StellarObject"] = set()

        # Properties
        self.name: str = data["name"]
        self.size: float = round(data["size"] * scales["size"], 4)
        self.colour: tuple[int, int, int] = (
            int(data["colour"]["r"]),
            int(data["colour"]["g"]),
            int(data["colour"]["b"]),
        )

        # Orbit properties
        self.angle = radians(uniform(0, 360))
        self.distance: float = round(data["distance"] * scales["distance"], 4)
        self.velocity: float = round(data["velocity"] * scales["velocity"], 4)

        # Position
        self.x: int = 0
        self.y: int = 0
        self.calculate_orbit()

        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey((0, 0, 0))

    @classmethod
    def create(cls, data: dict, scales: dict) -> "StellarObject":
        """Recursively creates StellarObject instances and their satellites"""
        stellar_body = cls(data, scales)

        for satellite_data in data.get("satellites", []):
            satellite = cls.create(satellite_data, scales)
            satellite.parent = stellar_body
            stellar_body.satellites.add(satellite)

        return stellar_body

    @property
    def centre_of_rotation(self) -> tuple[float, float]:
        centre_of_rotation_x = self.parent.x if self.parent else 0
        centre_of_rotation_y = self.parent.y if self.parent else 0
        return centre_of_rotation_x, centre_of_rotation_y

    def calculate_orbit(self) -> None:
        centre_x, centre_y = self.centre_of_rotation
        self.x = centre_x + self.distance * cos(self.angle)
        self.y = centre_y - self.distance * sin(self.angle)
        self.angle += self.velocity

    def update(self) -> None:
        self.calculate_orbit()
        [satellite.update() for satellite in self.satellites]

    def draw(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        pygame.draw.circle(
            self.image,
            self.colour,
            (self.size / 2, self.size / 2),
            self.size / 2,
        )
        surface.blit(
            self.image,
            (
                (self.x - (self.size / 2)) + offset[0],
                (self.y - (self.size / 2)) + offset[1],
            ),
        )

        [satellite.draw(surface, offset) for satellite in self.satellites]
