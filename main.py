import asyncio
import json

import pygame

from classes.SolarSystem import SolarSystem


def debug(info, y=10, x=10):
    """Temporary debug function"""
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)


async def main() -> None:
    with open("assets/settings.json", "r") as file:
        settings: dict = json.load(file)
    with open("assets/bodies.json", "r") as file:
        bodies: dict = json.load(file)
    with open("assets/scale.json", "r") as file:
        scale: dict = json.load(file)

    FPS = settings["screen"]["FPS"]
    pygame.display.set_mode(
        (settings["screen"]["width"], settings["screen"]["height"]),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption(settings["screen"]["title"])

    clock = pygame.time.Clock()
    solar_system = SolarSystem("milkyway", bodies, scale)

    delta_time = 0.1
    x = 0
    run = True
    while run:
        solar_system.tick()
        debug(f"FPS: {int(clock.get_fps())}")
        debug(f"Delta Time: {delta_time}", y=30)
        debug(
            f"position: {round(solar_system.surface.unzoomed_position[0], 2)} x {round(solar_system.surface.unzoomed_position[1], 2)}",
            y=50,
        )
        debug(f"zoom: x{round(solar_system.surface.zoom, 2)}", y=70)

        x += 50 * delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            solar_system.handle_events(event)

        pygame.display.update()

        delta_time = clock.tick(FPS) / 1000
        delta_time = max(0.001, min(0.1, delta_time))
        await asyncio.sleep(0)
    quit()


if __name__ == "__main__":
    asyncio.run(main())
