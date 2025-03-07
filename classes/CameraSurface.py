import pygame


class CameraSurface(pygame.Surface):
    """A Pygame Surface that can facilitate camera movement

    A CameraSurface has both a position and an offset:
        - The `position` is used to see the current coordinates of the camera
        - The `offset` should be applied against the x and y positions of any objects drawn on the CameraSurface
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.position: tuple[int | float, int | float] = (0, 0)
        self.half_width: int | float = self.get_width() / 2
        self.half_height: int | float = self.get_height() / 2

    @property
    def offset(self) -> tuple[int | float, int | float]:
        """Inverse of the CameraSurface's current position while accounting for the CameraSurface's size.
        Intended to be used as an offset for objects drawn on the CameraSurface.
        """
        return (
            -(self.position[0] - self.half_width),
            -(self.position[1] - self.half_height),
        )

    def transform(self, value: tuple[int | float, int | float]):
        """Moves the CameraSurface by the given x and y values

        Args:
            value (tuple[int | float, int | float]): The x and y values to move the CameraSurface by
        """
        self.position = (self.position[0] + value[0], self.position[1] + value[1])

    def reset(self):
        """Resets the CameraSurface's position to the origin (0, 0)."""
        self.position = (0, 0)
