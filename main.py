import asyncio
import json

import pygame as pg

from classes.CameraGroup import CameraGroup

with open("assets/settings.json", "r") as file:
    SETTINGS = json.load(file)
with open("assets/bodies.json", "r") as file:
    BODIES = json.load(file)

FPS = SETTINGS["screen"]["FPS"]
WIN = pg.display.set_mode(
    (SETTINGS["screen"]["width"], SETTINGS["screen"]["height"]),
    pg.RESIZABLE,
)
pg.display.set_caption(SETTINGS["screen"]["title"])


font = pg.font.Font(None, 24)


def debug(info, y=10, x=10):
    """Temporary debug function"""
    display_surface = pg.display.get_surface()
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)


async def main():
    visible_sprites = CameraGroup(SETTINGS, BODIES)
    visible_sprites.create_sprites()

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        WIN.fill((0, 0, 0))
        visible_sprites.update()

        debug(f"FPS: {int(clock.get_fps())}", 10, SETTINGS["screen"]["width"] - 100)
        debug(
            f"FPS: {int(visible_sprites.offset.x)} x {int(visible_sprites.offset.y)}",
            42,
            SETTINGS["screen"]["width"] - 200,
        )

        pg.display.update()

        for event in pg.event.get():
            run = event.type != pg.QUIT
            visible_sprites.handle_event(event)

        await asyncio.sleep(0)
    quit()


asyncio.run(main())
