import sys
import pygame as pg
from math import sin,cos,pi, radians
from random import randrange, uniform

WIDTH, HEIGHT = 1600, 900
WIN = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption("Solar System")

FPS = 60

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PURPLE = (255,0,255)
WHITE = (255,255,255)

def main(stars, satelites):
    clock = pg.time.Clock()
    run = True
    while run: # test if program has been quit
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        draw_window(stars, satelites)

def draw_window(stars, satelites):
    WIN.fill((0, 0, 0)) # blank screen
    [star.generate(WIN) for star in stars]
    [satelite.calculateMovement(WIN) for satelite in satelites]
    pg.display.update() # update screen


class star():
    instances = []
    def __init__(self, size, x, y, colour):
        self.__class__.instances.append(self)
        self.size = size
        self.x = x
        self.y = y
        self.colour = colour

    def generate(self, WIN):
        pg.draw.circle(WIN, self.colour, (self.x, self.y), self.size*10)

class satelite():
    instances = []
    def __init__(self, parent, size, distance, velocity, colour):
        self.__class__.instances.append(self)
        self.size = size/3
        self.radius = distance*70
        self.velocity = velocity/10000
        self.colour = colour
        self.parent = parent
        self.center_of_rotation_x = parent.x
        self.center_of_rotation_y = parent.y
        self.angle = radians(randrange(0,360))
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle)
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)

    def calculateMovement(self, WIN):
        self.center_of_rotation_x = self.parent.x #updates position of the body it's circling
        self.center_of_rotation_y = self.parent.y
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle) # generate position based on what we're orbiting + our angle
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle)
        pg.draw.circle(WIN, self.colour, (self.x, self.y), self.size*10) # draw to the screen
        self.angle = self.angle + self.velocity # New angle, we add angular velocity
        self.x = self.x + self.radius * self.velocity * cos(self.angle + pi / 2) # New x
        self.y = self.y - self.radius * self.velocity * sin(self.angle + pi / 2) # New y

# stars(size, x, y, colour)
    #background stars
for i in range(0,200):
    bg_stars = star(uniform(1.0,2.0)/10, randrange(0,WIDTH), randrange(0,HEIGHT), (randrange(220,255),randrange(220,255),randrange(220,255)))

    #the Sun
sun = star(5, WIDTH/2, HEIGHT/2, YELLOW)

# satelites(orbitining, size, distance, velocity, colour)
mercury = satelite(sun, 1, 1, -48, (219,206,202))
venus = satelite(sun, 3, 2, 35, (150,131,150))
earth = satelite(sun, 4, 3, 30, (0,0,205))
mars = satelite(sun, 2, 4, -24, (193,68,14))
jupiter = satelite(sun, 8, 6, 13, (227,110,75))
saturn = satelite(sun, 7, 7, -10, (206,184,184))
uranus = satelite(sun, 6, 8, -7, (213,251,252))
neptune = satelite(sun, 5, 9, 5, (91,93,223))

# moons(orbitining, size, distance, velocity, colour)
    #mercury
venus_moon = satelite(mercury, 0.6, 0.1, 200, (150,131,150))
    #venus
venus_moon = satelite(venus, 0.8, 0.3, -180, (150,131,150))
venus_moon = satelite(venus, 1, 0.4, 200, (150,131,150))
    #earth
Tmoon = satelite(earth, 0, 0.2, -300, (0,0,0))
Ttmoon = satelite(Tmoon, 0, 0.2, 350, (0,0,0))
Tttmoon = satelite(Ttmoon, 1, 0.2, -250, (255,255,255))
    #mars
mars_moon = satelite(mars, 0.4, 0.25, -380, (150,131,150))
mars_moon = satelite(mars, 0.7, 0.4, 240, (150,131,150))
    #jupiter
jupiter_moon = satelite(jupiter, 2, 0.6, 200, (150,131,150))
jupiter_moon = satelite(jupiter, 1.4, 0.45, -380, (150,131,150))
jupiter_moon = satelite(jupiter, 0.7, 0.6, 240, (150,131,150))
    #saturn
saturn_moon = satelite(saturn, 2, 0.6, 200, (150,131,150))
saturn_moon = satelite(saturn, 1.4, 0.45, -380, (150,131,150))
    #uranus
uranus_moon = satelite(uranus, 2, 0.6, 200, (150,131,150))
uranus_moon = satelite(uranus, 1.4, 0.45, -380, (150,131,150))
uranus_moon = satelite(uranus, 0.7, 0.6, 240, (150,131,150))
    #neptune
neptune_moon = satelite(neptune, 1.4, 0.45, -380, (150,131,150))
neptune_moon = satelite(neptune, 0.7, 0.6, 240, (150,131,150))

#asteroid belt - MAKE NEW CLASS
for i in range(0,2000):
    asteroid = satelite(sun, uniform(0.1,1.0), uniform(4.5, 5.2), randrange(20,22), (219,206,202))

if __name__ == '__main__':
    main(star.instances, satelite.instances)
    quit()
    sys.exit()
