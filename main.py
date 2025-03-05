import asyncio
import json

import pygame as pg

from sprites.CameraGroup import CameraGroup

with open("assets/settings.json", "r") as file:
    SETTINGS = json.load(file)
with open("assets/bodies.json", "r") as file:
    BODIES = json.load(file)


FPS = SETTINGS["Screen"]["FPS"]
WIN = pg.display.set_mode(
    (SETTINGS["Screen"]["Width"], SETTINGS["Screen"]["Height"]), pg.RESIZABLE
)
pg.display.set_caption(SETTINGS["Screen"]["Title"])


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
            if event.type == pg.QUIT:
                run = False
            visible_sprites.camera_controller(event)

        await asyncio.sleep(0)
    quit()


asyncio.run(main())
