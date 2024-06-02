import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt   

pg.init()

screen = pg.display.set_mode((600, 500))

pg.draw.rect(screen, (255, 255, 255), screen.get_rect())

time.sleep(5)

pg.quit()
