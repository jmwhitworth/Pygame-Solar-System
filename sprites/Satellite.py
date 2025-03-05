from math import cos, pi, radians, sin
from random import uniform

from .Star import Star


class Satellite(Star):
    def __init__(self, sprite_group, name, parent_name, size, radius, velocity, colour):
        super().__init__(sprite_group, name, size, 0, 0, colour)
        self.base_radius = radius
        self.base_velocity = velocity
        self.radius = self.base_radius * sprite_group.scale_distance
        self.velocity = self.base_velocity * sprite_group.scale_velocity

        self.parent = sprite_group.get_body_by_name(parent_name)
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.angle = radians(uniform(0, 360))
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)

    def update(self):
        self.center_of_rotation_x, self.center_of_rotation_y = (
            self.parent.x,
            self.parent.y,
        )
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
        self.scale()
        self.draw()
        self.angle = self.angle + self.velocity
        self.x = self.x + self.radius * self.velocity * cos(self.angle + pi / 2)
        self.y = self.y - self.radius * self.velocity * sin(self.angle + pi / 2)
