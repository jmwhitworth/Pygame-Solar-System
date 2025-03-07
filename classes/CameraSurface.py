import pygame


class CameraSurface(pygame.Surface):
    """A Pygame Surface that can facilitate camera movement

    A CameraSurface has both a position and an offset:
        - The `position` is used to see the current coordinates of the camera
        - The `offset` should be applied against the x and y positions of any objects drawn on the CameraSurface
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unzoomed_position: tuple[int | float, int | float] = (0, 0)
        self.half_width: int | float = self.get_width() / 2
        self.half_height: int | float = self.get_height() / 2

        # Camera movement
        self.dragging: bool = False
        self.mouse_previous_position = pygame.Vector2(0, 0)

        self._zoom = 1

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        """Ensures that the zoom is always rounded to the nearest 0.1"""
        self._zoom = round(value, 1)

    @property
    def position(self) -> tuple[int | float, int | float]:
        """The current position of the CameraSurface, accounting for current zoom level"""
        return (
            self.unzoomed_position[0] * self.zoom,
            self.unzoomed_position[1] * self.zoom,
        )

    @position.setter
    def position(self, value: tuple[int | float, int | float]):
        self.unzoomed_position = value

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
        self.position = (
            self.unzoomed_position[0] + value[0],
            self.unzoomed_position[1] + value[1],
        )

    def zoom_in(self):
        """Zooms in the CameraSurface by 10%"""
        self.zoom += 0.1
        self.zoom = min(2.5, self.zoom)

    def zoom_out(self):
        """Zooms out the CameraSurface by 10%"""
        self.zoom -= 0.1
        self.zoom = max(0.3, self.zoom)

    def reset(self):
        """Resets the CameraSurface's position to the origin (0, 0)."""
        self.position = (0, 0)
        self.zoom = 1

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click press
                self.dragging = True
                self.mouse_previous_position = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:  # Mouse drag movement
            mouse_current_position = pygame.mouse.get_pos()
            delta = (
                pygame.Vector2(self.mouse_previous_position)
                - pygame.Vector2(mouse_current_position)
            ) / self.zoom
            self.transform(delta)
            self.mouse_previous_position = mouse_current_position

        elif event.type == pygame.MOUSEWHEEL:  # Mouse wheel for zoom
            if event.y > 0:
                self.zoom_in()
            else:
                self.zoom_out()

        elif event.type == pygame.KEYDOWN:  # Reset camera with space key
            if event.key == pygame.K_SPACE:
                self.reset()
