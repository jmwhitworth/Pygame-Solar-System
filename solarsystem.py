import sys
import pygame as pg
from math import sin,cos,pi, radians
from random import randrange

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


def main(stars, planets):
    clock = pg.time.Clock()
    run = True
    while run: # test if program has been quit
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        draw_window(stars, planets)
        

def draw_window(stars, planets):
    WIN.fill((0, 0, 0)) # blank screen

    [star.generate(WIN) for star in stars]
    [planet.calculateMovement(WIN) for planet in planets]

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

class planet():
    instances = []
    def __init__(self, center_of_rotation_x, center_of_rotation_y, size, distance, velocity, colour):
        self.__class__.instances.append(self)
        self.size = size/2
        self.radius = distance*90
        self.velocity = velocity/10000
        self.colour = colour
        self.center_of_rotation_x = center_of_rotation_x
        self.center_of_rotation_y = center_of_rotation_y
        self.angle = radians(randrange(0,360))

        self.x = center_of_rotation_x + self.radius * cos(self.angle) #Starting position x
        self.y = center_of_rotation_y - self.radius * sin(self.angle) #Starting position y


    def calculateMovement(self, WIN):
        self.x = self.center_of_rotation_x + self.radius * cos(self.angle) #Starting position x
        self.y = self.center_of_rotation_y - self.radius * sin(self.angle) #Starting position y
        pg.draw.circle(WIN, self.colour, (self.x, self.y), self.size*10)
        self.angle = self.angle + self.velocity # New angle, we add angular velocity
        self.x = self.x + self.radius * self.velocity * cos(self.angle + pi / 2) # New x
        self.y = self.y - self.radius * self.velocity * sin(self.angle + pi / 2) # New y


# star(size, x, y)
sun = star(5, WIDTH/2, HEIGHT/2, YELLOW)

#planet(centre_of_x, center_of_y, size, distance, velocity, colour)
mercury = planet(sun.x, sun.y, 1, 1, 48, (219,206,202))
venus = planet(sun.x, sun.y, 3, 2, 35, (150,131,150))
earth = planet(sun.x, sun.y, 4, 3, 30, (0,0,205))
mars = planet(sun.x, sun.y, 2, 4, 24, (193,68,14))
jupiter = planet(sun.x, sun.y, 8, 5, 13, (227,110,75))
saturn = planet(sun.x, sun.y, 7, 6, 10, (206,184,184))
uranus = planet(sun.x, sun.y, 6, 7, 7, (213,251,252))
neptune = planet(sun.x, sun.y, 5, 8, 5, (91,93,223))

#the_moon = planet(mercury.x, mercury.y, 0.2, 0.1, 50, (255,255,255))


if __name__ == '__main__':
    main(star.instances, planet.instances)
    quit()
    sys.exit()
