from random import uniform

import pygame as pg

from .Button import ButtonGroup
from .Satellite import Satellite
from .Star import Star


class CameraGroup(pg.sprite.Group):
    """Sprite group subclass to handle inputs as offsets for a 'camera'.
    - Click and drag camera
    - Scroll wheel zoom
    - Space bar to reset positions
    """

    SETTINGS: dict = {}
    BODIES: dict = {}

    # Camera settings
    increment_up: float = 0
    increment_down: float = 0
    offset: pg.math.Vector2
    clickstart_offset: pg.math.Vector2
    dragging: bool
    scale_size: float
    scale_velocity: float
    scale_distance: float

    # Stage settings
    asteroid_distance_start: int
    asteroid_distance_end: int

    def __init__(self, SETTINGS: dict | None = None, BODIES: dict | None = None):
        if SETTINGS is None or BODIES is None:
            raise ValueError("SETTINGS and BODIES must be provided")

        self.SETTINGS: dict = SETTINGS
        self.increment_up: float = SETTINGS["scales"]["increments"]["up"]
        self.increment_down: float = SETTINGS["scales"]["increments"]["down"]

        self.BODIES: dict = BODIES
        self.asteroid_distance_start: int = BODIES["asteroids"]["distance"]["start"]
        self.asteroid_distance_end: int = BODIES["asteroids"]["distance"]["end"]

        self.offset = pg.math.Vector2()
        self.clickstart_offset = pg.math.Vector2()
        self.dragging = False

        self.button_group = ButtonGroup()
        self.button_group.add("Reset", self.reset)

        self.reset()
        super().__init__()

    def update(self, *args, **kwargs) -> None:
        """Update the sprites in the group"""
        self.button_group.draw()
        super().update(*args, **kwargs)

    def set(self, size, velocity, distance, x, y) -> None:
        self.scale_size = size
        self.scale_velocity = velocity
        self.scale_distance = distance
        self.offset.x = x
        self.offset.y = y

    def reset(self):
        self.set(
            self.SETTINGS["scales"]["size"],
            self.SETTINGS["scales"]["velocity"],
            self.SETTINGS["scales"]["distance"],
            0,
            0,
        )

    def view(self, target: Satellite | Star) -> None:
        self.set(
            self.scale_size,
            self.scale_velocity,
            self.scale_distance,
            target.x,
            target.y,
        )

    def scale(self, direction) -> None:
        # Set a maximum outer zoom level
        if (self.scale_size * direction) * 1000000 < 0.35:
            return

        self.offset.x *= direction
        self.offset.y *= direction
        self.scale_size *= direction
        self.scale_velocity *= direction
        self.scale_distance *= direction
        self.update()

    def handle_event(self, event) -> None:
        self.button_group.handle_event(event)

        # Handle mouse events
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.dragging = True
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.clickstart_offset.x = self.offset.x - mouse_x
                self.clickstart_offset.y = self.offset.y - mouse_y
            elif event.button == 4:  # Scroll up
                self.scale(self.increment_up)
            elif event.button == 5:  # Scroll down
                self.scale(self.increment_down)

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:  # Left click release
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:  # Mouse drag movement
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.offset.x = self.clickstart_offset.x + mouse_x
            self.offset.y = self.clickstart_offset.y + mouse_y

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:  # Spacebar reset
            self.reset()

    def create_sprites(self) -> None:
        """Create the sprites for the group"""
        self.create_stars()
        self.create_satellites()
        self.create_asteroids()

    def create_stars(self) -> None:
        """Creates the stars in the background and the main stars"""
        background_star_count = self.BODIES["background_stars"]["count"]
        for i in range(background_star_count):
            Star(
                self,
                "Background Star",
                1071000,
                uniform(-5000, 5000),
                uniform(-5000, 5000),
                (255, 255, 255),
            )

        for star in self.BODIES["stars"]:
            star_obj = Star(
                self,
                star["name"],
                star["size"] / 2,
                star["position"]["x"],
                star["position"]["y"],
                (star["colour"]["r"], star["colour"]["g"], star["colour"]["b"]),
            )
            self.button_group.add(star_obj.name, lambda: self.view(star_obj))

    def create_satellites(self) -> None:
        """Creates the planets and moons"""
        satellite_types = ["planets", "moons"]
        for satellite_type in satellite_types:
            for planet in self.BODIES[satellite_type]:
                parent = self.get_body_by_name(planet["orbits"])
                satellite_obj = Satellite(
                    self,
                    planet["name"],
                    parent.name,
                    planet["size"],
                    planet["distance"] + parent.radius,
                    planet["velocity"],
                    (
                        planet["colour"]["r"],
                        planet["colour"]["g"],
                        planet["colour"]["b"],
                    ),
                )
                self.button_group.add(
                    satellite_obj.name, lambda: self.view(satellite_obj)
                )

    def create_asteroids(self) -> None:
        """Creates the asteroids in the asteroid belt"""
        for i in range(0, self.BODIES["asteroids"]["count"]):
            Satellite(
                self,
                "asteroid",
                "Sun",
                4007100,
                self.generate_asteroid_distance(),
                uniform(
                    self.BODIES["asteroids"]["speed"]["start"],
                    self.BODIES["asteroids"]["speed"]["end"],
                ),
                (160, 160, 160),
            )

    def generate_asteroid_distance(self) -> float:
        """Returns the distance for the asteroids to spawn at and reduces area available over time.
        By reducing the area available, the asteroids will appear to be more dense towards the centre of the belt.
        """
        position = uniform(self.asteroid_distance_start, self.asteroid_distance_end)
        self.asteroid_distance_start += self.asteroid_distance_start * 0.00004
        self.asteroid_distance_end -= self.asteroid_distance_end * 0.00004
        return position

    def get_body_by_name(self, name) -> Star | Satellite | bool:
        """Returns the given sprite if it exists in the group"""
        for sprite in self:
            if sprite.name == name:
                return sprite
        return False
