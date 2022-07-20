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
WIN = pg.display.set_mode((SETTINGS["Screen"]["Width"], SETTINGS["Screen"]["Height"]), pg.RESIZABLE)
pg.display.set_caption(SETTINGS["Screen"]["Title"])


class MoveableCameraGroup(pg.sprite.Group):
    """
    SPRITE GROUP SUBCLASS TO HANDLE MOUSE INPUTS AS OFFSETS FOR A 'CAMERA'
        - CLICK AND DRAG CAMERA
        - SCROLL WHEEL ZOOM
        - SPACE BAR TO RESET POSITIONS
    """
    def __init__(self, SETTINGS):
        super().__init__()
        self.SETTINGS       = SETTINGS
        self.incriment_up   = SETTINGS["Scales"]["Incriments"]["Up"]
        self.incriment_down = SETTINGS["Scales"]["Incriments"]["Down"]
        
        self.offset             = pg.math.Vector2() #TO APPLY TO SPRITES
        self.clickstart_offset  = pg.math.Vector2() #NORMALISE AFTER CLICK
        self.dragging           = False #WHEN TO APPLY OFFSET TO SPRITES
        self.reset_scales()
        
        self.astroid_distance_start = BODIES["Asteroids"]["Distance"]["Start"]
        self.astroid_distance_end   = BODIES["Asteroids"]["Distance"]["End"]
    
    def reset_scales(self):
        self.scale_size     = SETTINGS["Scales"]["Size"]
        self.scale_velocity = SETTINGS["Scales"]["Velocity"]
        self.scale_distance = SETTINGS["Scales"]["Distance"]
        self.offset.x       = 0
        self.offset.y       = 0
    
    def scale(self, direction):
        self.offset.x       *= direction
        self.offset.y       *= direction
        self.scale_size     *= direction
        self.scale_velocity *= direction
        self.scale_distance *= direction
    
    def camera_controller(self, event):
        # IF LEFT MOUSE PRESSED
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.clickstart_offset.x = self.offset.x - mouse_x
            self.clickstart_offset.y = self.offset.y - mouse_y
        
        # IF LEFT MOUSE RELEASED
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        # IF MOUSE MOVED WHILE LEFT MOUSE PRESSED
        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.offset.x = mouse_x + self.clickstart_offset.x
                self.offset.y = mouse_y + self.clickstart_offset.y
        
        # IF MOUSE SCROLL WHEEL UP
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
            self.scale(self.incriment_up)
        
        # IF MOUSE SCROLL WHEEL DOWN
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
            self.scale(self.incriment_down)
        
        # IF SPACE BAR PRESSED
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.reset_scales()
    
    def create_sprites(self):
        #CREATE BACKGROUND STARS USING FILE DATA
        for i in range(0, BODIES["Background Stars"]["Count"]):
            star(
                self,
                "Background Star",
                1071000,
                uniform(-5000,5000),
                uniform(-5000,5000),
                (255,255,255)
            )
        
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
        for i in range(0, BODIES["Asteroids"]["Count"]):
            satellite(
                self,
                "Asteroid",
                "Sun",
                4007100,
                self.generate_asteroid_distance(),
                uniform(BODIES["Asteroids"]["Speed"]["Start"],BODIES["Asteroids"]["Speed"]["End"]),
                (160,160,160)
            )
        
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
    
    def generate_asteroid_distance(self):
        """
        RETURNS THE DISTANCE FOR THE ASTEROIDS TO SPAWN AT AND REDUCED AREA AVAILABLE WITH EACH CREATION
        FAVOURS A DENSE CENTER TO THE RING
        """
        position = uniform(self.astroid_distance_start,self.astroid_distance_end)
        self.astroid_distance_start     += self.astroid_distance_start*0.00004
        self.astroid_distance_end       -= self.astroid_distance_end*0.00004
        return position
    
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
        self.base_size      = size
        self.base_radius    = 0
        self.base_velocity  = 0
        self.size           = self.base_size * self.sprite_group.scale_size
        self.radius         = 0
        self.velocity       = 0
        
        self.name           = name
        self.x              = x
        self.y              = y
        self.colour         = colour
        self.surface        = pg.display.get_surface()
    
    def update(self):
        self.scale()
        self.draw()
    
    def scale(self):
        if self.name != "Background Star":
            self.size     = self.base_size     * self.sprite_group.scale_size
            self.velocity = self.base_velocity * self.sprite_group.scale_velocity
            self.radius   = self.base_radius   * self.sprite_group.scale_distance
    
    def draw(self):
        if self.name != "Background Star":
            pos = (self.x + self.sprite_group.offset.x, self.y + self.sprite_group.offset.y)
        else:
            pos = (self.x + self.sprite_group.offset.x*0.3, self.y + self.sprite_group.offset.y*0.3)
        pg.draw.circle(
            self.surface,
            self.colour,
            pos,
            self.size)

class satellite(star):
    def __init__(self, sprite_group, name, parent_name, size, radius, velocity, colour):
        super().__init__(sprite_group, name, size, 0, 0, colour)
        self.base_radius    = radius
        self.base_velocity  = velocity
        self.radius         = self.base_radius * sprite_group.scale_distance
        self.velocity       = self.base_velocity * sprite_group.scale_velocity
        
        self.parent         = sprite_group.get_body_by_name(parent_name)
        self.center_of_rotation_x = self.parent.x
        self.center_of_rotation_y = self.parent.y
        self.angle = radians(uniform(0,360))
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
    
    def update(self):
        self.center_of_rotation_x, self.center_of_rotation_y = self.parent.x, self.parent.y
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
            visible_sprites.camera_controller(event)
    quit()

if __name__ == '__main__':
    run()