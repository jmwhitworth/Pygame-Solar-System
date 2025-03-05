from random import uniform

import pygame as pg

from .Satellite import Satellite
from .Star import Star


class CameraGroup(pg.sprite.Group):
    """
    SPRITE GROUP SUBCLASS TO HANDLE MOUSE INPUTS AS OFFSETS FOR A 'CAMERA'
        - CLICK AND DRAG CAMERA
        - SCROLL WHEEL ZOOM
        - SPACE BAR TO RESET POSITIONS
    """

    def __init__(self, SETTINGS, BODIES):
        super().__init__()
        self.SETTINGS = SETTINGS
        self.BODIES = BODIES
        self.incriment_up = SETTINGS["Scales"]["Incriments"]["Up"]
        self.incriment_down = SETTINGS["Scales"]["Incriments"]["Down"]

        self.offset = pg.math.Vector2()  # TO APPLY TO SPRITES
        self.clickstart_offset = pg.math.Vector2()  # NORMALISE AFTER CLICK
        self.dragging = False  # WHEN TO APPLY OFFSET TO SPRITES
        self.reset_scales()

        self.astroid_distance_start = BODIES["Asteroids"]["Distance"]["Start"]
        self.astroid_distance_end = BODIES["Asteroids"]["Distance"]["End"]

    def reset_scales(self):
        self.scale_size = self.SETTINGS["Scales"]["Size"]
        self.scale_velocity = self.SETTINGS["Scales"]["Velocity"]
        self.scale_distance = self.SETTINGS["Scales"]["Distance"]
        self.offset.x = 0
        self.offset.y = 0

    def scale(self, direction):
        # Set a maximum outer zoom level
        if (self.scale_size * direction) * 1000000 < 0.35:
            return

        self.offset.x *= direction
        self.offset.y *= direction
        self.scale_size *= direction
        self.scale_velocity *= direction
        self.scale_distance *= direction
        self.update()

    def camera_controller(self, event):
        # IF LEFT MOUSE PRESSED
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.clickstart_offset.x = self.offset.x - mouse_x
            self.clickstart_offset.y = self.offset.y - mouse_y

        # IF LEFT MOUSE RELEASED
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        # IF MOUSE MOVED WHILE LEFT MOUSE PRESSED
        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.offset.x = mouse_x + self.clickstart_offset.x
                self.offset.y = mouse_y + self.clickstart_offset.y

        # IF MOUSE SCROLL WHEEL UP
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
            self.scale(self.incriment_up)

        # IF MOUSE SCROLL WHEEL DOWN
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
            self.scale(self.incriment_down)

        # IF SPACE BAR PRESSED
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.reset_scales()

    def create_sprites(self):
        # CREATE BACKGROUND STARS USING FILE DATA
        for i in range(0, self.BODIES["Background Stars"]["Count"]):
            Star(
                self,
                "Background Star",
                1071000,
                uniform(-5000, 5000),
                uniform(-5000, 5000),
                (255, 255, 255),
            )

        # CREATE STARS FROM FILE
        for i in self.BODIES["Stars"]:
            i = self.BODIES["Stars"][i]
            colour = (i["Colour"]["r"], i["Colour"]["g"], i["Colour"]["b"])
            Star(
                self,
                i["Name"],
                i["Size"] / 2,
                i["Position"]["x"],
                i["Position"]["y"],
                colour,
            )

        # CREATE ASTEROID BELT USING FILE DATA
        for i in range(0, self.BODIES["Asteroids"]["Count"]):
            Satellite(
                self,
                "Asteroid",
                "Sun",
                4007100,
                self.generate_asteroid_distance(),
                uniform(
                    self.BODIES["Asteroids"]["Speed"]["Start"],
                    self.BODIES["Asteroids"]["Speed"]["End"],
                ),
                (160, 160, 160),
            )

        # CREATE PLANETS & MOONS FROM FILE
        orbiters = ["Planets", "Moons"]
        for orbiter in orbiters:
            for i in self.BODIES[orbiter]:
                i = self.BODIES[orbiter][i]
                colour = (i["Colour"]["r"], i["Colour"]["g"], i["Colour"]["b"])
                if orbiter == "Moons":
                    # MOVES MOONS SLIGHTLY FURTHER OUT AND REVERSES ORBIT DIRECTION
                    i["Distance"] *= 10
                    i["Velocity"] *= -1
                Satellite(
                    self,
                    i["Name"],
                    i["Orbits"],
                    i["Size"],
                    i["Distance"],
                    i["Velocity"],
                    colour,
                )

    def generate_asteroid_distance(self):
        """
        RETURNS THE DISTANCE FOR THE ASTEROIDS TO SPAWN AT AND REDUCED AREA AVAILABLE WITH EACH CREATION
        FAVOURS A DENSE CENTER TO THE RING
        """
        position = uniform(self.astroid_distance_start, self.astroid_distance_end)
        self.astroid_distance_start += self.astroid_distance_start * 0.00004
        self.astroid_distance_end -= self.astroid_distance_end * 0.00004
        return position

    def get_body_by_name(self, name):
        """
        SEARCHES ALL SPRITES IN THE SPRITE GROUP
        AND RETURNS THE SPRITE WITH THE GIVEN NAME
        """
        for sprite in self:
            if sprite.name == name:
                return sprite
        return False
