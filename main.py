import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt 
  

pg.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)


MINSLEEP = 0.001  # Minimum interval to sleep the CPU
tsim = 0.0  # Simulation time
tstart =  0.001 * pg.time.get_ticks()
dt = 1/60

X = 600
Y = 500

screen = pg.display.set_mode((X, Y))

pg.draw.rect(screen, (255, 255, 255), screen.get_rect())

clicks = 0
clickrate = 0
prevclicks = 0
running = True
t = 0
refreshtime = 0.5

font = pg.font.Font('freesansbold.ttf', 32)


while running:
#SIMULATION TIME
    tsim = tsim + dt
#REMAINDER TO SLEEP FOR CPU
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    
    t+=dt
    
    if t > refreshtime:
        t = 0
        curclicks = clicks - prevclicks
        prevclicks = clicks
        clickrate = curclicks/refreshtime
    
    text = font.render('Clickrate: ' + str(clickrate), True, green, blue)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    screen.blit(text, textRect)
    
    print(clicks)
    
    
    
    pg.display.flip()
    pg.event.pump()   
#KEY COMMANDS   

    for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    clicks += 1
    keys = pg.key.get_pressed()     
# EXIT GAME
    if keys[pg.K_ESCAPE]:
        running = False

pg.quit()
