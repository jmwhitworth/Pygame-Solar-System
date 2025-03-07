import pygame


class CameraSurface(pygame.Surface):
    """A Pygame Surface that can facilitate camera movement"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset: tuple[int, int] = (-700, -350)

    @property
    def x(self) -> int:
        return -self.offset[0]

    @x.setter
    def x(self, value: int) -> None:
        self.offset = (value, self.offset[1])

    @property
    def y(self) -> int:
        return -self.offset[1]

    @y.setter
    def y(self, value: int) -> None:
        self.offset = (self.offset[0], value)

    def transform(self, value: tuple[int, int]):
        """Moves the CameraSurface by the given x and y values"""
        self.offset = (self.offset[0] + value[0], self.offset[1] + value[1])

    def reset(self):
        self.offset = (0, 0)
