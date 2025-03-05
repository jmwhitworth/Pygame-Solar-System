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


async def main():
    visible_sprites = CameraGroup(SETTINGS, BODIES)
    visible_sprites.create_sprites()

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        WIN.fill((0, 0, 0))
        visible_sprites.update()
        pg.display.update()

        for event in pg.event.get():
            run = event.type != pg.QUIT
            visible_sprites.camera_controller(event)

        await asyncio.sleep(0)
    quit()


asyncio.run(main())
