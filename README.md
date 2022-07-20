# Pygame-Solar-System
A simulation of the solar system written with Python and Pygame

# About This Project
- Contains our full solar system minus moons belonging to planets that aren't Earth (As there are many and I haven't had the time to enter their details)
- All distances and sizes are set at 1 pixel per meter then scaled down to be viewable. Scale is adjustable through the settings.json file or by scrolling with your mouse.
- All speeds are in Miles per Hour (MPH) and scalled down to be viewable. Scale can be changed in the settings.json file.
- The entire simulation is configurable through the two provided json files. When adding planets or moons, please use the name assigned to the body it is to orbit. Names must be unique for this to function correctly, otherwise first body with that name will be used by default.
- Click and drag camera (left click) + zoom functionality (scroll wheel) working. Reset viewport with space key.
- Asteroid count is dialed a lot lower than is realistic due to performance and they're individually larger than is realistic to keep them viewable. This is the only portion of the simulation that is not accurate to scale, however, the positions in which they spawn is accurate relative to the other planets.

# Tech Stack
1. [Python 3.10.4](https://www.python.org/)
2. [Pygame 2.1.2](https://www.pygame.org/news)

# Sample
Coming soon...

# Notes
No further development plans exist at this time, but if anybody wants to contribute by populating moons or other bodies I've missed that would be super helpful!