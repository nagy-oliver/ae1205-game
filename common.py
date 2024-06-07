import pygame as pg

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
red = (200, 0, 0)

# Fonts
pg.font.init()
titleFont = pg.font.Font('assets/joystix monospace.otf', 40)
mainFont = pg.font.Font('assets/joystix monospace.otf', 32)

# Screen parameters
screenX = 550
screenY = 500

pg.mixer.init()
arrowSound = pg.mixer.Sound("assets/ARROW.wav")
enterSound = pg.mixer.Sound("assets/pop.wav")
moanSound = pg.mixer.Sound("assets/Moan.wav")