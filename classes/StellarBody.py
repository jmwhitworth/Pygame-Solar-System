import pygame


class StellarBody:
    parent: "StellarBody"
    satellites: set["StellarBody"]

    name: str
    size: int
    distance: int
    velocity: int
    colour: tuple[int, int, int]
    x: int = 0
    y: int = 0

    scale: float = 0.000001
    image: pygame.Surface

    def __init__(self, data: dict) -> None:
        self.satellites = set()
        self.name = data["name"]
        self.size = data["size"] * self.scale
        self.distance = data["distance"] * self.scale
        self.velocity = data["velocity"] * self.scale
        self.colour = (
            data["colour"]["r"],
            data["colour"]["g"],
            data["colour"]["b"],
        )

        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey((0, 0, 0))

    @classmethod
    def create(cls, data: dict) -> "StellarBody":
        """Recursively creates StellarBody instances and their satellites"""
        stellar_body = cls(data)

        for satellite_data in data.get("satellites", []):
            stellar_body.satellites.add(cls.create(satellite_data))

        return stellar_body

    def update(self) -> None:
        self.x += 1
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
