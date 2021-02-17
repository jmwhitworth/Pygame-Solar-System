import random

#Distances in km, size in km radius and velocity is in kmp/s

class star():
    instances = []
    def __init__(self, name, size):
        self.__class__.instances.append([name,size])
        self.name = name
        self.size = size

class planet():
    instances = []
    def __init__(self, name, size, distance, velocity, colour):
        self.__class__.instances.append([name,size,distance,velocity,colour])
        self.name = name
        self.size = size
        self.distance = distance
        self.velocity = velocity
        self.colour = colour

class moon(planet):
    instances = []
    def __init__(self, name, size, distance, velocity, colour, orbiting):
        super().__init__(name, size, distance, velocity, colour)




"""
sun = star(696340)
earth = planet(6371, 147840000, 30, "blue & green")
the_moon = moon(1737.1, 384400, 1.022, "grey", earth)
asteroid_belt = asteroids(random.randrange(50,530), random.randrange(330000000,430000000), random.randrange(5,20), "grey", 700000)
"""