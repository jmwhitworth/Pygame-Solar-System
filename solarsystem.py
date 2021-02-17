import sys
import pygame as pg


from data.stellarbodies import star, planet, moon
from data.main import main


BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PURPLE = (255,0,255)
WHITE = (255,255,255)



if __name__ == '__main__':


        # Examples of bodies that can be input
    #kerbin = planet("Earth", 20, 200, 15, "BLUE")
    sun = star("The Sun", 40)

    #variable = planet(name, size, distance, velocity, RGB colour)
    mercury = planet("Mercury", 1, 1, 48, (219,206,202))
    venus = planet("Venus", 3, 2, 35, (150,131,150))
    earth = planet("Earth", 4, 3, 30, (0,0,205))
    mars = planet("Mars", 2, 4, 24, (193,68,14))
    jupiter = planet("Jupiter", 8, 5, 13, (227,110,75))
    saturn = planet("Saturn", 7, 6, 10, (206,184,184))
    uranus = planet("Uranus", 6, 7, 7, (213,251,252))
    neptune = planet("Neptune", 5, 8, 5, (91,93,223))


    the_moon = moon("Moon", 1737.1, 384400, 1.022, "grey", earth)


        # Runs main and passes the array of planets and such
    main(star.instances, planet.instances, moon.instances)
    quit()
    sys.exit()