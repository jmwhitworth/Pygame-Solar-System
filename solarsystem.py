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


class MoveableCameraGroup(pg.sprite.Group):
    """
    SPRITE GROUP SUBCLASS TO HANDLE MOUSE INPUTS AS OFFSETS FOR A 'CAMERA'
    """
    def __init__(self, SETTINGS):
        super().__init__()
        self.scale_size     = SETTINGS["Scales"]["Size"]
        self.scale_velocity = SETTINGS["Scales"]["Velocity"]
        self.scale_distance = SETTINGS["Scales"]["Distance"]
        self.incriment_up   = SETTINGS["Scales"]["Incriments"]["Up"]
        self.incriment_down = SETTINGS["Scales"]["Incriments"]["Down"]
        
        self.offset             = pg.math.Vector2() #TO APPLY TO SPRITES
        self.clickstart_offset  = pg.math.Vector2() #NORMALISE AFTER CLICK
        self.dragging           = False #WHEN TO APPLY OFFSET TO SPRITES
    
    def move_camera(self, event):
        """
        CLICK AND DRAG TO MOVE THE 'CAMERA'
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.clickstart_offset.x = self.offset.x - mouse_x
            self.clickstart_offset.y = self.offset.y - mouse_y
        
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.offset.x = mouse_x + self.clickstart_offset.x
                self.offset.y = mouse_y + self.clickstart_offset.y
        
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
            self.scale_size     *= self.incriment_up
            self.scale_velocity *= self.incriment_up
            self.scale_distance *= self.incriment_up
            
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
            self.scale_size     *= self.incriment_down
            self.scale_velocity *= self.incriment_down
            self.scale_distance *= self.incriment_down
    
    def create_sprites(self):
        #CREATE STARS FROM FILE
        for i in BODIES["Stars"]:
            i = BODIES["Stars"][i]
            colour = (i["Colour"]["r"],i["Colour"]["g"],i["Colour"]["b"])
            star(
                self,
                i["Name"],
                i["Size"]/2,
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
        for orbiter in orbiters:
            for i in BODIES[orbiter]:
                i = BODIES[orbiter][i]
                colour = (i["Colour"]["r"],i["Colour"]["g"],i["Colour"]["b"])
                if orbiter == "Moons":
                    #MOVES MOONS SLIGHTLY FURTHER OUT AND REVERSES ORBIT DIRECTION
                    i["Distance"] *= 10
                    i["Velocity"] *= -1
                satellite(
                    self,
                    i["Name"],
                    i["Orbits"],
                    i["Size"],
                    i["Distance"],
                    i["Velocity"],
                    colour
                )
    
    def get_body_by_name(self, name):
        """
        SEARCHES ALL SPRITES IN THE SPRITE GROUP
        AND RETURNS THE SPRITE WITH THE GIVEN NAME
        """
        for sprite in self:
            if sprite.name == name:
                return sprite
        return False

class star(pg.sprite.Sprite):
    def __init__(self, sprite_group, name, size, x, y, colour):
        super().__init__(sprite_group)
        self.sprite_group   = sprite_group
        self.name           = name
        self.base_size      = size
        self.base_radius    = 0
        self.base_velocity  = 0
        self.size           = self.base_size * self.sprite_group.scale_size
        self.radius         = 0
        self.velocity       = 0
        self.x              = x
        self.y              = y
        self.colour         = colour
        self.surface        = pg.display.get_surface()
    
    def update(self):
        self.scale()
        self.draw()
    
    def scale(self):
        self.size       = self.base_size * self.sprite_group.scale_size
        self.velocity   = self.base_velocity * self.sprite_group.scale_velocity
        self.radius     = self.base_radius * self.sprite_group.scale_distance
    
    def draw(self):
        pg.draw.circle(
            self.surface,
            self.colour,
            (self.x + self.sprite_group.offset.x, self.y + self.sprite_group.offset.y),
            self.size)

class satellite(star):
    def __init__(self, sprite_group, name, parent_name, size, radius, velocity, colour):
        super().__init__(sprite_group, name, size, 0, 0, colour)
        self.base_radius    = radius
        self.base_velocity  = velocity
        self.radius         = self.base_radius * sprite_group.scale_distance
        self.velocity       = self.base_velocity * sprite_group.scale_velocity
        self.parent         = sprite_group.get_body_by_name(parent_name) #GETS SPRITE OF BODY TO ORBIT
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.angle = radians(randrange(0,360))
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
    
    def update(self):
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.x = (self.center_of_rotation_x + self.radius * cos(self.angle))
        self.y = (self.center_of_rotation_y - self.radius * sin(self.angle))
        self.scale()
        self.draw()
        self.angle = self.angle + self.velocity
        self.x = self.x + self.radius * self.velocity * cos(self.angle + pi / 2)
        self.y = self.y - self.radius * self.velocity * sin(self.angle + pi / 2)


def run():
    visible_sprites = MoveableCameraGroup(SETTINGS)
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
            visible_sprites.move_camera(event)
    quit()


if __name__ == '__main__':
    run()