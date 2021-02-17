import pygame as pg
import math


WIDTH, HEIGHT = 1600, 900
WIN = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption("Solar System")

FPS = 60
VEL = 5

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PURPLE = (255,0,255)
WHITE = (255,255,255)

def main(star, planets, moons):

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False


        draw_window(star, planets, moons)
        

def draw_window(stars, planets, moons):

    for star in stars:
        pg.draw.circle(WIN, YELLOW, (WIDTH/2, HEIGHT/2), star[1])    

    for planet in planets:
        pg.draw.circle(WIN, planet[4], (WIDTH/2 + planet[2]*90, HEIGHT/2), planet[1]*4)



    """
    pg.draw.circle(WIN, GREEN, (WIDTH/2 + 100, HEIGHT/2), 5)
    pg.draw.circle(WIN, TEAL, (WIDTH/2 + 175, HEIGHT/2), 10)
    pg.draw.circle(WIN, BLUE, (WIDTH/2 + 300, HEIGHT/2), 6)
    pg.draw.circle(WIN, RED, (WIDTH/2 + 500, HEIGHT/2), 14)
    """
    pg.display.update()

    
