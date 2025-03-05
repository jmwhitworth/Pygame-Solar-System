import pygame as pg


class Star(pg.sprite.Sprite):
    def __init__(self, sprite_group, name, size, x, y, colour):
        super().__init__(sprite_group)
        self.sprite_group = sprite_group
        self.base_size = size
        self.base_radius = 0
        self.base_velocity = 0
        self.size = self.base_size * self.sprite_group.scale_size
        self.radius = 0
        self.velocity = 0

        self.name = name
        self.x = x
        self.y = y
        self.colour = colour
        self.surface = pg.display.get_surface()

    def update(self):
        self.scale()
        self.draw()

    def scale(self):
        if self.name != "Background Star":
            self.size = self.base_size * self.sprite_group.scale_size
            self.velocity = self.base_velocity * self.sprite_group.scale_velocity
            self.radius = self.base_radius * self.sprite_group.scale_distance

    def draw(self):
        if self.name != "Background Star":
            pos = (
                self.x + self.sprite_group.offset.x,
                self.y + self.sprite_group.offset.y,
            )
        else:
            pos = (
                self.x + self.sprite_group.offset.x * 0.3,
                self.y + self.sprite_group.offset.y * 0.3,
            )
        pg.draw.circle(self.surface, self.colour, pos, self.size)
