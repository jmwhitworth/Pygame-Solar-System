import asyncio
import json

import pygame

from classes.Button import ButtonGroup
from classes.SolarSystem import SolarSystem
from classes.StellarObject import StellarObject


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

    FPS = settings["FPS"]
    pygame.display.set_mode(
        (settings["width"], settings["height"]),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption(settings["title"])

    clock = pygame.time.Clock()
    solar_system = SolarSystem("milkyway", bodies, scale)

    # Add UI menu
    buttons = ButtonGroup()
    buttons.add("Zoom +", solar_system.surface.zoom_in)
    buttons.add("Zoom -", solar_system.surface.zoom_out)
    buttons.add("Reset", solar_system.reset)
    buttons.add("")
    for body in solar_system.bodies["satellites"]:
        buttons.add(
            body["name"],
            lambda body=StellarObject.all_hashmap[body["name"]]: solar_system.set_focus(
                body
            ),
        )

    delta_time = 0.1
    x = 0
    run = True
    while run:
        solar_system.tick()
        buttons.draw()

        if settings["debug"]:
            debug(f"FPS: {int(clock.get_fps())}", x=100)
            debug(f"Delta Time: {delta_time}", x=100, y=30)
            debug(
                f"position: {int(solar_system.surface.unzoomed_position[0])} x {int(solar_system.surface.unzoomed_position[1])}",
                x=100,
                y=50,
            )
            debug(f"zoom: x{round(solar_system.surface.zoom, 2)}", x=100, y=70)

        x += 50 * delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            solar_system.handle_events(event)
            buttons.handle_event(event)

        pygame.display.update()

        delta_time = clock.tick(FPS) / 1000
        delta_time = max(0.001, min(0.1, delta_time))
        await asyncio.sleep(0)
    quit()


if __name__ == "__main__":
    asyncio.run(main())
