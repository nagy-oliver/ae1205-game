import pygame as pg
import common as c

class Game:

    weights = []
    attempt = 0

    difficulties = []
    k = 4

    score = 0
    clicks = 0
    prevclicks = 0 
    clickrate = 0   
    
    refreshtime = 1
    t = 0
    dt = None

    posList = []
    for i in range(4):
        posList.append(pg.transform.scale(pg.image.load(f"assets/{i}.png"), (500, 500)))

    progress = pg.image.load("assets/BAR.png")
    progress = pg.transform.scale(progress, (50, 500))
    progressRect = progress.get_rect()
    progressRect.center = (25, c.screenY/2)

    def __init__(self, weights, dt):
        self.weights = weights
        for weight in weights:
            self.difficulties.append(weight/20)

        self.dt = dt
        
    def generate(self, screen: pg.Surface, events):
        for event in events:
            if event == pg.K_SPACE:
                self.clicks += 1

        self.t += self.dt

        if self.t > self.refreshtime:
            self.t = 0
            curclicks = self.clicks - self.prevclicks
            self.prevclicks = self.clicks
            self.clickrate = curclicks/self.refreshtime
        
        if self.score < 100:
            if self.clickrate >= self.difficulties[self.attempt]:
                self.score = self.score + (self.clickrate-self.difficulties[self.attempt]) * self.k * self.dt
            elif self.clickrate < self.difficulties[self.attempt] and self.score > 0:
                self.score = self.score - 10*self.dt
            else:
                self.score = 0
        else:
            self.score = 100
    
        if self.score < 33:
            pos = self.posList[0]
        elif self.score == 33:
            pos = self.posList[0] #OTHER MECHANICS TO BE ADDED
        elif 66 > self.score > 33:
            pos = self.posList[1]
        elif self.score == 66:   
            pos = self.posList[1] #OTHER MECHANICS TO BE ADDED
        elif 100 > self.score > 66:
            pos = self.posList[2]
        elif self.score >= 100:
            pos = self.posList[3]
            
            text3 = c.mainFont.render("You Won!", True, c.white)
            text3Rect = text3.get_rect()
            text3Rect.center = (c.screenX/2, c.screenY/4)
            screen.blit(text3, text3Rect)
            
        def myround(x, base=5):
            return base * (x//base)
            
        height = myround(5*self.score)
        pg.draw.rect(screen, c.red, pg.Rect(0, abs(500 - height), 50, height))
        
        screen.blit(self.progress, self.progressRect)
        
        posrect = pos.get_rect()
        posrect.centerx = c.screenX/2+25
        posrect.centery = c.screenY/2
        screen.blit(pos, posrect)


        return 2