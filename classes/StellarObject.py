from math import cos, pi, radians, sin
from random import uniform

import pygame


class StellarObject:
    all_set: set["StellarObject"] = set()
    all_hashmap: dict[str, "StellarObject"] = {}

    def __init__(self, data: dict, scales: dict) -> None:
        StellarObject.all_set.add(self)
        if name := data.get("name"):
            self.name: str = name
            StellarObject.all_hashmap[name] = self

        # Relationships
        self.parent: "StellarObject" = None
        self.satellites: set["StellarObject"] = set()

        # Properties
        self.scale: dict = scales[data["type"]]
        self.size: float = data["size"] * self.scale["size"]
        self.colour: tuple[int, int, int] = (
            int(data["colour"]["r"]),
            int(data["colour"]["g"]),
            int(data["colour"]["b"]),
        )
        self.zoom_level: int | float = 1

        # Orbit properties
        self.angle = radians(uniform(0, 360))
        self.distance: float = data["distance"] * self.scale["distance"]
        self.velocity: float = data["velocity"] * self.scale["velocity"]

        # Position
        self.x: int = 0
        self.y: int = 0
        self.calculate_orbit()

    @classmethod
    def create_from_dictionary(cls, data: dict, scales: dict) -> "StellarObject":
        """Recursively creates StellarObject instances and their satellites"""
        stellar_body = cls(data, scales)

        for satellite_data in data.get("satellites", []):
            satellite = cls.create_from_dictionary(satellite_data, scales)
            satellite.parent = stellar_body
            stellar_body.satellites.add(satellite)

        return stellar_body

    @property
    def centre_of_rotation(self) -> tuple[float, float]:
        centre_of_rotation_x = self.parent.x if self.parent else 0
        centre_of_rotation_y = self.parent.y if self.parent else 0
        return centre_of_rotation_x, centre_of_rotation_y

    def calculate_orbit(self, zoom: int | float = 1) -> None:
        centre_x, centre_y = self.centre_of_rotation
        self.x = centre_x + (self.distance * zoom) * cos(self.angle)
        self.y = centre_y - (self.distance * zoom) * sin(self.angle)
        self.angle += self.velocity

    def update(self, zoom: int | float = 1) -> None:
        self.zoom_level = zoom
        self.calculate_orbit(zoom)

    def draw(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        zoomed_size = self.size * self.zoom_level

        image = pygame.Surface((zoomed_size, zoomed_size))
        image.set_colorkey((0, 0, 0))

        pygame.draw.circle(
            image,
            self.colour,
            (zoomed_size / 2, zoomed_size / 2),
            zoomed_size / 2,
        )

        surface.blit(
            image,
            (
                (self.x - (zoomed_size / 2)) + offset[0],
                (self.y - (zoomed_size / 2)) + offset[1],
            ),
        )

    @staticmethod
    def generate_asteroid_distance(
        lower_range, upper_range
    ) -> tuple[float, float, float]:
        """Returns the distance for the asteroids to spawn at and reduces area available over time.
        By reducing the area available, the asteroids will appear to be more dense towards the centre of the belt.
        """
        position = uniform(lower_range, upper_range)
        lower_range += lower_range * 0.00004
        upper_range -= upper_range * 0.00004
        return (position, lower_range, upper_range)
