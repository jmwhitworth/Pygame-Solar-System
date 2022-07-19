from math           import sin, cos, pi, radians
from random         import randrange, uniform
import pygame       as pg
import json


#LOAD OUR JSON CONFIG FILES
with open("settings.json", "r") as file:
    SETTINGS = json.load(file)
with open("bodies.json", "r") as file:
    BODIES = json.load(file)

#SETUP WINDOW
FPS = SETTINGS["Screen"]["FPS"]
WIN = pg.display.set_mode((SETTINGS["Screen"]["Width"], SETTINGS["Screen"]["Height"]))
pg.display.set_caption(SETTINGS["Screen"]["Title"])

#SPRITE GROUP FOR UPDATING AND SEARCHING
visible_sprites = pg.sprite.Group()


def get_body_by_name(name):
    """
    SEARCHES ALL SPRITES IN THE VISIBLE SPRITE GROUP
    AND RETURNS THE SPRITE WITH THE GIVEN NAME
    """
    for sprite in visible_sprites:
        if sprite.name == name:
            return sprite
    return False


class star(pg.sprite.Sprite):
    def __init__(self, name, size, x, y, colour):
        super().__init__(visible_sprites)
        self.name   = name
        self.size   = size  * SETTINGS["Scales"]["Size"]
        self.x      = x
        self.y      = y
        self.colour = colour
    
    def update(self, WIN):
        pg.draw.circle(WIN, self.colour, (self.x, self.y), self.size)

class satellite(star):
    def __init__(self, name, parent_name, size, distance, velocity, colour):
        super().__init__(name, size, 0, 0, colour)
        self.radius     = distance * SETTINGS["Scales"]["Distance"]
        self.velocity   = velocity * SETTINGS["Scales"]["Velocity"]
        self.parent     = get_body_by_name(parent_name) #GETS SPRITE OF BODY TO ORBIT
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.angle = radians(randrange(0,360))
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
    
    def update(self, WIN):
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
        
        pg.draw.circle(WIN, self.colour, (self.x, self.y), self.size)
        
        self.angle = self.angle + self.velocity
        self.x = self.x + self.radius * self.velocity * cos(self.angle + pi / 2)
        self.y = self.y - self.radius * self.velocity * sin(self.angle + pi / 2)


def create_sprites():
    #CREATE STARS FROM FILE
    for i in BODIES["Stars"]:
        i = BODIES["Stars"][i]
        colour = (i["Colour"]["r"],i["Colour"]["g"],i["Colour"]["b"])
        star(
            i["Name"],
            i["Size"],
            i["Position"]["x"],
            i["Position"]["y"],
            colour
        )

    #CREATE ASTEROID BELT USING FILE DATA
    """CODE HERE"""

    #CREATE BACKGROUND STARS USING FILE DATA
    """CODE HERE"""

    #CREATE PLANETS & MOONS FROM FILE
    orbiters = ["Planets", "Moons"]
    for obiter in orbiters:
        for i in BODIES[obiter]:
            i = BODIES[obiter][i]
            colour = (i["Colour"]["r"],i["Colour"]["g"],i["Colour"]["b"])
            satellite(
                i["Name"],
                i["Orbits"],
                i["Size"],
                i["Distance"],
                i["Velocity"],
                colour
            )

def run():
    create_sprites()
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        WIN.fill((0, 0, 0))
        visible_sprites.update(WIN)
        pg.display.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
    quit()


if __name__ == '__main__':
    run()