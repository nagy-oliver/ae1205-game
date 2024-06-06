# External imports
import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt, floor

# Local imports
import common as c
from game import Game
from menu import Menu

#Initialization
## pygame, menu, initial general variables (such as dt etc.)
MINSLEEP = 0.001  # Minimum interval to sleep the CPU
tsim = 0.0  # Simulation time
tstart =  0.001 * pg.time.get_ticks()
dt = 1/60

state = 1
# 0 = quit
# 1 = menu
# 2 = running

pg.init()
menu = Menu()
game = None
screen = pg.display.set_mode((c.screenX, c.screenY))

# Load background
background = pg.image.load("assets/Background.png")
background = pg.transform.scale(background, (500, 500))
backgroundRect = background.get_rect()

# Main loop
while state:
    # Time control 
    tsim = tsim + dt
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)

    # Background
    screen.fill(c.grey)
    backgroundRect.center = (c.screenX/2+25, c.screenY/2) if state == 2 else (c.screenX/2, c.screenY/2)
    screen.blit(background, backgroundRect)

    # Event handling
    events = []
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                state = 0
            elif(event.unicode in [str(i) for i in range(10)]):
                events.append(int(event.unicode))
            else:
                events.append(event.key)
        elif event.type == pg.QUIT:
            state = 0

    # State actions
    if state == 0:
        break
    if state == 1:
        state = menu.generate(screen)
        menu.eventHandler(events)
    if state == 2:
        if not game:
            game = Game(menu.weights, dt)
        state = game.generate(screen, events)

    # Generate screen
    pg.display.flip()

pg.quit()