import pygame as pg
import common as c
import time

class Game:
    # Game settings variables
    weights = []
    attempt = 0
    maxWeight = 0

    # Difficulty settings
    difficulties = []
    k = 4

    # Clicking variables
    score = 0
    clicks = 0
    prevclicks = 0 
    clickrate = 0   
    
    # Clickrate refresh variables
    refreshtime = 1
    t = 0
    dt = None

    # End game wait
    waitTime = 1

    # Character images
    posList = []
    for i in range(4):
        posList.append(pg.transform.scale(pg.image.load(f"assets/{i}.png"), (500, 500)))

    # Progress bar
    progress = pg.transform.scale(pg.image.load("assets/BAR.png"), (50, 500))
    progressRect = progress.get_rect()
    progressRect.center = (25, c.screenY/2)

    def __init__(self, weights, dt):
        self.weights = weights
        for weight in weights:
            self.difficulties.append(weight/20)

        self.dt = dt
        
    def generate(self, screen: pg.Surface, events):
        # Registering of clicks
        for event in events:
            if event == pg.K_SPACE:
                self.clicks += 1
 
            #TODO - comment out - THIS IS CHEATS
            elif event == pg.K_COMMA:
                self.score = 100

        # Clickrate counter
        self.t += self.dt
        if self.t > self.refreshtime:
            self.t = 0
            curclicks = self.clicks - self.prevclicks
            self.prevclicks = self.clicks
            self.clickrate = curclicks/self.refreshtime
        
        # Score counter
        if self.score < 100:
            if self.clickrate >= self.difficulties[self.attempt]:
                self.score = self.score + (self.clickrate-self.difficulties[self.attempt]) * self.k * self.dt
            elif self.clickrate < self.difficulties[self.attempt] and self.score > 0:
                self.score = self.score - 10*self.dt
            else:
                self.score = 0
        else:
            self.score = 100

        # Position state
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
        # Winning state 
        elif self.score >= 100:
            pos = self.posList[3]
            
            textWin = c.mainFont.render("You Won!", True, c.white)
            textWinRect = textWin.get_rect()
            textWinRect.center = (c.screenX/2, c.screenY/4)
            screen.blit(textWin, textWinRect)
        
            if self.weights[self.attempt] > self.maxWeight: self.maxWeight = self.weights[self.attempt]
            
            #End game wait time
            if self.waitTime > 0: 
                self.waitTime -= self.dt
            else:
                # Move to next attempt
                self.attempt += 1
                #TODO make function
                self.score = 0
                self.clicks = 0
                self.clickrate = 0
                self.prevclicks = 0
                self.t = 0
                self.waitTime = 1
                # End game after third attempt
                if self.attempt == 3:
                    # TODO: leaderboard, offer restart, change attempt to 0
                    self.attempt = 0
                    return 1
            
        #Progress bar pixelation
        def myround(x, base=5):
            return base * (x//base)
            
        #Progress bar drawing
        height = myround(5*self.score)
        pg.draw.rect(screen, c.red, pg.Rect(0, abs(500 - height), 50, height))
        screen.blit(self.progress, self.progressRect)
        
        #Character drawing
        posrect = pos.get_rect()
        posrect.centerx = c.screenX/2+25
        posrect.centery = c.screenY/2
        screen.blit(pos, posrect)
        
        return 2